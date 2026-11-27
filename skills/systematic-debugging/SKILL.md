---
name: systematic-debugging
description: Use whenever investigating bugs, crashes, TypeErrors, HTTP 500s, CI failures, flaky tests, or regressions ("debug lỗi", "sửa bug", "tại sao lỗi", "investigate crash", "flaky test"). Enforces 6-step scientific root-cause debugging (Reproduce -> Evidence -> 1 Hypothesis -> Verify -> Root Fix -> Regression Test) with zero guessing.
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
- Check recent diffs (`git diff`, `git log -n 5`) if this is a regression, and compare against working sibling code paths.
- **Multi-Component Boundary Tracing:** When a bug crosses layers (e.g., Client → API → Queue → DB), add temporary boundary inspection (inputs/outputs/env entering and leaving each layer) in ONE diagnostic pass to isolate *which* boundary broke before forming a fix hypothesis.

### Step 3: Formulate ONE Explicit Hypothesis
- State clearly: *"I hypothesize X causes Y because Z."*
- Predict what observable check will prove or disprove X.

### Step 4: Verify the Hypothesis (Before Editing Production Code)
- Confirm X via targeted inspection, debugger/temporary diagnostic log, minimal reproduction script, or `git bisect`.
- **If disproved:** Revert any temporary diagnostic probes, update your mental model, and form a new hypothesis.
- **3-Failure Architectural Stop:** If **3 consecutive hypotheses or fix attempts fail**, STOP editing immediately. Question fundamental assumptions (stale build cache? wrong env/DB target? race condition? broken architectural invariant?) and present findings to the user before continuing.

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

## Red Flags & Rationalizations to Reject

| Excuse / Temptation | Reality & Required Action |
|---|---|
| *"Quick patch for now, investigate root cause later."* | **STOP.** Symptom patches (`?.`, `\|\| ""`, `catch {}`) hide the real defect and shift corruption downstream. |
| *"Let me tweak 3 things at once and re-run."* | **STOP.** Multi-variable changes make it impossible to know what fixed or masked the bug. Test 1 hypothesis at a time. |
| *"It's probably X — let me push a fix without reproducing."* | **STOP.** Unreproduced "fixes" fail silently in production. Reproduce first or state clearly why reproduction wasn't possible locally. |
| *"I don't fully understand why this happened, but tests pass now."* | **STOP.** Coincidence isn't a root cause. Explain the exact mechanism that broke and why your change fixes it. |

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
