---
name: api-designer
description: Design clean, consistent, production-ready REST or GraphQL APIs including resource modeling, HTTP methods and status codes, pagination/filtering, validation schemas, idempotency, structured error envelopes, versioning, and auth contracts. Use when designing API endpoints or OpenAPI/GraphQL schemas ("thiết kế API", "RESTful design", "OpenAPI", "GraphQL schema").
license: MIT
compatibility: opencode
metadata:
  category: web-backend
  audience: developers
  version: "1.0.0"
---

# API Designer — Consistent REST & GraphQL Contracts

Design predictable, evolvable API contracts that frontend/mobile clients and backend services can integrate against cleanly without breaking surprises.

## When to Use

- Designing new REST endpoints, GraphQL schemas/mutations, or webhook contracts.
- Standardizing inconsistent API error shapes, pagination, or status codes across an existing service.
- **Do NOT use** for DB table/index modeling (pair with `database-schema`) or security audits of existing implementations (use `security-review`).

## Step-by-Step Workflow

1. **Inspect Existing API Conventions First**:
   - Check existing routes, OpenAPI/Swagger specs, GraphQL SDL, error shapes, auth headers, and naming conventions (`camelCase` vs `snake_case`) so new endpoints match seamlessly.
2. **Model Resources & Operations**:
   - **REST:** Plural nouns (`/v1/orders`, `/v1/orders/{orderId}/items`), proper HTTP semantics (`GET` safe, `PUT` idempotent replace, `PATCH` partial update, `POST` create/action, `DELETE` remove), accurate status codes (`200`, `201` + `Location`, `204`, `400`, `401`, `403`, `404`, `409`, `422`, `429`).
   - **GraphQL:** Domain-oriented types, Relay/connection pagination or explicit `PageInfo`, input object types per mutation, explicit union/payload error types, **DataLoader batching** to prevent N+1 resolver loops, and query depth/complexity caps.
   - **Webhooks & Async Events:** Explicit versioned event envelope (`id`, `type`, `occurredAt`, `data`), HMAC-SHA256 signature + timestamp header for replay protection, and exponential retry + idempotent consumer semantics.
3. **Standardize Cross-Cutting Contracts**:
   - **Pagination:** Keyset/cursor pagination (`cursor`, `limit`) for large/live feeds; offset (`page`, `pageSize`) only when bounded/small. Always cap `limit` (e.g., max 100).
   - **Filtering & Sorting:** Explicit allowlisted query params (`?status=paid&sort=-createdAt`) — never expose raw SQL/ORM filter objects directly.
   - **Idempotency & Concurrency:** `Idempotency-Key` header for payment/order creation; `ETag` / `If-Match` or version field when concurrent updates could clobber state.
   - **Structured Error Envelope (e.g., RFC 9457):** Consistent `{ type/code, message, details?, requestId }` — never leak stack traces or internal SQL errors.
4. **Define Security, Rate Limits & Versioning**:
   - Specify auth requirement (Bearer JWT, API Key, public), role/ownership rules, rate-limit headers, and non-breaking evolution strategy (additive fields; path/header versioning only on breaking changes).
5. **Deliver Concrete Contract Examples**:
   - Provide endpoint table, request/response JSON (or OpenAPI/GraphQL SDL), validation constraints, and error examples.

## Anti-Patterns (Do Not)

- **DO NOT** invent RPC-style verbs in REST URLs (`/api/getUserById`, `/api/deleteOrder`) when standard resource routes fit cleanly.
- **DO NOT** return HTTP `200 OK` with `{ "success": false, "error": "Unauthorized" }`.
- **DO NOT** return unbounded arrays from list endpoints without pagination and a max page-size cap.
- **DO NOT** expose internal auto-increment secrets, PII, password hashes, or raw DB constraint exceptions in responses.
- **DO NOT** mix `camelCase` and `snake_case` randomly within the same API surface.

## Output Template

```markdown
## API Contract: <Domain / Feature>
- **Base & Versioning:** `/api/v1/...`
- **Auth & Rate Limit:** ...

### Endpoints
| Method & Path | Purpose | AuthZ | Status Codes |
|---|---|---|---|
| ... | ... | ... | ... |

### Request / Response Schemas & Examples
...

### Error Envelope Standard
...
```

## Examples

### Example: Designing an Idempotent Order Cancellation & List API
**Input:**
> "Thiết kế REST API cho tính năng quản lý đơn hàng (list có filter/pagination, xem chi tiết, hủy đơn hàng)."

**Output:**
> - **List Orders:** `GET /api/v1/orders?status=PENDING,PAID&cursor=ord_01J&limit=20&sort=-createdAt`
>   - `200 OK`: `{ "data": [...], "pagination": { "nextCursor": "ord_02K", "hasMore": true } }` (`limit` capped at `100`).
> - **Get Order:** `GET /api/v1/orders/{orderId}`
>   - `200 OK` (owner or admin), `403` (other user), `404` (not found).
> - **Cancel Order:** `POST /api/v1/orders/{orderId}/cancellations` (supports `Idempotency-Key` header)
>   - Request: `{ "reason": "CHANGED_MIND", "note": "Ordered wrong size" }`
>   - Responses: `200 OK` (updated order; repeated call with same key returns same `200`), `409 Conflict` (`ORDER_ALREADY_SHIPPED` when state transition invalid).
> - **Error Format:** `{ "code": "ORDER_ALREADY_SHIPPED", "message": "Cannot cancel an order after shipment.", "requestId": "req_9f82a" }`.
