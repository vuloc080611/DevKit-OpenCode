# Changelog

All notable changes to **DevKit OpenCode (`devkit-opencode`)** are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [1.0.0] - 2026-11-25

### Added
- **24 OpenCode Skills** across 6 lifecycle categories (`skills/<name>/SKILL.md`):
  - **Planning & Requirements:** `grill-me`, `spec-writer`, `project-planner`, `architecture-decision`
  - **Implementation Discipline:** `tdd-workflow`, `incremental-implementation`, `systematic-debugging`, `verification-before-done`
  - **Code Quality & Review:** `code-review`, `security-review`, `performance-review`, `refactor-safe`, `code-simplification`
  - **Daily Dev Tools:** `git-commit`, `changelog-generator`, `readme-generator`, `docs-writer`
  - **Web & Backend:** `api-designer`, `database-schema`, `frontend-component`, `docker-setup`
  - **Student & Learning:** `dsa-explainer`, `leetcode-helper`, `assignment-helper`
- **8 OpenCode Custom Slash Commands** (`commands/*.md`): `/grill`, `/plan`, `/tdd`, `/debug`, `/verify`, `/review`, `/security`, and `/commit`, with read-only `agent: plan` scoping on review/planning commands (`f7c2fba`).
- **Deep Skill References** (`skills/*/references/`): stack-specific OWASP checklists (`security-review`), zero-downtime PostgreSQL migration patterns (`database-schema`), copy-ready PRD template (`spec-writer`), and university capstone report template (`assignment-helper`) (`6f91ccb`).
- **Cross-Platform Installers** ([scripts/install.sh](scripts/install.sh), [scripts/install.ps1](scripts/install.ps1)) supporting global/project installation, `--core-only`, and timestamped backups of existing `AGENTS.md` and `opencode.jsonc` files (`4b58d36`).
- **Validation & CI** ([scripts/validate.py](scripts/validate.py), `.github/workflows/validate.yml`) checking frontmatter syntax, description lengths (`<= 1024`), command templates, JSONC config parsing, and Markdown links (`5e5100c`).
- **Trigger Evaluation Suite** ([docs/eval-prompts.md](docs/eval-prompts.md)) and sharpened trigger boundaries across sibling skills (`3ac6355`).
- **Repository Hygiene & Documentation:** [AGENTS.md](AGENTS.md), [config/opencode.jsonc.example](config/opencode.jsonc.example), [README.md](README.md) (Vietnamese), [README.en.md](README.en.md) (English), [INSTALL.md](INSTALL.md), [CONTRIBUTING.md](CONTRIBUTING.md), [LICENSE](LICENSE), `.gitignore`, and `.gitattributes` (`b08b305`, `a4fd66f`).
