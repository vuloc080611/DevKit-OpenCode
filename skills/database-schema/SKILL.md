---
name: database-schema
description: Design relational database schemas, entity relationships, constraints, query-driven indexes, and safe reversible migrations (including zero-downtime migration strategies). Use when modeling tables, Prisma/SQL/Drizzle/Alembic schemas, or optimizing indexes ("thiết kế database", "ERD", "migration", "tối ưu index").
license: MIT
compatibility: opencode
metadata:
  category: web-backend
  audience: developers
  version: "1.0.0"
---

# Database Schema — Data Modeling, Indexes & Safe Migrations

Design normalized, constraint-enforced schemas and safe migrations matched to real read/write query patterns.

## When to Use

- Designing new tables/collections, foreign key relationships, or ORM schemas (SQL, Prisma, Drizzle, TypeORM, SQLAlchemy/Alembic).
- Planning schema changes, data backfills, or adding indexes for slow queries.
- **Do NOT use** to tune application-level N+1 loops (use `performance-review`).

## Step-by-Step Workflow

1. **Inspect Existing Schema & Query Patterns**:
   - Read current schema/migrations, ORM conventions, ID strategy (UUIDv7/ULID vs `BIGINT` identity), and timestamp/soft-delete conventions.
   - List the actual queries this schema must serve (read filters, sort orders, uniqueness rules, write frequency).
2. **Model Entities & Enforce Integrity at the DB Level**:
   - Apply 3NF by default; denormalize *only* with an explicit read-performance rationale and sync strategy.
   - Enforce invariants in the DB, not only in app code: `NOT NULL`, `PRIMARY KEY`, `FOREIGN KEY` (`ON DELETE RESTRICT/CASCADE` intentionally chosen), `UNIQUE`, and `CHECK` constraints (e.g., `amount_minor >= 0`, `max_uses > 0`).
   - Store money in integer minor units (`BIGINT` / `INTEGER` cents/VND) or exact `NUMERIC(p, s)` — never `FLOAT`/`DOUBLE`.
   - Store timestamps in `TIMESTAMPTZ` (UTC).
3. **Design Indexes From Actual Queries**:
   - Follow leftmost-prefix rule for composite B-Tree indexes: put equality columns before range/sort columns (`WHERE tenant_id = ? AND status = ? ORDER BY created_at DESC` → `(tenant_id, status, created_at DESC)`).
   - Add partial indexes (`WHERE deleted_at IS NULL`) when queries consistently filter active rows.
   - Do not over-index write-heavy tables without read justification.
4. **Plan Safe, Reversible Migrations**:
   - Separate destructive changes using **Expand → Backfill → Contract** across releases (add nullable column → backfill in batches → add `NOT NULL` / drop old column later).
   - On large Postgres tables, note `CREATE INDEX CONCURRENTLY` (outside transaction block) to avoid locking writes.
   - Provide `up` and `down` (rollback) steps and verify locally against a clean DB.

## Anti-Patterns (Do Not)

- **DO NOT** store monetary amounts as IEEE-754 `FLOAT`/`REAL`.
- **DO NOT** leave uniqueness or positive-balance invariants solely to application `if` checks (race conditions will corrupt data).
- **DO NOT** blindly add single-column indexes on every column without matching actual `WHERE`/`JOIN`/`ORDER BY` clauses.
- **DO NOT** run `DROP COLUMN` or `ALTER COLUMN ... TYPE` blindly on live production tables without an expand-and-contract plan.
- **DO NOT** use `ON DELETE CASCADE` on financial, audit, or invoice records where accidental parent deletion would destroy accounting history.

## Examples

### Example: Multi-Tenant Wallet & Ledger Schema (PostgreSQL)
**Input:**
> "Thiết kế database schema cho ví điểm thưởng (wallet + lịch sử giao dịch không bị âm số dư, chống double-credit khi retry)."

**Output:**
```sql
CREATE TABLE wallets (
  id UUID PRIMARY KEY,
  user_id UUID NOT NULL UNIQUE REFERENCES users(id) ON DELETE RESTRICT,
  balance_minor BIGINT NOT NULL DEFAULT 0 CHECK (balance_minor >= 0),
  currency CHAR(3) NOT NULL DEFAULT 'VND',
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE wallet_transactions (
  id UUID PRIMARY KEY,
  wallet_id UUID NOT NULL REFERENCES wallets(id) ON DELETE RESTRICT,
  idempotency_key VARCHAR(128) NOT NULL,
  direction VARCHAR(10) NOT NULL CHECK (direction IN ('CREDIT', 'DEBIT')),
  amount_minor BIGINT NOT NULL CHECK (amount_minor > 0),
  balance_after_minor BIGINT NOT NULL CHECK (balance_after_minor >= 0),
  reference_type VARCHAR(32) NOT NULL,
  reference_id VARCHAR(128) NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (wallet_id, idempotency_key)
);

-- Serves paginated transaction history per wallet ordered newest-first
CREATE INDEX idx_wallet_tx_wallet_created
  ON wallet_transactions (wallet_id, created_at DESC);
```
> **Concurrency & Safety Notes:**
> - `CHECK (balance_minor >= 0)` guarantees non-negative balances even if an app bug slips through.
> - `UNIQUE (wallet_id, idempotency_key)` prevents double-credit/double-debit on client or webhook retries.
> - `ON DELETE RESTRICT` protects financial ledger history from accidental user deletion.
