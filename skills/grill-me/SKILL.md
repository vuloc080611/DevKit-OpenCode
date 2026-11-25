---
name: grill-me
description: Relentlessly interrogate ambiguous feature requests, project ideas, or bug reports until edge cases, constraints, non-goals, and success criteria are crystal clear before writing any code. Use when a prompt is vague, underspecified, large, high-risk, or when the user asks to clarify requirements first ("hỏi kỹ trước khi code", "interview me", "clarify requirements").
license: MIT
compatibility: opencode
metadata:
  category: planning
  audience: developers
  version: "1.0.0"
---

# Grill Me — Requirements Interrogation Before Code

Force clarity before implementation. When requirements are ambiguous, incomplete, or carry hidden assumptions, ask sharp, targeted questions until both you and the user agree on exact scope, edge cases, constraints, and acceptance criteria.

## When to Use

- The user asks for a non-trivial feature with missing details (e.g., "build auth", "add notifications", "create a dashboard", "làm hệ thống đặt lịch").
- Key business rules, failure modes, security boundaries, or success criteria are unstated.
- Multiple valid interpretations exist and guessing wrong would waste significant implementation effort.
- **Do NOT use** for trivial, unambiguous edits (e.g., typo fixes, single-line renames) or when a complete approved spec already exists (hand off to `project-planner` or `tdd-workflow`).

## Step-by-Step Workflow

1. **Restate & Inspect Context First**:
   - Read relevant repository files silently so you never ask questions the codebase already answers (tech stack, existing models, framework conventions).
   - Briefly state what you already understand in 2-3 bullet points.
2. **Identify Ambiguity Gaps**:
   - Audit five dimensions:
     1. **Users & Trigger**: Who initiates this, from where, with what permissions?
     2. **Core Behavior & Data**: Inputs, outputs, state transitions, persistence, validation rules?
     3. **Edge Cases & Failure Modes**: Empty/null states, concurrency, retries, timeouts, invalid input, partial failure?
     4. **Constraints & Non-Goals**: Performance targets, backwards compatibility, security/privacy limits, what is explicitly out of scope?
     5. **Success Criteria**: How will we prove it works (tests, observable metrics, UI/API behavior)?
3. **Ask Focused Questions in Tight Batches**:
   - Group at most **3-5 high-impact questions** per turn, ordered from highest architectural impact to smallest detail.
   - Provide sensible default recommendations `(Recommended)` where appropriate so the user can answer quickly.
   - Wait for the user's answers. Do **not** start editing files or writing production code yet.
4. **Repeat Until Convergence**:
   - If answers reveal new ambiguities or contradictions, ask a focused follow-up round.
   - Stop grilling once no blocking ambiguity remains.
5. **Lock Alignment Summary**:
   - Summarize the agreed **Scope**, **Non-Goals**, **Key Edge Cases**, and **Acceptance Criteria** concisely and ask for a quick `"Proceed"` confirmation before handing off to `spec-writer`, `project-planner`, or implementation.

## Anti-Patterns (Do Not)

- **DO NOT** write any production code, scaffold files, or run mutating commands while requirements are still ambiguous.
- **DO NOT** dump 20 generic questions in one overwhelming wall of text.
- **DO NOT** ask questions whose answers are already visible in `package.json`, schema files, or existing code.
- **DO NOT** silently invent business rules (e.g., pricing logic, permission defaults, retention policies) without surfacing them.
- **DO NOT** accept vague answers like "make it secure/fast" without pinning down concrete thresholds or rules.

## Output Checklist

- [ ] Codebase inspected before questioning
- [ ] Questions grouped, prioritized (3-5 max per round), with recommended defaults
- [ ] Edge cases, failure modes, and non-goals explicitly probed
- [ ] Final alignment summary confirmed by user before coding

## Examples

### Example 1: Vague Feature Request
**Input:**
> "Thêm tính năng quên mật khẩu cho backend Node.js của mình."

**Output:**
> Tôi đã kiểm tra repo và thấy dự án đang dùng Express + PostgreSQL + JWT (`src/routes/auth.ts`). Trước khi viết code, cần làm rõ 4 điểm quyết định hành vi cốt lõi:
>
> 1. **Cơ chế reset**: Dùng link token gửi qua email (Recommended — hết hạn sau 15 phút, dùng 1 lần) hay mã OTP 6 số?
> 2. **Email provider**: Hiện chưa thấy thư viện gửi mail trong `package.json` — bạn muốn dùng provider nào (Resend, Nodemailer/SMTP), hay log token ra console ở môi trường dev?
> 3. **Bảo mật & Chống brute-force**: Có cần rate-limit (ví dụ tối đa 3 lần / 15 phút / email+IP) và vô hiệu hóa toàn bộ refresh token cũ sau khi đổi mật khẩu không? (Recommended: Có cả hai)
> 4. **Thông báo lỗi**: Khi email không tồn tại trong DB, API nên trả về `200 OK` chung chung để chống user enumeration (Recommended) hay báo lỗi cụ thể?
>
> Trả lời ngắn gọn 4 ý trên, tôi sẽ chốt spec/plan rồi bắt đầu implement.

### Example 2: User Confirms Alignment
**Input:**
> "1. Link token 15p dùng 1 lần. 2. Dev log console, prod dùng Resend qua env. 3. Có cả rate-limit và revoke token cũ. 4. Trả 200 chung chung."

**Output:**
> Đã chốt phạm vi cho **Forgot/Reset Password**:
> - **Flow**: `POST /auth/forgot-password` tạo random token (SHA-256 hash lưu DB, TTL 15 phút, single-use) → gửi link qua Resend (hoặc console log khi `NODE_ENV !== 'production'`), luôn trả `200`.
> - **Reset**: `POST /auth/reset-password` verify token chưa hết hạn/chưa dùng → cập nhật password hash → mark token used → revoke toàn bộ active sessions/refresh tokens.
> - **Guardrails**: Rate-limit 3 req / 15m per IP+email; **Non-goals**: chưa làm UI email template HTML phức tạp hay SMS fallback.
> - **Acceptance Criteria**: Test cover happy path, expired token, reused token, unknown email (still 200), và session revocation.
>
> Xác nhận `Proceed` để tôi chuyển sang lập plan (`project-planner`) hoặc viết test trước (`tdd-workflow`).
