---
name: performance-review
description: Diagnose and optimize application performance through measurement-first profiling (latency, SQL N+1 queries, memory leaks, algorithmic complexity, bundle size, caching) without guessing. Use when investigating slow endpoints, high CPU/memory, heavy queries, or frontend lag ("tối ưu hiệu năng", "chậm quá", "N+1 query", "profile performance").
license: MIT
compatibility: opencode
metadata:
  category: quality
  audience: developers
  version: "1.0.0"
---

# Performance Review — Measure First, Optimize Second

Eliminate real bottlenecks backed by profiling, query plans, or complexity analysis. Never optimize blindly.

## When to Use

- API endpoints have high p95/p99 latency, timeouts, or DB CPU spikes.
- Frontend pages suffer slow initial load, large bundles, or UI jank/re-render storms.
- Reviewing loops, batch jobs, or DB access patterns likely to degrade under realistic data scale.
- **Do NOT use** for premature micro-optimizations on cold code paths or refactoring clarity alone (use `code-simplification`).

## Step-by-Step Workflow

1. **Define Target & Workload Scale**:
   - Clarify SLA/budget (e.g., p95 < 200ms at 10k rows, bundle < 200KB gzip) and realistic data sizes ($N$, concurrency).
2. **Measure Baseline Before Editing**:
   - Gather concrete evidence: benchmark script, profiler trace, `EXPLAIN ANALYZE`, query count logs, memory snapshot, or build bundle analyzer output.
3. **Locate the Dominant Bottleneck (80/20 Rule)**:
   - **Database:** N+1 queries inside loops, missing composite indexes, `SELECT *` pulling huge blobs, offset pagination on deep pages, missing connection pooling.
   - **Backend / Async:** Sequential `await` in loops instead of bounded `Promise.all`, synchronous CPU/JSON/crypto work blocking event loop, unbounded in-memory caches leaking RAM.
   - **Algorithmic:** $O(n^2)$ nested scans / repeated `.includes()` / `.find()` where a `Map`/`Set` gives $O(n)$.
   - **Frontend:** Unmemoized expensive derived state, huge unsplit third-party dependencies, waterfall fetches, missing virtualization for long lists.
4. **Apply Targeted Fix**:
   - Fix the measured bottleneck cleanly (e.g., batch query / JOIN / dataloader, index + keyset pagination, streaming instead of buffering whole files, `Map` lookup).
5. **Re-Measure & Compare Before vs After**:
   - Re-run the exact same benchmark / query plan / build measurement and report concrete numbers.
   - Verify correctness stayed 100% identical (`verification-before-done`).

## Anti-Patterns (Do Not)

- **DO NOT** guess which function is slow and rewrite clean code into unreadable bit-twiddling without profiling.
- **DO NOT** invent fake speedup numbers ("50% faster!") without running a before/after measurement.
- **DO NOT** add unbounded in-memory caches (`const cache = {}`) that silently cause OOM crashes or stale data bugs.
- **DO NOT** fire `Promise.all` unconditionally on 10,000 items (can exhaust DB connections or upstream rate limits — use bounded concurrency).
- **DO NOT** sacrifice correctness, transactions, or security checks just to shave milliseconds.

## Output Template

```markdown
## Performance Analysis
- **Baseline Measurement:** `<tool / query / timing observed>`
- **Root Bottleneck:** `<exact file:line and complexity / I/O cause>`
- **Optimization Applied:** `<change>`
- **Post-Change Measurement:** `<exact new timing / query count / bundle delta>`
- **Trade-offs / Notes:** `<cache invalidation, memory bound, index write cost>`
```

## Examples

### Example: Fixing N+1 Queries and $O(n^2)$ Grouping
**Input:**
> "Endpoint `GET /api/orders` mất ~1.8s khi user có 200 đơn hàng. Kiểm tra và tối ưu giúp tôi."

**Output:**
> - **Baseline Measurement:** Logged Prisma queries on seeded 200 orders (each with 5 items): executed **201 SQL queries** (`1` for orders + `200` per-order item queries), total **1,740 ms**.
> - **Root Bottleneck:**
>   1. `src/services/order.service.ts:24` runs `await db.orderItem.findMany({ where: { orderId } })` inside `for (const order of orders)` (classic N+1).
>   2. `src/services/order.service.ts:31` matches user metadata using `users.find(u => u.id === order.userId)` inside loop ($O(n \cdot m)$).
> - **Fix Applied:**
>   1. Replaced loop query with single eager batch query `where: { orderId: { in: orderIds } }` (or Prisma `include: { items: true }`) and added pagination (`take: 20` default).
>   2. Indexed `users` into a `Map<string, User>` ($O(1)$ lookup).
> - **Post-Change Measurement:** Re-ran query benchmark on same 200-order dataset: **2 SQL queries**, **48 ms** (~36x latency reduction on measured local dataset). Tests in `tests/orders.test.ts` pass (`8/8`).
