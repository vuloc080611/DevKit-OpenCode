---
name: architecture-decision
description: Use whenever choosing between technologies, databases, queues, auth patterns, or system boundaries ("A vs B", "should we use", "migrate from X to Y", "viết ADR", "so sánh kiến trúc", "trade-offs"). Produces an objective Architecture Decision Record with constraints, real options including status quo, ops cost, and exit triggers.
license: MIT
compatibility: opencode
metadata:
  category: planning
  audience: developers
  version: "1.0.0"
---

# Architecture Decision — Structured ADR Authoring

Document important technical decisions rigorously so teams understand *why* a choice was made, what alternatives were rejected, and what consequences follow.

## When to Use

- Choosing between databases, queues, auth architectures, monolith vs microservices, rendering strategies, or major libraries.
- Resolving technical disagreements across competing approaches.
- Recording an architectural shift in `docs/adr/` (or `docs/decisions/`).
- **Do NOT use** for trivial local library picks (e.g., utility helper) or product feature specs (use `spec-writer`).

## Step-by-Step Workflow

1. **Inspect Current Constraints & Context**:
   - Read existing project dependencies, infra setup, team/scale profile, and pain points.
   - Clarify drivers: scale, latency, team familiarity, operational complexity, budget, and timeline.
2. **Frame the Decision Problem**:
   - State the single architectural question being answered and the forcing factors (constraints that rule options in or out).
3. **Evaluate 2-4 Genuine Options (Including Status Quo)**:
   - Always include **"Keep / Evolve Current Setup (Status Quo)"** as a baseline option unless clearly impossible — never assume a shiny new tool beats extending existing infra.
   - Compare real viable alternatives fairly — never construct strawman options just to justify a preset preference.
   - Analyze each across concrete criteria: Complexity, Performance/Scale fit, Failure Blast Radius, Cost/Ops & On-Call burden, Lock-in / Reversibility.
4. **Make & Justify the Decision**:
   - State the chosen option clearly, tying the choice directly to the project's primary drivers.
5. **Document Consequences & Exit Strategy**:
   - List positive consequences, accepted downsides/tech debt, required follow-up work, and what signal would trigger revisiting this decision.

## Anti-Patterns (Do Not)

- **DO NOT** compare a favorite option against obviously weak strawmen.
- **DO NOT** list generic pros/cons detached from the project's actual constraints (e.g., praising "handles 1M RPS" for an internal admin tool).
- **DO NOT** hide negative consequences — every architectural choice has costs; name them honestly.
- **DO NOT** write a 10-page essay; keep an ADR crisp enough to review in 5 minutes.
- **DO NOT** invent benchmark numbers you did not measure or cite.

## ADR Template

```markdown
# ADR-NNN: <Short Decision Title>

- **Status:** Proposed | Accepted | Superseded by ADR-XXX
- **Date:** YYYY-MM-DD
- **Decision Drivers:** <Key constraints & goals>

## Context
<What problem or architectural tension requires a decision now?>

## Options Considered
### Option 1: <Name>
- **Pros:** ...
- **Cons / Risks:** ...
- **Reversibility:** High / Medium / Low

### Option 2: <Name>
...

## Comparison Summary
| Criterion | Option 1 | Option 2 |
|---|---|---|
| Complexity | ... | ... |
| Ops Overhead | ... | ... |
| Reversibility | ... | ... |

## Decision
We choose **<Option X>** because <direct link to decision drivers>.

## Consequences
- **Positive:** ...
- **Negative / Accepted Trade-offs:** ...
- **Follow-up Actions:** ...
- **Revisit Trigger:** <Condition that invalidates this choice>
```

## Examples

### Example: Background Job Processing Choice
**Input:**
> "Team đang cân nhắc giữa Postgres-backed queue (pg-boss) vs Redis + BullMQ cho hệ thống gửi email & xuất báo cáo (~5,000 jobs/ngày) hiện đã có PostgreSQL."

**Output:**
```markdown
# ADR-004: Use PostgreSQL-Backed Job Queue (`pg-boss`) Instead of Redis + BullMQ

- **Status:** Proposed
- **Date:** 2026-11-25
- **Decision Drivers:** Small 3-person team, existing PostgreSQL instance, ~5,000 jobs/day, low infra budget, transactional job enqueueing needed on order events.

## Context
Email notifications and async CSV report exports currently block HTTP request threads. The stack runs Node.js + PostgreSQL with no Redis instance in production.

## Options Considered

### Option 1: `pg-boss` on Existing PostgreSQL
- **Pros:** Zero new infrastructure to provision, monitor, or back up; supports transactional enqueueing alongside business DB writes; built-in retries and dead-letter handling.
- **Cons / Risks:** Adds polling/write load to primary PostgreSQL; unsuitable if throughput grows into tens of thousands of jobs/sec.
- **Reversibility:** High (behind an internal `JobQueue` interface).

### Option 2: Redis + BullMQ
- **Pros:** Very low latency, high throughput, rich dashboard ecosystem, designed natively for high-volume queues.
- **Cons / Risks:** Requires provisioning/securing Redis persistence, failover, and monitoring; dual-write risk between Postgres commit and Redis enqueue without an outbox pattern.
- **Reversibility:** Medium.

## Decision
Choose **Option 1 (`pg-boss`)** behind an internal `QueueService` abstraction. At ~5,000 jobs/day (< 1 job/sec average), eliminating Redis ops overhead and gaining transactional safety outweighs BullMQ's peak-throughput advantage.

## Consequences
- **Positive:** Faster delivery, simpler staging/local Docker setup, atomic job scheduling with DB transactions.
- **Negative / Accepted Trade-offs:** Must monitor Postgres table bloat/autovacuum on `pgboss` schema and keep heavy report payloads out of job JSON columns.
- **Revisit Trigger:** Queue latency exceeds SLA (> 5s pickup delay) or volume surpasses ~500 jobs/min sustained.
```
