---
name: security-review
description: Audit code, APIs, configs, and dependencies for security vulnerabilities covering OWASP Top 10, authentication, authorization/IDOR, input validation, injection (SQLi, XSS, command, SSRF), secrets handling, and supply-chain risks. Use when reviewing auth, payments, file uploads, configs, or running a security audit ("bảo mật", "security audit", "OWASP check"). For general PR quality review, use code-review.
license: MIT
compatibility: opencode
metadata:
  category: quality
  audience: developers
  version: "1.0.0"
---

# Security Review — Focused Application Security Audit

Identify exploitable security flaws across trust boundaries, data flows, configurations, and dependencies with concrete remediation steps.

## When to Use

- Auditing authentication, authorization, session/JWT handling, file uploads, webhooks, payment flows, or admin endpoints.
- Before shipping sensitive changes or when user asks for an OWASP / security review.
- **Do NOT use** for general code style feedback (use `code-review`).

## Step-by-Step Security Audit

1. **Map Entry Points & Trust Boundaries**:
   - Identify untrusted inputs (HTTP params, headers, cookies, uploaded files, webhook payloads, URL params, LLM/tool outputs) and sensitive sinks (DB queries, shell commands, filesystem paths, HTML templates, outbound HTTP requests).
2. **Audit Authentication & Session Management**:
   - Password hashing (`bcrypt`/`argon2`, never MD5/SHA-256), constant-time comparisons for tokens/signatures, short-lived access tokens + revocable refresh tokens, secure cookie flags (`HttpOnly`, `Secure`, `SameSite`), brute-force rate limiting.
3. **Audit Authorization (Access Control)**:
   - Verify **every** endpoint/resolver checks both authentication AND object-level ownership/tenant isolation (prevent IDOR/BOLA). Check default-deny policy and admin privilege escalation paths.
4. **Check Injection & Input/Output Sinks**:
   - **SQLi / NoSQLi:** Parameterized queries / ORM bindings only; never string-concatenated queries or raw `$where`/unsanitized query objects.
   - **XSS:** Context-aware escaping; block `dangerouslySetInnerHTML`, `v-html`, raw HTML interpolation without strict sanitization (DOMPurify).
   - **Command Injection:** Never pass user input into shell strings (`exec`, `shell=True`); use argument arrays (`execFile`, `subprocess.run([...], shell=False)`).
   - **Path Traversal:** Canonicalize paths and verify `resolved.startsWith(allowedRoot + path.sep)` for uploads/downloads.
   - **SSRF:** Validate outbound URLs against allowlists and block private/loopback/metadata IP ranges (`169.254.169.254`, `127.0.0.0/8`, `10.0.0.0/8`, `::1`).
5. **Inspect Secrets, Cryptography & Data Exposure**:
   - Search for hardcoded API keys, fallback JWT secrets (`process.env.JWT_SECRET || "dev-secret"`), sensitive fields leaked in API responses/logs (passwords, tokens, PII), and missing CORS/CSRF protections.
6. **Check Dependencies & Config**:
   - Inspect lockfiles/manifests (`npm audit`, `pip-audit` if available), permissive CORS (`origin: "*"` with `credentials: true`), debug stack traces enabled in prod.
7. **Report Exploit Scenario + Minimal Fix**:
   - Rank by Risk (`Critical`, `High`, `Medium`, `Low`) with attack vector and exact remediation code.

## Anti-Patterns (Do Not)

- **DO NOT** assume framework defaults make code safe without verifying route middleware and query filters.
- **DO NOT** rely on client-side validation or hidden UI fields as security controls.
- **DO NOT** report hypothetical issues in dead/unreached code without checking actual data flow first.
- **DO NOT** print or echo real secret values found in `.env` or logs into outputs — redact them.

## Security Checklist

- [ ] AuthN: strong hashing, signed/verified tokens, brute-force protection
- [ ] AuthZ: object/tenant ownership enforced on every mutating & private read route
- [ ] Injection: SQLi, XSS, Command Injection, Path Traversal, SSRF checked
- [ ] Secrets: no hardcoded keys or insecure default fallbacks; no PII/tokens in logs
- [ ] Transport & Browser: CORS, CSRF, Helmet/CSP headers, secure cookies verified
- [ ] Files & Webhooks: MIME/magic-bytes + size limits + signature verification (`crypto.timingSafeEqual`)

## Reference Files

- For detailed stack-specific checks (JWT/Auth, SQL/NoSQL, SSRF, Uploads, Webhooks), see [owasp-stack-checklists.md](references/owasp-stack-checklists.md).

## Examples

### Example: Auditing a File Export & Webhook Handler
**Input:**
> "Kiểm tra bảo mật cho route download invoice và webhook callback thanh toán này."

**Output:**
> ### Security Audit Findings
>
> 1. **[Critical] Path Traversal in `GET /invoices/download` (`src/routes/invoices.ts:19`)**
>    - **Issue:** `path.join(UPLOAD_DIR, req.query.file)` lets an attacker pass `../../.env` to read arbitrary server files.
>    - **Fix:** Allowlist filename pattern or resolve `const target = path.resolve(UPLOAD_DIR, path.basename(file))` and assert `target.startsWith(path.resolve(UPLOAD_DIR) + path.sep)` PLUS verify invoice ownership (`invoice.userId === req.user.id`).
> 2. **[High] Non-constant-time / unverified webhook signature (`src/routes/webhook.ts:11`)**
>    - **Issue:** Signature uses `req.headers["x-sig"] === expectedSig` and parses JSON before verifying raw body HMAC.
>    - **Fix:** Compute HMAC-SHA256 over the raw request buffer and compare with `crypto.timingSafeEqual(Buffer.from(sig), Buffer.from(expected))`.
> 3. **[Medium] Secret fallback in JWT config (`src/config/auth.ts:4`)**
>    - **Issue:** `JWT_SECRET = process.env.JWT_SECRET ?? "secret123"` allows forged tokens if env var is missing in prod.
>    - **Fix:** Fail fast on startup when `JWT_SECRET` is unset or `< 32` chars.
