---
name: verification-before-done
description: Enforce a mandatory verification gate before claiming any task, bug fix, refactor, or feature is complete. Requires running actual tests, linters, typechecks, and edge-case checks after the final edit and reporting observed output verbatim. Use before finishing any coding task ("kiểm tra xong chưa", "verify before done", "ready to merge").
license: MIT
compatibility: opencode
metadata:
  category: implementation
  audience: developers
  version: "1.0.0"
---

# Verification Before Done — Evidence Over Assumptions

Never declare victory based on intuition, stale test runs, or partial checks. Evidence from commands run **after your final edit** is the sole basis for claiming completion.

## When to Use

- Immediately before telling the user a feature is finished, a bug is fixed, a refactor is safe, or a PR/commit is ready.
- Whenever handing off completed work to another developer or agent.
- **Always active** as the final gate after `tdd-workflow`, `incremental-implementation`, `systematic-debugging`, or `refactor-safe`.

## Step-by-Step Verification Gate

1. **Inspect Final State (`git status` / `git diff`)**:
   - Confirm no stray debug logs, temp files, unintended edits, or secrets were introduced.
2. **Identify All Required Checks**:
   - Determine what proves correctness in this repo: unit tests, integration tests, typecheck (`tsc --noEmit`, `mypy`, `pyright`), linter, build (`npm run build`), migration check, or live endpoint/CLI execution.
3. **Run Fresh Verification Commands AFTER Final Edit**:
   - Execute each command fresh. Earlier runs before your last edit are **invalid**.
   - Check exit codes AND read full output (watch out for skipped tests, warnings-as-errors, or `0 tests found`).
4. **Verify Edge Cases & Requirements Match**:
   - Cross-check every acceptance criterion or edge case requested by the user against what was actually tested.
5. **Report Accurately & Transparently**:
   - State exact commands executed, scope covered, and observed counts/results.
   - If something could NOT be verified (e.g., no staging DB, external webhook key missing, E2E suite skipped), state that gap explicitly instead of claiming full verification.

## Anti-Patterns (Do Not)

- **DO NOT** say "All tests pass", "Fixed!", or "Works as expected" without running tests after your very last edit.
- **DO NOT** cite "should pass", "looks good by inspection", or "it passed earlier" as verification.
- **DO NOT** report a single filtered unit test file (`vitest run foo.test.ts`) as "the whole test suite passes".
- **DO NOT** hide skipped tests (`it.skip`), relaxed assertions, or mocked-out checks as full behavioral proof.
- **DO NOT** ignore compiler warnings, typecheck errors, or failing lint rules unless explicitly out of scope and disclosed.

## Iron Rule

> **No fresh execution output = no completion claim. State exactly what ran, what passed, what failed, and what remains unverified.**

## Verification Summary Template

```markdown
## Verification Summary
- **Files Changed:** `path/to/file1`, `path/to/file2`
- **Checks Executed (post-final-edit):**
  - `<command 1>` → `<exact observed result, e.g. 42 passed, 0 failed>`
  - `<command 2>` → `<exact observed result>`
- **Edge Cases Confirmed:** <list>
- **Not Verified / Limitations:** <None, or exact gap e.g. "Prod SMTP delivery not tested; verified console fallback in dev">
```

## Examples

### Example 1: Honest Verification Report (With Explicit Scope)
**Input:**
> "Xong bug fix reset password chưa bạn?"

**Output:**
> Đã hoàn tất sửa lỗi và chạy kiểm tra sau lần edit cuối cùng:
> - **Checks đã chạy:**
>   - `npx vitest run tests/auth/reset-password.test.ts` → `11 passed (11)` (bao gồm expired token, reused token, unknown email).
>   - `npm run typecheck` → exit code `0`, không có lỗi TypeScript.
>   - `npm run lint` → exit code `0`.
> - **Chưa kiểm tra:** Email thật qua Resend API (chưa có `RESEND_API_KEY` trong môi trường local; đã verify console fallback khi `NODE_ENV=test`).

### Example 2: Catching an Incomplete State Before Claiming Done
**Input:**
> (Agent fixed a CSS bug in `Button.tsx` and is about to reply "Done!")

**Self-Check Output:**
> Caught before claiming done: `npm run build` failed with `TS2322` in `src/pages/Home.tsx:18` because `variant="ghost"` was removed from `ButtonProps`. Fixing caller in `Home.tsx`, re-running `npm run build` and `npm test`, and only then reporting completion.
