# Feature Spec / Mini-PRD Template

Copy and populate this template when executing `spec-writer`. Remove sections only if genuinely inapplicable and state why.

```markdown
# Feature Spec: <Feature Name>

- **Author / Owner:** <Name or Team>
- **Status:** Draft | In Review | Approved
- **Related Docs:** <Links to ADR, existing API/schema, or ticket>

## 1. Problem & Context
<2-3 sentences: Who is blocked today, what concrete pain exists, and what repo modules are involved.>

## 2. Goals & Non-Goals
- **Goals (Measurable Outcomes):**
  - ...
- **Non-Goals (Explicitly Out of Scope):**
  - ...

## 3. Actors & Permissions
| Actor | Allowed Actions | Auth / Ownership Rule |
|---|---|---|
| ... | ... | ... |

## 4. Core User / System Flows
1. **Happy Path:** ...
2. **Alternate / Retry Flow:** ...

## 5. Functional Requirements & Contracts
- **FR-1:** ...
- **FR-2:** ...

### Data / API Contract Summary
- Inputs & validation rules:
- State transitions (`PENDING -> PAID -> CANCELLED`):
- Outputs & error codes:

## 6. Non-Functional & Security Constraints
- **Latency / Scale:** e.g., p95 < 200ms at 100 RPS
- **Concurrency / Idempotency:** e.g., unique key / DB transaction guard
- **Security / Privacy:** e.g., PII redaction, rate limits, ownership checks
- **Observability:** e.g., structured logs with `requestId`, failure metrics

## 7. Edge Cases & Failure Modes
| Scenario | Trigger | Expected System Behavior |
|---|---|---|
| Empty / missing input | ... | ... |
| Concurrent duplicate request | ... | ... |
| Downstream timeout / failure | ... | ... |

## 8. Acceptance Criteria (Testable)
- [ ] **Given** ..., **When** ..., **Then** ...
- [ ] **Given** ..., **When** ..., **Then** ...

## 9. Open Questions
- [ ] <Question needing user/product decision before Task planning>
```
