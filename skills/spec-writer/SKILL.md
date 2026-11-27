---
name: spec-writer
description: Use whenever converting aligned requirements or product ideas into a concise, actionable PRD or technical specification ("write spec", "PRD", "acceptance criteria", "viết spec", "đặc tả tính năng"). Produces goals, non-goals, user flows, data contracts, edge cases, and testable Given/When/Then criteria.
license: MIT
compatibility: opencode
metadata:
  category: planning
  audience: developers
  version: "1.0.0"
---

# Spec Writer — Actionable PRD & Feature Specification

Convert aligned requirements into a crisp, unambiguous specification that engineers and AI agents can execute and verify without guesswork.

## When to Use

- Requirements have been clarified (e.g., via `grill-me`) and need a written PRD / feature spec before planning tasks.
- A team or user asks for a formal specification, API/behavior contract, or acceptance criteria document.
- **Do NOT use** if core requirements are still vague (run `grill-me` first) or if the user wants a step-by-step task list (use `project-planner`) or a technology trade-off record (use `architecture-decision`).

## Step-by-Step Workflow

1. **Gather Ground Truth**:
   - Inspect existing docs, schemas, routes, and domain terminology in the repository so the spec uses exact real names and conventions.
2. **Define Problem & Boundaries**:
   - Write a 2-3 sentence **Problem Statement** (who is blocked, what fails today, why solve it now).
   - State explicit **Goals** (measurable outcomes) and **Non-Goals** (what this spec deliberately excludes to stop scope creep).
3. **Specify Flows & Contracts**:
   - Document primary **User / System Flows** step by step.
   - Define **Data & Interface Contracts** (fields, types, validation constraints, state transitions, auth rules).
4. **Capture Edge Cases & Failure Handling**:
   - List every non-happy-path scenario: empty states, invalid inputs, duplicates, rate limits, concurrency races, downstream failures, and rollback expectations.
   - Check operational readiness: **backward compatibility**, **data migration/backfill**, **idempotency**, **observability (logs/metrics)**, and **rollout/rollback** impact.
5. **Write Testable Acceptance Criteria**:
   - Express each requirement in verifiable **Given / When / Then** or concrete pass/fail assertions — never vague adjectives like "fast" or "intuitive".
6. **Surface Open Questions (If Any)**:
   - Flag remaining assumptions clearly with owners instead of hiding guesses inside requirements.

## Anti-Patterns (Do Not)

- **DO NOT** write multi-page corporate fluff or repeat the same requirement in 4 sections.
- **DO NOT** use untestable acceptance criteria ("UI looks modern", "system handles errors gracefully", "loads quickly").
- **DO NOT** omit **Non-Goals** — unstated scope boundaries cause runaway implementation.
- **DO NOT** invent existing endpoints, tables, or UI routes without verifying them in the codebase.
- **DO NOT** embed deep implementation code inside a PRD; specify contracts and behavior, leaving coding tasks to `project-planner`.

## Spec Template

```markdown
# Feature Spec: <Feature Name>

## 1. Problem & Context
<2-3 sentences explaining the problem and context in this codebase.>

## 2. Goals & Non-Goals
- **Goals:** ...
- **Non-Goals:** ...

## 3. User / System Flows
1. ...

## 4. Functional Requirements & Contracts
- **FR-1**: ...

## 5. Non-Functional & Security Constraints
- Auth/Permissions, Latency/Throughput targets, Data retention, Observability.

## 6. Edge Cases & Failure Modes
| Scenario | Expected Behavior |
|---|---|
| ... | ... |

## 7. Acceptance Criteria
- [ ] **Given** ..., **When** ..., **Then** ...

## 8. Open Questions
- None (or explicit items needing decision).
```

## Reference Files

- For the full copy-ready spec template with actors, contracts, and NFR prompts, see [prd-template.md](references/prd-template.md).

## Examples

### Example: Rate-Limited Coupon Redemption Spec
**Input:**
> "Viết spec ngắn gọn cho tính năng áp mã giảm giá khi checkout: mỗi user dùng 1 lần/mã, mã có hạn dùng và giới hạn lượt toàn hệ thống."

**Output:**
```markdown
# Feature Spec: Checkout Coupon Redemption

## 1. Problem & Context
Users currently cannot apply promotional discount codes during checkout. We need server-validated coupon redemption integrated with `POST /api/orders` while preventing race-condition over-redemption.

## 2. Goals & Non-Goals
- **Goals:** Validate coupon eligibility server-side, apply percentage or fixed-amount discounts, and enforce global + per-user usage limits atomically.
- **Non-Goals:** Stackable coupons (max 1 per order), admin CRUD UI, automatic cart-level recommendations.

## 3. User / System Flows
1. User submits coupon code in checkout → server previews discounted total via `POST /api/coupons/preview`.
2. User confirms order via `POST /api/orders` with `couponCode` → server validates, atomically increments `used_count`, inserts `coupon_redemptions(coupon_id, user_id, order_id)`, and stores final discounted total on the order.

## 4. Functional Requirements & Contracts
- **FR-1:** Coupon code lookup is case-insensitive (`TRIM` + uppercase normalized).
- **FR-2:** Discount calculation supports `PERCENT` (`1..100`, rounded down to nearest integer minor unit) and `FIXED_AMOUNT` (clamped so final payable total >= `0`).
- **FR-3:** Global limit (`used_count < max_uses`) and per-user uniqueness `(coupon_id, user_id)` must be enforced inside a single DB transaction.

## 5. Non-Functional & Security Constraints
- Authenticated user required; return generic `400 COUPON_INVALID` for expired, exhausted, or nonexistent codes? Wait: distinguish `COUPON_EXPIRED`, `COUPON_LIMIT_REACHED`, `COUPON_ALREADY_USED` only for authenticated checkout; rate-limit preview endpoint to 20 req/min/user to block brute-force enumeration.

## 6. Edge Cases & Failure Modes
| Scenario | Expected Behavior |
|---|---|
| Two concurrent requests claim last remaining slot | DB atomic conditional update (`used_count < max_uses`) lets exactly 1 succeed; second receives `409 COUPON_LIMIT_REACHED`. |
| Order payment creation fails after redemption | Transaction rolls back `used_count` and `coupon_redemptions` row. |
| Fixed discount exceeds cart subtotal | Discount clamped to cart subtotal; order total becomes `0`. |

## 7. Acceptance Criteria
- [ ] **Given** a valid coupon with 1 slot left and 2 concurrent order requests, **When** both execute simultaneously, **Then** exactly 1 order succeeds and the other fails with `409`.
- [ ] **Given** a user who already redeemed `SAVE20`, **When** they apply `save20` again, **Then** checkout rejects with `409 COUPON_ALREADY_USED`.
```
