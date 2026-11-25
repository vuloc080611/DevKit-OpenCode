---
description: Implement a feature or fix using strict Red-Green-Refactor TDD (tdd-workflow)
agent: build
---

Load and strictly follow the `tdd-workflow` skill.

Target requirement or bug fix:
$ARGUMENTS

Write one failing test first, run it to verify it fails for the expected reason (RED), write minimal production code to pass (GREEN), refactor safely while keeping tests green, and finish with `verification-before-done`.
