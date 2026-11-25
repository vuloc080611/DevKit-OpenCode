# Contributing to DevKit OpenCode

Thank you for helping make **DevKit OpenCode** sharper, more disciplined, and genuinely practical for developers and students.

---

## Design Principles

1. **One Skill = One Clear Job:** Avoid bloated catch-all skills or duplicate variations of an existing skill. Before proposing a new skill, check whether an existing skill or a new file under `skills/<existing>/references/` fits better.
2. **Concrete Discipline Over Generic Advice:** Every skill must enforce clear steps, measurable gates, explicit **Anti-Patterns (Do Not)**, and realistic **Input → Output** examples.
3. **Sharp Trigger Boundaries:** `description` must clearly state *when* to trigger and *when not* to trigger (to avoid confusion with sibling skills), staying strictly within **1–1024 characters**.
4. **No Unverified Claims:** Only document real commands, flags, file paths, and observed validation output.

---

## Authoring Checklist for New or Updated Skills

When adding or modifying a skill under `skills/<skill-name>/SKILL.md`:

- [ ] Directory name and frontmatter `name:` match exactly (`^[a-z0-9]+(-[a-z0-9]+)*$`, `<= 64` chars).
- [ ] Frontmatter includes `name`, `description` (`<= 1024` chars), `license: MIT`, `compatibility: opencode`, and `metadata`.
- [ ] Body contains `## When to Use`, `## Step-by-Step Workflow` (or `## Mandatory ...`), `## Anti-Patterns (Do Not)`, and `## Examples`.
- [ ] If adding a **new** skill:
  - Register it under `permission.skill` in [config/opencode.jsonc.example](config/opencode.jsonc.example).
  - Document it in [AGENTS.md](AGENTS.md), [README.md](README.md), and [README.en.md](README.en.md).
  - Add boundary test prompts in [docs/eval-prompts.md](docs/eval-prompts.md) if it sits near an existing skill.

## Authoring Checklist for Slash Commands

When adding or modifying a command under `commands/<name>.md`:

- [ ] Frontmatter includes `description` and `agent` (`plan` for read-only planning/review commands, `build` for implementation/commit commands).
- [ ] Do **not** hardcode a specific `model:` override so the command inherits each user's configured provider/model.
- [ ] Support `$ARGUMENTS` cleanly when user input is expected.

---

## Local Verification Before Opening a PR

Always run the repository validator before committing:

```bash
python scripts/validate.py
```

On Linux / macOS (or Git Bash), also sanity-check the bash installer:

```bash
bash -n scripts/install.sh
bash scripts/install.sh --target /tmp/devkit-verify
```

On Windows PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install.ps1 -TargetDir "$env:TEMP\devkit-verify"
```

---

## Pull Request Process

1. Create a focused branch (`feat/skill-xyz`, `docs/improve-security-checklist`, `fix/install-ps1`).
2. Keep commits clean using Conventional Commits (`feat:`, `fix:`, `docs:`, `ci:`, `chore:`).
3. Confirm `python scripts/validate.py` exits with `0` and paste the output in your PR description.
