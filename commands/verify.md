---
description: Run final verification checks before claiming a task or PR is done (verification-before-done)
agent: build
---

Load and strictly follow the `verification-before-done` skill.

Scope or context to verify:
$ARGUMENTS

Inspect `git status` / `git diff`, run all relevant fresh test, typecheck, lint, and build commands after the latest edit, and report exact commands run, observed results, and any unverified gaps.
