---
name: changelog-generator
description: Use whenever preparing a release, summarizing git history between tags/commits, or updating CHANGELOG.md ("tạo changelog", "release notes", "tổng hợp commit", "prepare release"). Produces Keep-a-Changelog notes from real git log history, handling breaking changes (`!`), monorepo paths, and untagged repos.
license: MIT
compatibility: opencode
metadata:
  category: devtools
  audience: developers
  version: "1.0.0"
---

# Changelog Generator — Release Notes from Real Git History

Produce accurate, user-focused release notes directly from `git log` commit ranges, filtering internal noise and highlighting breaking changes.

## When to Use

- Preparing a tagged release (`v1.2.0`), updating `CHANGELOG.md`, or summarizing changes between two refs (`v1.1.0..HEAD`, `main..feature`).
- **Do NOT use** to invent unreleased features not present in git history.

## Step-by-Step Workflow

1. **Determine Commit Range & Existing Style**:
   - Inspect existing `CHANGELOG.md` (if present) to match version headings, comparison link format, and release date style.
   - Check tags (`git tag --sort=-v:refname`) and determine exact range (`<last-tag>..HEAD`; if no tags exist yet, inspect full commit history from root). For monorepos, scope by package path (`git log <range> -- packages/<name>`).
2. **Read Actual Commits (and Merge PRs)**:
   - Run `git log <range> --pretty=format:"%h|%ad|%s|%b" --date=short` (or `--no-merges` where appropriate).
   - Inspect diff/commit bodies for any commit marked `<type>!:` or `BREAKING CHANGE:`.
3. **Filter & Categorize for End Users**:
   - Map commits into standard **Keep a Changelog** sections:
     - **Breaking Changes** (surface at top with migration steps!)
     - **Added** (`feat`)
     - **Changed** (behavior updates, `perf`, impactful `refactor`)
     - **Deprecated**
     - **Removed**
     - **Fixed** (`fix`)
     - **Security** (security fixes / CVEs)
   - Omit noisy internal-only commits (`chore: fmt`, `style: prettier`, `wip`, typo fixes in comments) unless user asks for a raw full commit dump.
4. **Rewrite Entries in Clear Outcome Language**:
   - Describe what changed for users/developers (include commit hash / PR ref if repo uses them), rather than pasting cryptic internal commit fragments.
5. **Write/Update `CHANGELOG.md` & Verify Links**:
   - Preserve prior version entries intact; prepend the new release (or `[Unreleased]` section) cleanly.

## Anti-Patterns (Do Not)

- **DO NOT** fabricate commits, PR numbers, dates, or contributors not present in `git log`.
- **DO NOT** paste raw `wip`, `fix typo`, `merge branch main` noise into user-facing release notes.
- **DO NOT** bury breaking changes inside regular bullets — always highlight them with migration guidance.
- **DO NOT** overwrite older release sections in `CHANGELOG.md`.

## Output Template

```markdown
## [vX.Y.Z] - YYYY-MM-DD

### Breaking Changes
- **<Area>**: <What broke> — **Migration:** <exact action needed>

### Added
- ...

### Changed
- ...

### Fixed
- ...

### Security
- ...
```

## Examples

### Example: Generating v1.4.0 Release Notes from `v1.3.0..HEAD`
**Input:**
> "Tạo changelog cho bản `v1.4.0` từ tag `v1.3.0` đến `HEAD`."

**Output (grounded in `git log v1.3.0..HEAD`):**
```markdown
## [v1.4.0] - 2026-11-25

### Breaking Changes
- **Auth Config:** Startup now fails fast if `JWT_SECRET` is unset or shorter than 32 characters (previously fell back to a dev default). **Migration:** Ensure `JWT_SECRET` (>= 32 chars) is set in `.env` / production secrets before deploying (`a1b2c3d`).

### Added
- **Checkout Coupons:** Added `POST /api/coupons/preview` and atomic `couponCode` redemption inside `POST /api/orders` with per-user and global usage limits (`d4e5f6g`).
- **Docker:** Added multi-stage production `Dockerfile` running as non-root user (`h7i8j9k`).

### Fixed
- **Product Search:** Fixed 500 error on `GET /api/products?q=` caused by coercing empty query strings to `undefined` (`l0m1n2o`).
- **Orders API:** Eliminated N+1 item queries in `GET /api/orders`, cutting 200-order response time from ~1.7s to <50ms in local benchmarks (`p3q4r5s`).
```
