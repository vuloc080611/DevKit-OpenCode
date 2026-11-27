---
name: refactor-safe
description: Restructure existing code across functions or modules without changing external behavior by building characterization tests first, applying small mechanical steps, migrating callers explicitly, and verifying tests after every step. Use when extracting modules, renaming contracts, or splitting monoliths ("refactor an toàn", "tách module", "clean up without breaking"). For local simplification of nested logic, use code-simplification.
license: MIT
compatibility: opencode
metadata:
  category: quality
  audience: developers
  version: "1.0.0"
---

# Refactor Safe — Behavior-Preserving Structural Improvement

Improve internal code structure without altering observable external behavior, backed by tests before and after every step.

## When to Use

- Splitting large god-functions or god-classes into focused modules.
- Extracting shared helpers to eliminate duplication.
- Renaming symbols, normalizing interfaces, or decoupling tight dependencies.
- **Do NOT use** to sneak new product features or behavior changes into the same diff — separate feature work from refactoring.

## Step-by-Step Workflow

1. **Map Scope & Callers First**:
   - Search the entire repository for all callers, imports, exports, dynamic references, and serialized contracts of the target code.
2. **Establish a Characterization Test Safety Net**:
   - Run existing tests first.
   - If existing coverage around the legacy target is weak or missing, write **characterization (golden-master) tests** capturing exact current observable behavior (return values, side effects, thrown error types, edge outputs) BEFORE changing structure — even when legacy behavior looks quirky.
3. **Choose Small Mechanical Transformations**:
   - Break the refactor into tiny, reversible steps:
     - Extract pure helper function → run tests
     - Inject dependency / introduce interface → run tests
     - Use **Parallel Implementation / Strangler Seam** when changing large public interfaces (keep old adapter calling new implementation until all callers migrate)
     - Move module & update all imports → run tests + typecheck
     - Remove deprecated wrapper only after confirming zero remaining callers → run tests
4. **Preserve Contracts (or Migrate All Callers Atomically)**:
   - Keep external signatures, error types, and return shapes identical unless an explicit contract migration across all callers is part of the plan.
5. **Run Full Verification**:
   - After the final step, run full test suite, typecheck, and linter (`verification-before-done`). Confirm `git diff` contains only structural changes with zero unintended behavior drift.

## Anti-Patterns (Do Not)

- **DO NOT** refactor code that has zero tests without writing characterization tests first.
- **DO NOT** mix bug fixes or new feature requirements inside a pure refactor commit — bugs uncovered during refactoring should be documented or fixed in a separate verified step.
- **DO NOT** rename exported symbols or move files without searching all usages (including tests, configs, routes, and dynamic imports).
- **DO NOT** perform a "big bang rewrite" deleting working code before the replacement passes every existing test.

## Checklist

- [ ] All callers & exports mapped across repo
- [ ] Baseline tests pass (characterization tests added if coverage was lacking)
- [ ] Zero behavior changes mixed into refactor
- [ ] Full test suite, typecheck, and lint pass after final edit

## Examples

### Example: Splitting a 220-Line Order Handler
**Input:**
> "Hàm `processCheckout` trong `src/routes/checkout.ts` dài 220 dòng, vừa validate, vừa tính giá, vừa gọi Stripe. Tách cho sạch nhưng không đổi logic cũ."

**Output Plan & Execution:**
> 1. **Callers & Coverage Check:** Searched repo — `processCheckout` is mounted only at `POST /api/checkout` in `src/app.ts:41`. Existing test `tests/checkout.test.ts` covers happy path + invalid card (`3 tests`), missing coupon/tax rounding assertions.
> 2. **Safety Net:** Added 4 characterization tests in `tests/checkout.test.ts` locking down tax rounding, empty-cart `400`, and Stripe failure rollback (`7/7 passing`).
> 3. **Incremental Extractions:**
>    - Step A: Extracted pure `calculateOrderTotals(items, coupon, taxRate)` to `src/services/pricing.ts` → ran `vitest` (`7/7`).
>    - Step B: Extracted `validateCheckoutPayload(body)` Zod schema to `src/validators/checkout.ts` → ran `vitest` (`7/7`).
>    - Step C: Slimmed `processCheckout` to orchestrate validation → pricing → payment call → DB persistence (`38 lines`).
> 4. **Final Verification:** `npm test` (`31 passed`), `npm run typecheck` (`0 errors`), `npm run lint` (`0 warnings`).
