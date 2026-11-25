---
name: readme-generator
description: Inspect the actual repository codebase, dependencies, scripts, env variables, and architecture to generate or update an accurate, well-structured README.md with verified commands and zero hallucinated instructions. Use when creating or refreshing README.md ("viết README", "cập nhật README", "tạo hướng dẫn dự án").
license: MIT
compatibility: opencode
metadata:
  category: devtools
  audience: developers
  version: "1.0.0"
---

# README Generator — Grounded, Accurate Project Documentation

Create scannable, practical `README.md` files verified strictly against real files, scripts, and configs in the repository.

## When to Use

- Bootstrapping `README.md` for a new repository or updating an outdated `README.md` after major changes.
- **Do NOT use** for granular API docs or code docstrings (use `docs-writer`) or release history (use `changelog-generator`).

## Step-by-Step Workflow

1. **Inspect the Real Codebase First (Never Guess)**:
   - Read directory layout, manifest files (`package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`), `.env.example`, `compose.yaml`, `Makefile`, and entrypoints.
   - Note exact runtime versions, package manager (`npm`/`pnpm`/`uv`/`poetry`), scripts (`dev`, `build`, `test`, `lint`), and existing links.
2. **Clarify Audience & Language**:
   - Match the project's primary language (English or Vietnamese) and audience (open-source contributors, internal team, or end users).
3. **Structure for Fast Onboarding (< 2 min to understand)**:
   - **Title & 1-sentence Value Prop**: What it does and who it is for.
   - **Key Features**: Concrete capabilities actually implemented (not wishlist vaporware).
   - **Tech Stack / Requirements**: Exact prerequisites (Node, Python, Docker, Postgres versions observed).
   - **Quick Start / Installation**: Copy-pasteable commands from clone → env setup → install → run.
   - **Configuration / Environment Variables**: Table of real env vars from `.env.example` or config loaders.
   - **Usage / Commands / API Overview**: Real CLI commands, scripts, or endpoints.
   - **Project Structure**: Clean tree of top-level directories/key files.
   - **Testing & Contributing / License**: Exact test commands and license file link.
4. **Verify Every File Link, Path & Command**:
   - Double-check every relative path, npm script, env var name, and directory tree entry against actual files in the repository.

## Anti-Patterns (Do Not)

- **DO NOT** invent npm scripts (`npm run start:prod`), CLI flags, or features that do not exist in the codebase.
- **DO NOT** copy generic placeholder text (`"Lorem ipsum"`, `"your-repo-url"` without marking `<repo-url>`, fake screenshots/badges).
- **DO NOT** dump every single helper file into the Project Structure tree — keep it readable at 1-2 levels.
- **DO NOT** list secret values; only document env var names and safe example formats from `.env.example`.

## README Checklist

- [ ] Every documented script/command exists in manifest/Makefile
- [ ] Every env variable matches `.env.example` or config parser
- [ ] Every markdown link points to an existing file/heading
- [ ] Prerequisites and quick-start steps tested or cross-checked against config

## Examples

### Example: Refreshing an Outdated FastAPI Service README
**Input:**
> "Cập nhật `README.md` cho project Python FastAPI này sau khi tụi mình chuyển từ pip sang `uv` và thêm Docker Compose."

**Output Highlights:**
> Inspected `pyproject.toml`, `uv.lock`, `.env.example`, `compose.yaml`, and `app/main.py`:
> - Updated prerequisites to `Python >= 3.11` and `uv` (or Docker Compose v2).
> - Replaced outdated `pip install -r requirements.txt` with verified `uv sync` and `uv run uvicorn app.main:app --reload`.
> - Added Env table matching all 6 variables in `.env.example` (`DATABASE_URL`, `REDIS_URL`, `JWT_SECRET`, `LOG_LEVEL`, `PORT`, `CORS_ORIGINS`).
> - Added Testing section using exact `uv run pytest` command verified in `pyproject.toml`.
