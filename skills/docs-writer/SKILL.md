---
name: docs-writer
description: Write clear, accurate technical documentation including module/function docstrings, API guides, architecture overviews, and operational runbooks strictly grounded in inspected source code. Use when documenting modules, writing docstrings, or creating developer/ops guides ("viết docs", "viết docstring", "tài liệu kỹ thuật", "runbook").
license: MIT
compatibility: opencode
metadata:
  category: devtools
  audience: developers
  version: "1.0.0"
---

# Docs Writer — Clear Technical Docs & Docstrings

Produce concise, maintainable documentation that explains contracts, invariants, failure modes, and operational procedures accurately without parroting obvious syntax.

## When to Use

- Adding docstrings/JSDoc/TSDoc to public APIs, libraries, or complex non-obvious modules.
- Writing developer onboarding guides, integration guides, architecture notes, or production runbooks.
- **Do NOT use** for top-level `README.md` (use `readme-generator`), ADRs (use `architecture-decision`), or git changelogs (use `changelog-generator`).

## Step-by-Step Workflow

1. **Read the Source Code & Callers Completely**:
   - Inspect exact parameter types, return shapes, default values, thrown errors, side effects, and concurrency/idempotency guarantees.
   - Check existing doc style in the repo (JSDoc/TSDoc, Google/NumPy Python docstrings, GoDoc, Rustdoc).
2. **Match Audience & Format**:
   - **Code Docstrings:** Document *contract, invariants, units, edge cases, and raised errors* — skip restating types already clear from signatures.
   - **Developer / Integration Guides:** Prerequisites → Auth → End-to-End Example → Error Handling → Edge Cases.
   - **Operational Runbooks:** Trigger/Alert → Quick Triage Checks → Diagnosis → Safe Mitigation / Rollback → Escalation.
3. **Preserve Unrelated Comments & Code Integrity**:
   - When adding docstrings to source files, keep existing behavior and unrelated comments untouched.
4. **Verify Examples & Signatures**:
   - Ensure every code snippet, flag, endpoint path, and symbol name in the documentation matches actual inspected code and compiles/runs if executed.

## Anti-Patterns (Do Not)

- **DO NOT** write tautological comments (`/** Gets the user by id. @param id The id */` — zero new information!).
- **DO NOT** guess undocumented error codes, default timeouts, or side effects without reading the implementation.
- **DO NOT** alter code logic while "just adding docstrings" (if you spot a bug, document/flag it separately).
- **DO NOT** write sprawling prose where a 4-row table or runnable example communicates twice as fast.

## Examples

### Example 1: High-Value TypeScript Docstring
**Input:**
> "Viết TSDoc cho hàm `acquireDistributedLock` trong `src/lib/lock.ts`."

**Output (after reading `src/lib/lock.ts`):**
```ts
/**
 * Attempts to acquire a short-lived Redis mutex using `SET key token NX PX ttlMs`.
 *
 * Callers must pass the returned release token to {@link releaseDistributedLock} so a
 * slow worker cannot accidentally delete another worker's lock after TTL expiry.
 *
 * @param key - Logical resource identifier (automatically prefixed with `lock:`).
 * @param ttlMs - Lease duration in milliseconds; must be greater than worst-case work time.
 * @returns Unique ownership token if acquired, or `null` if another holder owns the lock.
 * @throws {Error} When Redis is unreachable or `ttlMs <= 0`.
 */
```

### Example 2: Incident Runbook Section
**Input:**
> "Viết runbook ngắn xử lý alert `QueueBacklogHigh` cho worker `pg-boss`."

**Output:**
> ## Runbook: `QueueBacklogHigh`
> - **Trigger:** Pending `pgboss.job` count > 5,000 for > 10 minutes.
> - **1. Triage (Read-Only):**
>   - Check worker health/logs (`kubectl logs -l app=worker --tail=100`).
>   - Inspect stuck/failed jobs by name:
>     `SELECT name, state, count(*) FROM pgboss.job GROUP BY name, state;`
> - **2. Common Causes & Safe Mitigation:**
>   - *Worker crash loop / OOM:* Check pod restarts; scale replicas or increase memory limit.
>   - *Downstream SMTP/Webhook outage:* Pause non-critical queue consumers or verify retry backoff; do **not** `TRUNCATE pgboss.job` in production.
> - **3. Recovery Verification:** Confirm `created`/`active` backlog trends downward over 5 minutes and error rate drops below 1%.
