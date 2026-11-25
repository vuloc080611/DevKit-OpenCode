---
description: Craft an accurate Conventional Commit from staged or working git diffs (git-commit)
agent: build
---

Load and follow the `git-commit` skill.

Optional user note or scope hint:
$ARGUMENTS

Inspect `git status --short`, `git diff --staged`, `git diff`, and `git log -n 10 --oneline`. Warn if secrets or unrelated concerns are mixed, and craft a clean Conventional Commit message grounded strictly in the real diff.
