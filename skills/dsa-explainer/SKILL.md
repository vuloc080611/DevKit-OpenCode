---
name: dsa-explainer
description: Explain general data structures and algorithms from first principles with intuition, step-by-step dry-run trace, time and space complexity proof, common pitfalls, and clean reference code. Use when learning or reviewing DSA concepts ("giải thích thuật toán", "cấu trúc dữ liệu", "Big-O", "how does Dijkstra/BFS/DP work"). For progressive non-spoil coding problem hints, use leetcode-helper.
license: MIT
compatibility: opencode
metadata:
  category: learning
  audience: students-and-developers
  version: "1.0.0"
---

# DSA Explainer — Intuition, Step-by-Step Trace & Complexity

Build genuine understanding of data structures and algorithms — never dump bare code or memorize-only definitions.

## When to Use

- Explaining algorithms (BFS/DFS, Dijkstra, Union-Find, Binary Search, Dynamic Programming, Sliding Window, Topological Sort, KMP) or data structures (Heap, Trie, Segment Tree, Hash Table).
- Comparing trade-offs between two data structures or proving why a time/space complexity holds.
- **Do NOT use** when the user wants progressive interview hints without spoiling a specific LeetCode problem (use `leetcode-helper`).

## Step-by-Step Workflow

1. **Identify Learner Level & Preferred Language**:
   - Adapt explanation depth to the user's question (beginner vs interview prep) and preferred programming language (default Python/C++/TypeScript/Java based on context).
2. **Start with Core Problem & Intuition (Why Does It Exist?)**:
   - State the problem the data structure/algorithm solves and the key mental model ("one sentence AHA idea") before mathematical notation.
3. **Trace Step-by-Step on a Small Concrete Example**:
   - Walk through a 4-6 element or 4-5 node trace table/diagram showing exact state changes at each step so the mechanics click visually.
4. **Analyze Time & Space Complexity (And Why)**:
   - Explain *how* the Big-O bound arises (e.g., "each element enters and leaves the monotonic deque at most once → $O(n)$", not just asserting "$O(n)$").
   - Cover Best / Average / Worst cases and auxiliary space vs total space when relevant.
5. **Provide Clean, Annotated Reference Code + Common Pitfalls**:
   - Keep code idiomatic, readable, and tested mentally against edge cases (empty input, duplicates, negative weights, disconnected graphs, overflow).
6. **Check Understanding & Pattern Signals**:
   - Summarize "When to recognize this pattern in the wild" using input/constraint signals (e.g., *"sorted/monotonic property → Binary Search; next greater/smaller → Monotonic Stack; unweighted shortest path → BFS; weighted non-negative → Dijkstra"*) and offer a small follow-up variation question.

## Anti-Patterns (Do Not)

- **DO NOT** paste code first with zero intuition or dry-run trace.
- **DO NOT** state Big-O complexity without explaining *why* it holds (especially amortized or $O(V + E)$ vs $O((V + E)\log V)$ nuances).
- **DO NOT** skip failure boundaries (e.g., forgetting to mention Dijkstra breaks on negative edge weights, or binary search requiring monotonicity).
- **DO NOT** overwhelm beginners with esoteric optimizations before the core idea is solid.

## Output Template

```markdown
## 1. Ý tưởng cốt lõi (Core Intuition)
<Simple mental model & problem solved>

## 2. Minh họa từng bước (Step-by-Step Trace)
<Small 4-6 item trace showing state transitions>

## 3. Độ phức tạp (Time & Space Complexity)
- **Time:** <Big-O + concise derivation>
- **Space:** <Big-O + auxiliary breakdown>

## 4. Code mẫu sạch (Reference Code)
<Idiomatic, concise, edge-case-safe implementation>

## 5. Lỗi hay gặp & Khi nào áp dụng
- Pitfall 1...
- When to use...
```

## Examples

### Example: Explaining Monotonic Stack ("Next Greater Element")
**Input:**
> "Giải thích thuật toán Monotonic Stack (ngăn xếp đơn điệu) qua bài Next Greater Element bằng Python."

**Output Highlights:**
> 1. **Intuition:** Instead of scanning right from every element ($O(n^2)$), keep a stack of indices still *waiting* for a larger number to their right. As soon as a bigger element arrives, it resolves every smaller element waiting on top of the stack.
> 2. **Trace on `[2, 1, 5, 3]`:**
>    - `i=0 (val=2)`: stack `[0(2)]`
>    - `i=1 (val=1)`: `1 <= 2`, push → stack `[0(2), 1(1)]`
>    - `i=2 (val=5)`: `5 > 1` → ans[1]=5, pop; `5 > 2` → ans[0]=5, pop; push → stack `[2(5)]`
>    - `i=3 (val=3)`: `3 <= 5`, push → stack `[2(5), 3(3)]` → remaining stay `-1` → Result `[5, 5, -1, -1]`.
> 3. **Complexity:** Time $O(n)$ because each index is pushed once and popped at most once (`<= 2n` stack ops total). Space $O(n)$ for the stack + output.
> 4. **Clean Python code + Pitfall note** (storing indices instead of values so duplicates & distance calculations work cleanly).
