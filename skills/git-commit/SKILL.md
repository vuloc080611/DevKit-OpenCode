---
name: git-commit
description: Use whenever committing code, reviewing staged/working changes before commit, writing a Conventional Commit message, or splitting mixed edits ("viết commit message", "git commit", "stage and commit", "split commits", "conventional commit"). Scans diffs for accidental secrets/debug logs and crafts accurate why-focused messages.
license: MIT
compatibility: opencode
metadata:
  category: devtools
  audience: developers
  version: "1.0.0"
---

# Git Commit — Smart Conventional Commits from Real Diffs

Craft clean, accurate commit messages grounded strictly in the actual diff (`git diff --staged`), never vague guesses like `"update files"`.

## When to Use

- Preparing a commit for staged or unstaged changes.
- Splitting mixed changes into clean atomic commits.
- Standardizing commit history under Conventional Commits (`feat`, `fix`, `refactor`, `docs`, `test`, `chore`, `perf`, `ci`, `build`).

## Step-by-Step Workflow

1. **Inspect Git State & Recent Style**:
   - Run `git status --short`, `git diff --staged`, and (if nothing staged yet) `git diff` to see exact modified files and hunks.
   - Check `git log -n 10 --oneline` to match existing repo conventions (scope naming, imperative style, ticket tags).
2. **Check Commit Atomicity & Pre-Commit Secret Scan**:
   - Scan diff hunks for accidental `.env*`, API tokens (`sk-`, `ghp_`, `AKIA`, `BEGIN PRIVATE KEY`), `console.log`/`print` debug leftovers, or commented-out dead code. Warn and stop before staging if found!
   - If changes mix unrelated concerns across files (or within the same file), recommend splitting into atomic commits (using `git add <file>` or interactive hunk staging `git add -p`).
3. **Select Accurate Type & Scope**:
   - `feat`: new user-facing capability
   - `fix`: bug fix
   - `refactor`: structural change with no external behavior change
   - `perf`: measurable performance improvement
   - `test`: adding or fixing tests only
   - `docs`: documentation only
   - `build` / `ci` / `chore`: build scripts, CI pipelines, maintenance
   - Optional `(scope)`: concise module/area name (e.g., `auth`, `checkout`, `api`, `docker`).
4. **Write Subject + Why-Focused Body**:
   - Subject line: `<type>(<scope>): <imperative summary>` (lowercase, no trailing period, <= 72 chars).
   - Body (when change is non-trivial): explain **why** the change was needed and key behavioral impact, not a line-by-line repeat of the diff.
   - Footer: add `BREAKING CHANGE: <migration note>` or `Refs: #<id>` when applicable.
5. **Confirm Before Committing (Unless Explicitly Asked to Commit Now)**:
   - Present the proposed commit message (and exact files to stage if unstaged). Only run `git commit` if the user wants it executed immediately or `bash` permission allows.

## Anti-Patterns (Do Not)

- **DO NOT** write commit messages without reading `git diff --staged` / `git diff` first.
- **DO NOT** use vague subjects (`fix bug`, `update code`, `wip`, `changes`).
- **DO NOT** use `--no-verify` to bypass pre-commit hooks or linters.
- **DO NOT** stage and commit `.env`, credentials, or large unintended build artifacts.
- **DO NOT** amend or force-push commits (`--amend`, `push --force`) unless explicitly requested on unshared local commits.

## Examples

### Example 1: Non-Trivial Bug Fix Diff
**Input:**
> "Xem staged diff và viết commit message giúp tôi."

**Output:**
```text
fix(auth): prevent null crash on empty search query parameter

Express parses `?q=` as an empty string, which `parseSearchTerm` previously
coerced to `undefined` via `||` before calling `.trim()`. Preserve empty
strings safely and handle repeated array query params without throwing 500.

Closes #142
```

### Example 2: Mixed Unrelated Changes Warning
**Input:**
> "Commit hết mấy file mình vừa sửa nhé." (Diff contains both `src/auth/jwt.ts` bugfix and `README.md` typo fix + accidentally modified `.env.local`)

**Output:**
> Phát hiện `.env.local` nằm trong working tree — không nên stage file secrets. Ngoài ra, 2 thay đổi còn lại thuộc 2 mục đích khác nhau, nên tách thành 2 commit gọn:
> 1. `fix(auth): validate JWT audience claim before accepting token` (`src/auth/jwt.ts`, `tests/auth/jwt.test.ts`)
> 2. `docs(readme): fix local setup command flag` (`README.md`)
>
> Bạn muốn tôi chạy tách 2 commit này (bỏ qua `.env.local`) không?
