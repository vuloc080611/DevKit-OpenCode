---
name: docker-setup
description: Create production-grade multi-stage Dockerfiles and clean compose.yaml / docker-compose setups with minimal image size, non-root users, deterministic dependency caching, healthchecks, and secure secret/env handling. Use when containerizing apps or setting up local/prod Docker environments ("viết Dockerfile", "docker-compose", "tối ưu docker image").
license: MIT
compatibility: opencode
metadata:
  category: web-backend
  audience: developers
  version: "1.0.0"
---

# Docker Setup — Multi-Stage Dockerfiles & Clean Compose

Build small, reproducible, secure containers and dependable multi-service `compose.yaml` environments.

## When to Use

- Containerizing Node.js, Python, Go, Java, or static frontend apps with `Dockerfile` + `.dockerignore`.
- Setting up local dev or staging stacks (`compose.yaml`) with databases, caches, and service health dependencies.
- Optimizing bloated or insecure existing Dockerfiles.

## Step-by-Step Workflow

1. **Inspect Runtime, Lockfiles & Entrypoint**:
   - Check actual runtime versions (`.nvmrc`, `pyproject.toml`, `go.mod`, `package.json` engines), build commands, static output dirs, and exposed port.
2. **Create `.dockerignore` First**:
   - Exclude `.git`, `node_modules`, `.venv`, `__pycache__`, `dist`, `.env*`, test coverage, and local IDE artifacts to avoid slow build contexts and secret leaks into image layers.
3. **Write a Multi-Stage `Dockerfile`**:
   - **Pin specific base tags** (e.g., `node:22-alpine`, `python:3.12-slim`) — never `:latest`.
   - **Optimize layer caching:** Copy lockfiles (`package.json` + `package-lock.json` / `pnpm-lock.yaml`, `pyproject.toml` + `uv.lock`) and install dependencies *before* copying `src/`.
   - **Builder vs Runtime stage:** Compile/bundle in `builder`; copy only production artifacts + runtime deps into a slim final image (or `distroless`/binary for Go/Rust).
   - **Run as non-root user:** Create/use a dedicated low-privilege user (`USER node`, `USER appuser`).
   - **Include `HEALTHCHECK`** where appropriate and proper signal handling (`exec` form `CMD ["node", "dist/server.js"]`).
4. **Write Clean `compose.yaml`**:
   - Define explicit `healthcheck` on DB/cache services (`pg_isready`, `redis-cli ping`) and wire app `depends_on: { db: { condition: service_healthy } }`.
   - Use named volumes for persistent DB state (`postgres_data:/var/lib/postgresql/data`).
   - Load config via `env_file` / environment variables with safe dev defaults — never hardcode real production credentials.
   - Separate dev hot-reload overrides (`compose.override.yaml` or `profiles`) from clean production builds when needed.
5. **Verify Build & Startup (When Docker Daemon Is Available)**:
   - Run `docker build` and `docker compose config` (plus `docker compose up -d` + health check if Docker is running locally) and report exact observed status.

## Anti-Patterns (Do Not)

- **DO NOT** omit `.dockerignore` (leads to huge build context and copying local `.env` or `node_modules` into the container).
- **DO NOT** run production containers as `root` when a non-root user works cleanly.
- **DO NOT** `COPY . .` before `npm ci` / `pip install` (busts dependency cache on every single code edit).
- **DO NOT** bake `.env`, SSH keys, or API secrets into `Dockerfile` `ENV`/`ARG` layers (they persist in image history).
- **DO NOT** use shell-form `CMD npm start` without checking signal forwarding (`SIGTERM` graceful shutdown).

## Examples

### Example: Production Node.js (TypeScript) + PostgreSQL Setup
**Input:**
> "Tạo `Dockerfile`, `.dockerignore` và `compose.yaml` cho app Node.js TypeScript + PostgreSQL."

**Output (`Dockerfile`):**
```dockerfile
# syntax=docker/dockerfile:1
FROM node:22-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci

FROM deps AS builder
COPY tsconfig.json ./
COPY src ./src
RUN npm run build && npm prune --omit=dev

FROM node:22-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder --chown=node:node /app/node_modules ./node_modules
COPY --from=builder --chown=node:node /app/dist ./dist
COPY --from=builder --chown=node:node /app/package.json ./package.json
USER node
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD wget -qO- http://127.0.0.1:3000/health || exit 1
CMD ["node", "dist/server.js"]
```
*(Paired with `.dockerignore` excluding `.git`, `node_modules`, `.env*`, `dist`, and `compose.yaml` with `postgres:16-alpine` `pg_isready` healthcheck and `service_healthy` dependency.)*
