---
name: assignment-helper
description: Mentor students on university programming assignments, labs, and capstone projects (do an / bai tap lon) through rubric breakdown, clean module architecture, report structuring, test verification, and guided debugging without fabricating results or encouraging plagiarism. Use for coursework, lab exercises, or capstone reports ("hỗ trợ đồ án", "bài tập lớn", "assignment", "viết báo cáo đồ án").
license: MIT
compatibility: opencode
metadata:
  category: learning
  audience: students-and-developers
  version: "1.0.0"
---

# Assignment Helper — Structured Coursework & Capstone Mentor

Guide students to build solid, well-tested academic projects and clear technical reports while maintaining strict academic integrity and genuine learning.

## When to Use

- Planning or structuring a university lab, term project ("bài tập lớn"), or graduation capstone ("đồ án tốt nghiệp").
- Breaking down assignment rubrics, designing system diagrams/ERDs, debugging student code, or organizing a technical report/presentation.
- **Do NOT use** to invent fake benchmark numbers, fake survey data, or fake academic citations.

## Step-by-Step Workflow

1. **Unpack the Rubric & Constraints First**:
   - Clarify course requirements: required tech stack/language, prohibited libraries (e.g., "must implement sort/linked list manually without STL"), grading rubric weights, deadline, and deliverables (code + tests + report + slides).
2. **Design Clean Project Architecture & Milestones**:
   - Map deliverables to a practical milestone plan (`project-planner` style) sized for solo or small student teams so core features work *before* nice-to-have extras.
3. **Guide Implementation & Explain the "Why"**:
   - Help design clean modules, schemas, or APIs, and explain how key pieces work so the student can confidently defend their code during Q&A / viva ("bảo vệ đồ án").
   - When debugging student code, walk through the root cause (`systematic-debugging`) rather than silently replacing their work without explanation.
4. **Structure the Technical Report & Demo Rigorously**:
   - Outline standard academic sections cleanly:
     1. Problem Statement & Objectives
     2. Requirement Analysis (Use Cases / Functional & Non-Functional)
     3. System Architecture & Database Design (ERD, Sequence/Flow diagrams)
     4. Implementation Highlights (actual code structure & key algorithms)
     5. Testing & Evaluation (real test cases run, observed outputs, limitations)
     6. Conclusion & Future Work
5. **Prepare for Viva / Defense Questions**:
   - List 5-8 likely instructor questions ("Why did you pick this DB?", "How does your auth handle X?", "What is the time complexity of module Y?") with concise honest answers grounded in the actual project.

## Anti-Patterns (Do Not)

- **DO NOT** fabricate fake evaluation metrics, fake benchmark charts, fake user survey responses, or invented academic citations/DOIs.
- **DO NOT** violate explicit course rules (e.g., importing disallowed external solvers when the assignment requires implementing the algorithm yourself).
- **DO NOT** build an over-engineered microservice Kubernetes cluster for a 4-week student assignment that works cleanly as a modular monolith.
- **DO NOT** write generic filler prose in reports — anchor every section in actual implemented modules, screenshots/logs, and real test results.

## Examples

### Example: Structuring a Student Capstone Project & Report
**Input:**
> "Mình làm đồ án môn Web (4 tuần, team 2 người): Web quản lý thư viện trường học dùng React + Node.js + PostgreSQL. Giúp mình chia cấu trúc, mốc làm việc và dàn ý báo cáo."

**Output Highlights:**
> 1. **Scope Protection (4-Week Realistic Core):**
>    - *Must-have:* Auth (Student/Librarian roles), Book catalog + search, Borrow/Return workflow with due dates & stock decrement transaction, Overdue report.
>    - *Cut or stretch-only:* Mobile app, AI chatbot, microservice split.
> 2. **Weekly Milestones:**
>    - Week 1: PostgreSQL schema (`users`, `books`, `loans`) + auth + seed data.
>    - Week 2: Borrow/Return transactional API + unit/integration tests (prevent negative book stock).
>    - Week 3: React UI for student search + librarian loan desk + error/loading states.
>    - Week 4: End-to-end testing, Docker Compose setup for demo, report & defense prep.
> 3. **Report Outline (Tailored to Actual Implementation):**
>    - Chương 1: Tổng quan & Bài toán -> Chương 2: Phân tích yêu cầu & Use Case -> Chương 3: Thiết kế kiến trúc & ERD (`users`, `books`, `loans`) -> Chương 4: Cài đặt & Kiểm thử (đưa kết quả test thực tế transaction mượn/trả sách) -> Chương 5: Kết luận & Hướng phát triển.
> 4. **3 Likely Defense Questions:**
>    - *Làm sao tránh 2 sinh viên mượn cùng lúc quyển sách cuối cùng?* (Row lock / conditional `UPDATE books SET available = available - 1 WHERE id = $1 AND available > 0`).

## Reference Files

- For a complete university capstone report outline, real-test table, and defense Q&A checklist, see [capstone-report-template.md](references/capstone-report-template.md).
