---
name: project-planner
description: Break down an approved spec, feature, or refactor into an ordered, actionable engineering plan with small tasks, file targets, dependencies, risks, and an explicit verification step for every task. Use when planning implementation steps ("lập kế hoạch", "chia task", "break down tasks", "implementation plan").
license: MIT
compatibility: opencode
metadata:
  category: planning
  audience: developers
  version: "1.0.0"
---

# Project Planner — Ordered Task Breakdown with Verification

Turn a clear goal or specification into an executable, dependency-ordered plan where every task is small, scoped, and paired with a concrete verification command or check.

## When to Use

- Requirements or specs are clear and you need an execution roadmap before editing code.
- A task touches 3+ files, involves schema/API/UI coordination, or carries regression risk.
- **Do NOT use** when requirements are still unclear (run `grill-me` first) or for trivial 1-file changes.

## Step-by-Step Workflow

1. **Audit the Codebase Baseline**:
   - Inspect affected modules, existing tests, build/lint commands, and migration tooling.
   - Confirm how tests and typechecks are actually executed in this repo (check `package.json`, `pyproject.toml`, `Makefile`, etc.).
2. **Choose Vertical Slices Over Horizontal Layers**:
   - Prefer thin end-to-end slices (schema → service/test → route/test → UI) over creating 10 untested files before anything runs.
3. **Define Ordered Tasks (Target: 30-90 min of work per task)**:
   - For every task, specify:
     - **Objective**: One clear outcome.
     - **Files**: Exact files to create or modify.
     - **Dependencies**: Which prior tasks must finish first (and which tasks can run in parallel).
     - **Verification Step**: Exact command, test case, or observable check proving the task works before moving on.
4. **Identify Risks & Rollback Points**:
   - Highlight risky migrations, breaking API changes, or external dependencies, plus safe fallback/rollback steps.
5. **Present Plan & Confirm Execution Mode**:
   - Ask whether to proceed with `tdd-workflow` or `incremental-implementation` from Task 1.

## Anti-Patterns (Do Not)

- **DO NOT** write vague tasks like "Implement backend", "Handle edge cases", or "Write tests later" at the end of the plan.
- **DO NOT** defer all testing to a final "QA task" — every implementation task must carry its own verification step.
- **DO NOT** reference unverified file paths or npm/pytest scripts that do not exist in the repo.
- **DO NOT** create mega-tasks touching 15 files with no intermediate checkpoint.
- **DO NOT** start coding while presenting a plan unless the user explicitly instructed you to plan and execute immediately.

## Output Template

```markdown
# Implementation Plan: <Feature / Change>

## Baseline & Verification Commands
- Test: `<exact command>`
- Lint / Typecheck: `<exact command>`

## Task Breakdown
### Task 1: <Short imperative title>
- **Files:** `path/to/file.ts`, `path/to/file.test.ts`
- **Depends on:** None
- **Changes:** Concrete scope of change.
- **Verify:** Exact command + expected assertion/behavior.

## Risks & Mitigations
- <Risk> → <Mitigation / Rollback>
```

## Examples

### Example: Adding Coupon Redemption to an Express + Prisma App
**Input:**
> "Chia task implement tính năng coupon theo spec đã chốt. Repo dùng Express, TypeScript, Prisma, Vitest."

**Output:**
```markdown
# Implementation Plan: Checkout Coupon Redemption

## Baseline & Verification Commands
- Test: `npm test` (Vitest)
- Typecheck: `npm run typecheck`

## Task Breakdown

### Task 1: Add Coupon & CouponRedemption models + migration
- **Files:** `prisma/schema.prisma`, `prisma/migrations/...`
- **Depends on:** None
- **Changes:** Add `Coupon` (`code` unique uppercase, `discountType`, `value`, `maxUses`, `usedCount`, `expiresAt`) and `CouponRedemption` with `@@unique([couponId, userId])`.
- **Verify:** Run `npx prisma migrate dev --name add_coupons` and `npx prisma validate`; verify migration applies cleanly on empty test DB.

### Task 2: Implement discount calculation & validation domain service (TDD)
- **Files:** `src/services/coupon.service.ts`, `tests/services/coupon.service.test.ts`
- **Depends on:** Task 1
- **Changes:** Pure discount calculation (percent rounding, fixed clamping to `>= 0`) and eligibility checks (case-insensitive code, expiry, usage limits).
- **Verify:** Run `npx vitest run tests/services/coupon.service.test.ts`; all unit tests for valid, expired, exhausted, and clamp edge cases pass.

### Task 3: Integrate atomic redemption inside order creation transaction
- **Files:** `src/services/order.service.ts`, `tests/integration/order-coupon.test.ts`
- **Depends on:** Task 2
- **Changes:** Inside `prisma.$transaction`, execute conditional atomic update `where: { id, usedCount: { lt: maxUses } }` and insert `CouponRedemption`; roll back if order fails.
- **Verify:** Run `npx vitest run tests/integration/order-coupon.test.ts` including a `Promise.all` concurrency test confirming only 1 of 2 requests claims the last slot.

### Task 4: Wire preview/order endpoints & rate limiting
- **Files:** `src/routes/coupons.ts`, `src/routes/orders.ts`, `tests/integration/coupon-routes.test.ts`
- **Depends on:** Task 3
- **Changes:** Add `POST /api/coupons/preview` (rate-limited 20/min/user) and optional `couponCode` validation in `POST /api/orders`.
- **Verify:** Run full `npm test` and `npm run typecheck`; confirm HTTP `200`, `400`, `409`, and `429` status codes match spec.

## Risks & Mitigations
- **Race condition on `usedCount`** → Enforced via DB conditional update inside transaction + unique constraint on `(couponId, userId)`.
```
