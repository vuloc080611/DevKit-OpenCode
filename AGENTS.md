# AGENTS.md — DevKit OpenCode Engineering Rules

This repository / workspace uses **DevKit OpenCode** (`devkit-opencode`), a disciplined 24-skill workflow covering the full software development lifecycle from planning and implementation to verification, review, web/backend engineering, and learning.

## 1. Core Engineering Discipline

1. **Clarify Before Building (`grill-me` → `spec-writer` → `project-planner`)**
   - When requirements are ambiguous, underspecified, or touch critical architecture, ask focused questions before writing code.
   - Break non-trivial work into small, verifiable tasks with clear acceptance criteria.
2. **Test-First & Incremental Delivery (`tdd-workflow`, `incremental-implementation`)**
   - Prefer Red-Green-Refactor: write a failing test first, verify it fails for the expected reason, write minimal code to pass, then refactor.
   - Deliver in small vertical slices rather than sprawling unverified diffs.
3. **Evidence-Based Debugging (`systematic-debugging`)**
   - Never guess or apply random fixes. Reproduce → collect logs/traces → state 1 explicit hypothesis → verify → fix root cause → add regression test.
4. **Verify Before Claiming Done (`verification-before-done`)**
   - Never claim a task is fixed, complete, or passing unless you ran the relevant test/build/lint commands *after* your final edit and directly observed the output.
   - Report exact commands run and actual results; state clearly what was not verified.
5. **No Hallucinated Facts**
   - Only reference files, symbols, APIs, dependency versions, and command outputs you actually inspected in the workspace or tool output.
6. **Language Matching**
   - Respond in the language the user uses (e.g., Vietnamese or English) while keeping code identifiers, commit tags, and technical terms accurate.

---

## 2. Skill Routing Guide (24 Skills)

Load the matching skill whenever the user's request falls into its domain:

### A. Planning & Requirements
- **`grill-me`**: Feature is vague, large, or has unstated edge cases/constraints. Interrogate requirements before coding.
- **`spec-writer`**: Need a crisp PRD, feature spec, user stories, or acceptance criteria.
- **`project-planner`**: Need a sequenced implementation plan, task breakdown, dependencies, and per-task verification steps.
- **`architecture-decision`**: Choosing between tech stacks, patterns, databases, or structural trade-offs (produces an ADR).

### B. Implementation Discipline
- **`tdd-workflow`**: Implementing features or bug fixes using strict Red-Green-Refactor test-driven development.
- **`incremental-implementation`**: Executing multi-step changes in small, safe, testable slices with clean checkpoints.
- **`systematic-debugging`**: Investigating bugs, crashes, flaky tests, regressions, or unexpected runtime behavior.
- **`verification-before-done`**: Final pre-completion gate before saying "done", opening a PR, or reporting success.

### C. Code Quality & Review
- **`code-review`**: Reviewing diffs, PRs, or modules for correctness, edge cases, maintainability, and test coverage.
- **`security-review`**: Auditing auth, authorization, input validation, SQLi/XSS/SSRF, secrets, and dependencies.
- **`performance-review`**: Profiling and fixing latency, N+1 queries, memory growth, bundle bloat, or algorithmic bottlenecks.
- **`refactor-safe`**: Restructuring existing code without changing external behavior, guarded by tests.
- **`code-simplification`**: Removing over-engineering, dead abstractions, deep nesting, and duplication.

### D. Daily Dev Tools
- **`git-commit`**: Crafting accurate Conventional Commit messages from real staged/working diffs.
- **`changelog-generator`**: Generating release changelogs from git commit history/tags.
- **`readme-generator`**: Writing or updating an accurate `README.md` grounded in the real codebase.
- **`docs-writer`**: Writing docstrings, API guides, architecture docs, or operational runbooks.

### E. Web & Backend
- **`api-designer`**: Designing REST or GraphQL endpoints, schemas, error formats, pagination, and auth contracts.
- **`database-schema`**: Designing tables, relationships, constraints, indexes, and safe migrations.
- **`frontend-component`**: Building clean, accessible, responsive UI components without generic AI look.
- **`docker-setup`**: Writing optimized multi-stage `Dockerfile`s and `compose.yaml` configurations.

### F. Student & Learning
- **`dsa-explainer`**: Explaining data structures and algorithms with intuition, step-by-step trace, and Big-O proof.
- **`leetcode-helper`**: Guided hints, approach breakdown, and edge cases for coding problems without instant spoilers.
- **`assignment-helper`**: Mentoring students on coursework, projects, and technical reports ethically and systematically.

---

## 3. Repository Conventions

- Skills live in `skills/<skill-name>/SKILL.md` (with optional `references/` subdirectories) and can be installed to `.opencode/skills/` or `~/.config/opencode/skills/`.
- Custom OpenCode slash commands live in `commands/*.md` (and can be installed to `.opencode/commands/` or `~/.config/opencode/commands/`).
- Every `SKILL.md` follows the OpenCode Agent Skills format (`name`, `description` <= 1024 chars, `compatibility: opencode`, step-by-step workflow, anti-patterns, and input/output examples).
- Run `python scripts/validate.py` before committing changes to skills, commands, configs, or documentation.
- Never bypass failing checks, suppress linter/type errors without cause, or commit secrets/credentials.
