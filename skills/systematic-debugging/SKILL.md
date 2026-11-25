---
name: systematic-debugging
description: Investigate bugs, crashes, regressions, and flaky tests through strict scientific root-cause analysis (Reproduce -> Collect Evidence -> Formulate 1 Hypothesis -> Verify -> Fix Root Cause -> Verify). Use whenever debugging an error, stack trace, failing test, or unexpected behavior ("debug lỗi", "sửa bug", "tại sao lỗi này xảy ra", "investigate crash").
license: MIT
compatibility: opencode
metadata:
  category: implementation
  audience: developers
  version: "1.0.0"
---

# Systematic Debugging — Evidence Before Fixes

Never guess and patch symptoms. Find the proven root cause through reproducible observation and falsifiable hypotheses before touching production code.

## When to Use

- Any bug report, runtime exception, failing test, race condition, performance regression, build failure, or unexpected output.
- Especially critical when an initial "obvious" fix failed or when multiple modules interact.
- **Do NOT use** to implement brand-new features from scratch (use `grill-me` / `tdd-workflow`).

## Mandatory 6-Step Debugging Protocol

### Step 1: Reproduce Reliably
- Run the failing command, test, or request locally to confirm the exact failure behavior.
- Narrow the trigger to the smallest reproducible case (exact input, env vars, OS/runtime, data state).
- If intermittent/flaky, identify timing, ordering, shared state, or concurrency conditions.

### Step 2: Gather Raw Evidence (Read Everything)
- Inspect the **complete** error message, stack trace, exit code, and server/test logs — never stop at line 1.
- Check recent diffs (`git diff`, `git log -n 5`) if this is a regression.
- Read the actual failing code path and trace values from entry to failure point.

### Step 3: Formulate ONE Explicit Hypothesis
- State clearly: *"I hypothesize X causes Y because Z."*
- Predict what observable check will prove or disprove X.

### Step 4: Verify the Hypothesis (Before Editing Production Code)
- Confirm X via targeted inspection, debugger/temporary diagnostic log, minimal reproduction script, or `git bisect`.
- **If disproved:** Revert any temporary diagnostic probes, update your mental model, and form a new hypothesis.
- **Circuit Breaker:** If **2 consecutive hypotheses fail**, STOP making guesses. Re-read assumptions from scratch (wrong config file? stale build artifact? wrong DB/env? misunderstood API contract?) and report findings clearly.

### Step 5: Implement a Targeted Root-Cause Fix + Regression Test
- Fix the underlying cause, not just a surface null-check symptom.
- Write a regression test (following `tdd-workflow`) that fails before the fix and passes after.

### Step 6: Verify End-to-End
- Clean up any temporary debug logs.
- Re-run the original failing reproducer AND the broader test/build suite (`verification-before-done`).

## Anti-Patterns (Do Not)

- **DO NOT** change 3 things at once hoping one fixes the bug ("shotgun debugging").
- **DO NOT** wrap failing code in `try { ... } catch {}` or `|| ""` / `?.` just to silence crashes without knowing *why* the value was invalid.
- **DO NOT** propose a fix before reading the full stack trace and reproducing (or inspecting actual failing logs).
- **DO NOT** leave `console.log` / `print` debug statements behind after fixing.
- **DO NOT** delete or skip a failing test to make CI look green.

## Debug Report Format

```markdown
## Root Cause Investigation
- **Reproduction:** `<exact command or steps>` → `<observed failure>`
- **Evidence:** `<key stack frame / log / state observed>`
- **Hypothesis:** `<cause>` → **Verification:** `<how confirmed>`
- **Root Cause:** `<concise explanation>`
- **Fix & Regression Test:** `<files modified>`
- **Verification:** `<fresh post-fix test output>`
```

## Examples

### Example: API Returning 500 on Empty Search Query
**Input:**
> "Endpoint `GET /api/products?q=` đang trả 500 Internal Server Error trên prod nhưng test unit vẫn pass. Debug giúp tôi."

**Output:**
> 1. **Reproduce:** Ran `npx vitest run` (all passed — tests only tested `q="laptop"`, not `q=""`). Reproduced via integration test hitting `GET /api/products?q=`:
>    `TypeError: Cannot read properties of undefined (reading 'trim')` at `src/controllers/product.controller.ts:42`.
> 2. **Evidence:** Express query parser yields `req.query.q = ""` (empty string) or `string[]` if repeated (`?q=a&q=b`). At line 39, `parseSearchTerm` had `const q = req.query.q || undefined` turning `""` into `undefined`, then line 42 called `q.trim()`.
> 3. **Hypothesis:** `parseSearchTerm` coerces empty string `""` to `undefined` via `||`, while the caller assumes a `string` is returned.
> 4. **Verify:** Confirmed by inspecting `src/controllers/product.controller.ts:38-45` and running a failing test for `?q=` and `?q=a&q=b`.
> 5. **Fix & Regression Test:** Updated `parseSearchTerm` to check `typeof raw === "string" ? raw.trim() : ""` (handling `undefined` and `string[]` safely) and added tests for `?q=`, missing `q`, and `?q=a&q=b`.
> 6. **Final Verification:** `npx vitest run tests/product.controller.test.ts` → `9 passed (9)`.
