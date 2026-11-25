---
description: Perform a severity-ranked multi-dimensional code review (code-review)
agent: plan
---

Load and follow the `code-review` skill.

Target files, PR scope, or diff to review (default to current git diff if omitted):
$ARGUMENTS

Inspect surrounding callers and tests alongside the diff, then report findings ranked from `[Blocker]` to `[Nit]` with exact `file:line` references, concrete fixes, and a clear merge verdict.
