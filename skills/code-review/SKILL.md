---
name: code-review
description: Perform a thorough, multi-dimensional code review covering correctness, edge cases, security, performance, readability, and test quality with severity-ranked findings and concrete fixes. Use when reviewing pull requests, git diffs, or source files ("review code", "check PR", "đánh giá đoạn code này").
license: MIT
compatibility: opencode
metadata:
  category: quality
  audience: developers
  version: "1.0.0"
---

# Code Review — Multi-Dimensional Engineering Review

Deliver high-signal, actionable code reviews focused on real bugs, missing edge cases, maintainability, and test gaps — not stylistic nitpicks.

## When to Use

- Reviewing a PR, staged diff (`git diff --staged`), recent commits, or a module before merge.
- Asked to sanity-check implementation quality, edge cases, or test coverage.
- **Hand-offs:** If deep security threat modeling is needed, invoke `security-review`. If profiling hot paths is needed, invoke `performance-review`.

## Step-by-Step Workflow

1. **Understand Context & Intent**:
   - Inspect the full diff (`git diff`, PR scope) AND surrounding callers/tests — never review isolated lines without reading how they are called.
2. **Evaluate Across 5 Dimensions**:
   - **Correctness & Edge Cases:** Off-by-one, null/undefined, empty collections, error propagation, race conditions, partial failure, resource leaks.
   - **Security & Trust Boundaries:** Input validation, auth/authz checks, secret exposure, injection risks.
   - **Performance & Scalability:** Unbounded loops, N+1 queries, blocking I/O in async paths, redundant allocations.
   - **Maintainability & Design:** Single responsibility, clear naming, shallow control flow, public contract clarity, backward compatibility.
   - **Tests & Verification:** Are new branches and failure paths tested? Are assertions meaningful rather than mock-tautologies?
3. **Rank Findings by Severity**:
   - **`[Blocker]`**: Bugs, data corruption, security flaws, broken builds — must fix before merge.
   - **`[Major]`**: Missing edge-case handling, missing critical tests, significant performance/maintenance traps.
   - **`[Minor]`**: Small clarity/structure improvements with clear benefit.
   - **`[Nit]`**: Optional style or naming suggestions (label clearly so author isn't blocked).
4. **Provide Evidence + Concrete Fix**:
   - Cite exact `file:line`, explain *why* it fails or risks breaking, and suggest a concrete patch.
5. **Acknowledge Strengths & State Merge Verdict**:
   - Give a clear verdict: `Approve`, `Approve with minor suggestions`, or `Request Changes`.

## Anti-Patterns (Do Not)

- **DO NOT** rubber-stamp with "LGTM, clean code!" when real bugs or missing tests exist.
- **DO NOT** flood a review with 20 formatting/whitespace nits while ignoring a missing authorization check.
- **DO NOT** invent bugs in code you did not read or claim behavior without checking callers/types.
- **DO NOT** request vague rewrites ("refactor this to be cleaner") without explaining the concrete issue and fix.

## Output Format

```markdown
## Code Review Summary
**Verdict:** Approve | Approve with Comments | Request Changes
**Scope Reviewed:** `<files or diff range>`

### Findings
1. **[Blocker] `src/orders.ts:48` — Missing transaction around stock decrement**
   - **Why:** If `payment.charge()` throws after `inventory.decrement()`, stock leaks permanently.
   - **Fix:** Wrap decrement + order insert in a transaction or compensate on failure.
...

### Test Coverage Check
- Covered: ...
- Missing: ...
```

## Examples

### Example: Reviewing a User Update Endpoint Diff
**Input:**
> "Review đoạn diff này cho endpoint `PATCH /api/users/:id`."

**Output:**
> **Verdict:** Request Changes
>
> 1. **[Blocker] `src/routes/users.ts:27` — Mass assignment & missing ownership check (BOLA)**
>    - **Why:** Passing `req.body` directly into `db.user.update({ where: { id }, data: req.body })` allows any authenticated user to modify another user's record AND escalate `role: "ADMIN"`.
>    - **Fix:** Verify `req.user.id === id || req.user.role === "ADMIN"`, and whitelist allowed fields via Zod (`name`, `bio`) before updating.
> 2. **[Major] `src/routes/users.ts:34` — Unhandled `P2025` not-found error**
>    - **Why:** Updating a nonexistent `id` throws Prisma `P2025` -> unhandled `500` instead of `404`.
>    - **Fix:** Catch `P2025` (or check existence) and return `404 Not Found`.
> 3. **[Minor] `tests/users.test.ts` — Missing negative authz test**
>    - Add a test verifying User A updating User B's profile returns `403`.
