---
name: code-simplification
description: Reduce accidental complexity, deep nesting, redundant abstractions, duplicate logic, and over-engineering while keeping exact behavior and clarity intact. Use when code feels bloated, over-abstracted, deeply nested, or hard to read ("đơn giản hóa code", "bớt rườm rà", "remove over-engineering", "simplify"). For cross-module restructuring needing test safety nets first, use refactor-safe.
license: MIT
compatibility: opencode
metadata:
  category: quality
  audience: developers
  version: "1.0.0"
---

# Code Simplification — Clarity Without Over-Engineering

Make code shorter, flatter, and easier for a teammate to understand in 30 seconds — without clever one-liners or behavioral regressions.

## When to Use

- Functions have deep `if/else` pyramids, convoluted boolean flags, or needless indirection layers (e.g., a factory creating a single implementation).
- AI-generated or legacy code has repetitive boilerplate, dead variables, or over-engineered design patterns for a simple problem.
- **Do NOT use** to compress code into unreadable ternary chains or remove defensive checks on untrusted input.

## Step-by-Step Workflow

1. **Verify Existing Behavior & Tests**:
   - Confirm tests cover the target code (or capture expectations before simplifying).
2. **Hunt High-Yield Complexity Sources**:
   - **Deep Nesting:** Replace nested `if/else` trees with early returns / guard clauses.
   - **Boolean & State Noise:** Simplify `if (cond) return true; else return false;` to `return cond;`; replace multi-flag combinations with explicit small states.
   - **Dead / Speculative Abstractions:** Inline single-use wrappers, unused interfaces, redundant pass-through classes, and speculative config flags nobody uses.
   - **Repeated Conditionals:** Replace long `if/elif` chains mapping keys to values with a clean lookup object/table.
   - **Duplication:** Merge near-identical branches into one parameterized helper (only when the abstraction genuinely clarifies intent).
3. **Separate Essential vs Accidental Complexity**:
   - **Keep (Essential):** Explicit input validation, null/finite/bounds guards, auth/ownership checks, currency integer rounding, error context, and non-obvious *why* comments.
   - **Remove (Accidental):** >3 levels of nesting, >4 positional boolean/flag parameters, single-implementation pass-through classes, unused config knobs, and redundant wrappers.
4. **Verify Behavior Unchanged**:
   - Run tests, typecheck, and linter after simplifying (`verification-before-done`).

## Anti-Patterns (Do Not)

- **DO NOT** sacrifice clarity for line count (avoid nested ternaries, cryptic regex golf, or dense functional chains that are harder to debug).
- **DO NOT** delete defensive boundary guards (`null` checks, finite checks, auth checks) in the name of "clean code".
- **DO NOT** force deduplication between two blocks that happen to look superficially similar today but represent independent business concepts likely to diverge.
- **DO NOT** remove useful docstrings or non-obvious *why* comments.

## Simplification Patterns

| Smell | Clean Replacement |
|---|---|
| 4-level nested `if` | Guard clauses with early `return` / `throw` |
| 6-branch `if/else if` mapping codes | Lookup `Record<Key, Value>` / `Map` |
| Single-implementation `BaseFoo -> FooFactory -> FooImpl` | Direct `foo()` module/function |
| Duplicated try/catch setup across 5 handlers | Shared middleware or small helper wrapper |

## Examples

### Example: Flattening Deep Nesting & Replacing Speculative Factory
**Input:**
> "Đoạn code xử lý status notification này vừa lồng nhiều `if`, vừa có class `NotifierFactory` chỉ để tạo đúng 1 notifier. Đơn giản hóa giúp tôi."

**Before:**
```ts
async function sendOrderAlert(order: Order | null, user: User | null) {
  if (order !== null) {
    if (user !== null) {
      if (user.emailEnabled) {
        const notifier = NotifierFactory.create("email");
        if (order.status === "PAID") {
          return notifier.send(user.email, "Order paid");
        } else if (order.status === "SHIPPED") {
          return notifier.send(user.email, "Order shipped");
        } else if (order.status === "CANCELLED") {
          return notifier.send(user.email, "Order cancelled");
        }
      }
    }
  }
  return false;
}
```

**After:**
```ts
const STATUS_SUBJECTS: Partial<Record<OrderStatus, string>> = {
  PAID: "Order paid",
  SHIPPED: "Order shipped",
  CANCELLED: "Order cancelled",
};

async function sendOrderAlert(order: Order | null, user: User | null): Promise<boolean> {
  if (!order || !user?.emailEnabled) return false;
  const subject = STATUS_SUBJECTS[order.status];
  if (!subject) return false;

  return sendEmail(user.email, subject);
}
```
> Verified: Ran `npx vitest run tests/alerts.test.ts` → `6 passed (6)`; behavior identical, 18 lines reduced to 9 readable lines, unused `NotifierFactory` removed after confirming zero other callers.
