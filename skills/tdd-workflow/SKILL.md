---
name: tdd-workflow
description: Use whenever implementing business logic, API handlers, parsers, validators, or bug fixes using Red-Green-Refactor ("viết test trước", "TDD", "Red-Green-Refactor", "test-first"). Strictly bans writing production code before watching a new failing test fail for the expected reason.
license: MIT
compatibility: opencode
metadata:
  category: implementation
  audience: developers
  version: "1.0.0"
---

# TDD Workflow — Strict Red-Green-Refactor Discipline

Write no production logic before a failing test proves what is missing or broken. Drive design through small, fast feedback loops.

## When to Use

- Implementing business logic, services, parsers, validators, API handlers, state machines, or bug fixes.
- Whenever the user asks for TDD or high-confidence regression protection.
- **Exception Handling:** If a change is purely static markup/CSS styling, documentation, or config wiring where unit tests cannot meaningfully assert behavior, state that explicitly and switch to `verification-before-done` checks instead of writing fake tautological tests.

## Step-by-Step Workflow

### 1. RED — Write One Failing Test First
- Pick the smallest next behavior (one happy path or one edge case).
- Write the test using the repo's existing test framework (`vitest`, `jest`, `pytest`, `go test`, etc.).
- **Run the test immediately** and observe it FAIL.
- Confirm it fails for the *expected reason* (missing behavior or failed assertion), NOT because of a syntax error, broken import, or wrong test setup.

### 2. GREEN — Write Minimal Production Code
- Implement *only* the simplest production code needed to make that failing test pass.
- Do not add speculative flags, premature abstractions, or untested branches "just in case".
- **Run the test suite** and confirm the new test and all existing tests pass.

### 3. REFACTOR — Clean Without Breaking Green
- Remove duplication, improve naming, simplify branching (`code-simplification`), and tighten types while keeping behavior identical.
- **Re-run the test suite** immediately after refactoring to confirm everything stays green.

### 4. Repeat Per Requirement / Edge Case
- Move to the next edge case (boundary values, null/empty, invalid inputs, error paths, concurrency) and repeat Red → Green → Refactor.

## Anti-Patterns (Do Not)

- **DO NOT** write production implementation first and backfill tests afterward to "check the box".
- **DO NOT** skip running the RED step — an unexecuted test might pass trivially or fail for the wrong reason.
- **DO NOT** write multiple failing tests across 5 features at once before making the first one green.
- **DO NOT** mock the system under test so heavily that the test only asserts your mocks return what you configured.
- **DO NOT** weaken or delete an existing assertion just to turn a broken build green.

## Red Flags & Rationalizations to Reject

| Excuse / Temptation | Reality & Required Action |
|---|---|
| *"I'll write the test immediately after implementing."* | **STOP.** Post-hoc tests prove existing code passes, not that the test catches missing behavior. Write the failing test first. |
| *"New test passed on first try — great!"* | **STOP.** An immediate pass means the behavior already existed or the assertion tests the wrong thing. Prove the test can fail first. |
| *"Too simple / trivial to write a failing test first."* | **STOP.** Simple functions take 30 seconds to test first and prevent subtle boundary regressions (`0`, `null`, `NaN`). |
| *"Keep the untested draft as reference while writing the test."* | **STOP.** Delete/stash the untested production edit, observe RED first, then write minimal code to reach GREEN. |
| *"I already tested it manually."* | **STOP.** Manual runs aren't repeatable regressions. Capture the check in an automated test. |

## Iron Rule

> **If you wrote production code before seeing a failing test for that behavior, delete or revert the production code, write the failing test first, verify RED, then re-implement.**

## Examples

### Example: Implementing Password Strength / Expiry or Discount Clamp
**Input:**
> "Implement hàm `calculateDiscount(subtotal, percent)` theo TDD: làm tròn xuống số nguyên, clamp về 0 nếu invalid, không vượt quá subtotal."

**Execution Flow (Output):**
> **Step 1 (RED):** Added test in `tests/pricing.test.ts` for percentage floor rounding and `>100%` clamping.
> Ran `npx vitest run tests/pricing.test.ts`:
> - `FAIL`: `TypeError: calculateDiscount is not a function` (expected — not implemented yet).
>
> **Step 2 (GREEN):** Implemented minimal `calculateDiscount` in `src/pricing.ts`:
> ```ts
> export function calculateDiscount(subtotal: number, percent: number): number {
>   if (subtotal <= 0 || percent <= 0) return 0;
>   const clampedPercent = Math.min(percent, 100);
>   return Math.floor((subtotal * clampedPercent) / 100);
> }
> ```
> Ran `npx vitest run tests/pricing.test.ts` → `4 passed (4)`.
>
> **Step 3 (RED - next edge case):** Added test for `NaN` / `Infinity` inputs → failed (`NaN` returned instead of `0`).
> **Step 4 (GREEN + REFACTOR):** Guarded with `Number.isFinite(subtotal) && Number.isFinite(percent)` → re-ran `npx vitest run tests/pricing.test.ts` → `6 passed (6)`.
