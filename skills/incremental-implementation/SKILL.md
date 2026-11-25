---
name: incremental-implementation
description: Execute features or multi-file changes in small, independently verifiable vertical slices with frequent clean checkpoints instead of giant speculative edits. Use when implementing a plan, building multi-layer features, or migrating subsystems safely ("làm từng bước nhỏ", "incremental", "vertical slice").
license: MIT
compatibility: opencode
metadata:
  category: implementation
  audience: developers
  version: "1.0.0"
---

# Incremental Implementation — Small Verifiable Slices

Build complex changes through thin, working increments where each slice compiles, passes checks, and leaves the repository in a clean, deployable state.

## When to Use

- Executing an approved `project-planner` roadmap or multi-file feature.
- Integrating backend, database, and frontend layers without breaking the build mid-way.
- **Do NOT use** as an excuse to skip tests (pair each slice with `tdd-workflow` and `verification-before-done`).

## Step-by-Step Workflow

1. **Confirm Baseline Green State**:
   - Before touching files, run existing tests/build/typecheck (or `git status`) to verify whether the starting tree is clean and passing.
2. **Select the Next Minimal Vertical Slice**:
   - Choose a slice small enough to inspect and verify in a single pass (typically 1-3 closely coupled files).
   - Ensure the slice either adds a complete thin behavior end-to-end or lands behind a safe boundary (feature flag, new non-breaking helper) without breaking callers.
3. **Implement & Verify Immediately**:
   - Apply the change (following `tdd-workflow` for logic).
   - Run targeted tests, typecheck, and linter immediately after the slice — do not stack Slice 2 on top of broken Slice 1.
4. **Checkpoint Progress**:
   - Summarize what changed and what verification passed.
   - If the user wants incremental commits, suggest or create an atomic commit (`git-commit`) per verified slice.
5. **Continue Slice by Slice**:
   - Only proceed to the next slice once the current slice is verified green.

## Anti-Patterns (Do Not)

- **DO NOT** rewrite 12 files across UI, API, and DB in one unverified giant edit before running a single build or test.
- **DO NOT** move on to the next task while tests or typechecks are failing ("I'll fix the types at the end").
- **DO NOT** leave half-wired dead code, commented-out blocks, or `TODO: implement later` stubs in critical paths.
- **DO NOT** mix unrelated cleanups or formatting churn into a feature slice (keep diffs tight and reviewable).

## Slice Checkpoint Template

```markdown
### Slice <N>: <Short Name>
- **Changed:** `fileA`, `fileB`
- **Verified:** `<command>` → `<result>`
- **Next:** Slice <N+1> (<brief description>)
```

## Examples

### Example: Implementing User Profile Avatar Upload Incrementally
**Input:**
> "Thực hiện feature upload avatar cho user (validate file, lưu S3/local storage, update DB, UI button)."

**Output Plan & Execution Cadence:**
> **Baseline:** Ran `npm test` → `24 passed`. Working tree clean.
>
> **Slice 1 — Storage validation & adapter (`src/lib/avatar-storage.ts`, `tests/avatar-storage.test.ts`):**
> - Implement MIME/size validation (`png/jpeg/webp <= 2MB`) and local disk/S3 abstraction.
> - Verify: `npx vitest run tests/avatar-storage.test.ts` → `5 passed`.
>
> **Slice 2 — API endpoint (`src/routes/profile.ts`, `tests/profile-avatar.test.ts`):**
> - Wire `PATCH /api/me/avatar` with auth check + storage call + DB URL update.
> - Verify: `npx vitest run tests/profile-avatar.test.ts` & `npm run typecheck` → passed.
>
> **Slice 3 — UI control (`src/components/AvatarUploader.tsx`):**
> - Add accessible file input, preview, loading/error states wired to `PATCH /api/me/avatar`.
> - Verify: `npm run build` & `npm test` → passed.
