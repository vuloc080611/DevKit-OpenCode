# OWASP & Stack-Specific Security Checklists

Load this checklist during `security-review` when auditing Node.js/TypeScript, Python, SQL, file upload, or webhook codebases.

## 1. Authentication & Session Security
- Passwords hashed with `argon2id` or `bcrypt` (cost >= 10), never `md5`/`sha1`/`sha256`.
- JWT verification explicitly pins allowed `alg` (`HS256` or `RS256` — reject `"none"` and key-confusion attacks) and validates `exp`, `iss`, and `aud`.
- Secrets (`JWT_SECRET`, session signing keys, webhook secrets) loaded from env with startup fail-fast validation (never `|| "dev-secret"` fallbacks).
- Cookies storing session/refresh tokens set `HttpOnly`, `Secure`, `SameSite=Lax` (or `Strict`).
- Password reset / magic-link tokens generated via CSPRNG (`crypto.randomBytes(32)` / `secrets.token_urlsafe(32)`), stored hashed in DB, single-use, short TTL (`<= 15 min`).

## 2. Authorization (IDOR / BOLA / Privilege Escalation)
- Every single-resource endpoint (`GET/PATCH/DELETE /items/:id`) scopes query by authenticated tenant/owner (`WHERE id = $1 AND user_id = $2` or explicit admin role check).
- Request bodies validated through strict allowlist schemas (Zod / Pydantic) — never spread raw `req.body` into `update()` (blocks mass assignment of `role`, `isAdmin`, `balance`).
- Admin / internal endpoints enforce role check in middleware AND verify non-elevatable role claims.

## 3. Injection & Input/Output Sinks
- **SQL Injection:** Parameterized queries (`$1`, `?`, ORM bindings) only; validate dynamic `ORDER BY` column names against a hardcoded `Set`/`Map` allowlist.
- **NoSQL Injection:** Strip or reject `$`-prefixed keys (`$ne`, `$gt`, `$where`) from untrusted JSON payloads; enforce scalar types with Zod/Pydantic.
- **XSS:** Never inject unescaped user strings into `dangerouslySetInnerHTML`, `v-html`, `innerHTML`, or raw HTML email templates without sanitization (DOMPurify + strict CSP).
- **Command Injection:** Use argument arrays (`execFile`, `spawn(..., { shell: false })`, `subprocess.run([...], shell=False)`), never string interpolation into shells.
- **SSRF:** Parse outbound user-provided URLs, enforce `https:` scheme + explicit host allowlist when possible, and resolve DNS before connecting to block loopback (`127.0.0.0/8`, `::1`), RFC1918 (`10/8`, `172.16/12`, `192.168/16`), and cloud metadata (`169.254.169.254`).

## 4. File Uploads & Downloads
- Enforce hard request size limits before buffering.
- Validate magic bytes/file signature (not only `Content-Type` header or `.jpg` extension).
- Store uploaded files outside webroot using random UUID filenames; never serve user-uploaded `.html`/`.svg` inline on the main origin without `Content-Disposition: attachment` + `X-Content-Type-Options: nosniff`.
- Canonicalize download paths (`path.resolve`) and verify `resolved.startsWith(allowedBase + path.sep)` to stop `../` traversal.

## 5. Webhooks & External Callbacks
- Verify HMAC signatures against raw unparsed request bytes using constant-time comparison (`crypto.timingSafeEqual` / `hmac.compare_digest`).
- Reject replayed timestamps outside tolerance window (e.g., `> 5 minutes`) and store processed event IDs for idempotency.

## 6. Browser & API Hardening
- CORS never combines `Access-Control-Allow-Origin: *` with `Access-Control-Allow-Credentials: true`; allowlist explicit trusted origins.
- Sensitive endpoints (`login`, `forgot-password`, `otp-verify`, `coupons/preview`) protected with IP + account rate limiting.
- Production error handlers return generic messages + `requestId`; stack traces, SQL queries, and env dumps stay in server logs only (redacting `Authorization`, `Cookie`, passwords, and tokens).
