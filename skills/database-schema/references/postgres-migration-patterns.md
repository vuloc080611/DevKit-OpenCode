# Safe PostgreSQL Schema & Zero-Downtime Migration Patterns

Reference guide for `database-schema` when planning migrations on active production tables.

## 1. Expand → Backfill → Contract (Safe Breaking Changes)

Never rename/drop columns or tighten constraints in a single deploy while old application instances still read/write the old shape.

### Example: Renaming `full_name` → `display_name`
1. **Deploy 1 (Expand):**
   - `ALTER TABLE users ADD COLUMN display_name TEXT;` (nullable!)
   - Update app code to dual-write both `full_name` and `display_name`, reading `COALESCE(display_name, full_name)`.
2. **Backfill (Out-of-band batched job):**
   - Update rows in bounded batches (e.g., 1,000–5,000 IDs per transaction with brief sleep) so autovacuum/replication lag doesn't spike.
3. **Deploy 2 (Enforce & Switch Reads):**
   - Add `NOT NULL` safely without long `ACCESS EXCLUSIVE` table scan lock:
     ```sql
     ALTER TABLE users ADD CONSTRAINT users_display_name_not_null
       CHECK (display_name IS NOT NULL) NOT VALID;
     ALTER TABLE users VALIDATE CONSTRAINT users_display_name_not_null;
     ```
   - Switch app reads to `display_name` only.
4. **Deploy 3 (Contract):**
   - Stop writing `full_name` and drop `full_name` in a later cleanup migration.

## 2. Non-Blocking Index Creation
- Standard `CREATE INDEX` blocks all writes (`INSERT`, `UPDATE`, `DELETE`) until index build finishes.
- On live PostgreSQL tables, run outside a transaction block:
  ```sql
  CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_orders_user_created
    ON orders (user_id, created_at DESC);
  ```
- Remember to inspect `pg_index.indisvalid` if a concurrent build fails mid-way (drop invalid index before retrying).

## 3. Foreign Keys Without Full Table Lockout
```sql
ALTER TABLE orders
  ADD CONSTRAINT fk_orders_coupon
  FOREIGN KEY (coupon_id) REFERENCES coupons(id)
  ON DELETE RESTRICT NOT VALID;

ALTER TABLE orders VALIDATE CONSTRAINT fk_orders_coupon;
```
`NOT VALID` takes a brief metadata lock; `VALIDATE CONSTRAINT` acquires a `SHARE UPDATE EXCLUSIVE` lock allowing concurrent reads and writes!

## 4. Set Lock & Statement Timeouts in Migrations
Prevent a slow migration lock wait from piling up all app traffic behind it:
```sql
SET lock_timeout = '3s';
SET statement_timeout = '30s';
```
If lock acquisition times out, fail fast and retry safely instead of stalling production requests.

## 5. PostgreSQL Indexing & Row-Level Security (RLS) Gotchas
- **Foreign Keys Are NOT Auto-Indexed:** PostgreSQL enforces FKs without creating indexes on child FK columns. Always add indexes on frequently joined/deleted FK columns (`CREATE INDEX CONCURRENTLY idx_order_items_order_id ON order_items(order_id);`) to avoid full table scans on parent `DELETE` or joins.
- **Covering Indexes (`INCLUDE`):** If hot list queries read 2–3 extra columns after filtering, `CREATE INDEX ... ON orders (user_id, created_at DESC) INCLUDE (status, total_minor);` enables index-only scans without bloating sort keys.
- **RLS Policy Performance:** Wrap `auth.uid()` / `current_setting(...)` inside a scalar subselect (`USING (user_id = (SELECT auth.uid()))`) so Postgres caches it per statement instead of calling it per row.
