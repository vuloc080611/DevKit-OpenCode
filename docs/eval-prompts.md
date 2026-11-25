# Bộ Prompt Kiểm Thử Trigger & Ranh Giới Skill (`eval-prompts.md`)

Tài liệu này dùng để kiểm tra thực tế trên OpenCode xem agent có **chọn đúng skill** và **tuân thủ đúng ranh giới kỷ luật** (đặc biệt giữa các cặp skill dễ trùng ngữ nghĩa) hay không.

---

## 1. Kiểm Thử Ranh Giới Giữa Các Cặp Skill Gần Nhau

| Prompt thử nghiệm | Skill kỳ vọng | Không được nhầm sang | Tiêu chí đạt |
|---|---|---|---|
| *"Review giúp mình PR thêm chức năng giỏ hàng xem có bug hay thiếu test không."* | `code-review` | `security-review` | Xếp hạng `[Blocker]`/`[Minor]`, kiểm tra edge cases & test coverage |
| *"Audit bảo mật cho flow upload file và webhook thanh toán Stripe này giúp mình."* | `security-review` | `code-review` | Kiểm tra path traversal, magic bytes, HMAC `timingSafeEqual`, IDOR |
| *"Tách file `order.service.ts` 400 dòng thành các module nhỏ hơn nhưng tuyệt đối không đổi behavior cũ."* | `refactor-safe` | `code-simplification` | Map callers + đảm bảo có characterization tests trước khi tách từng bước |
| *"Hàm `sendAlert` này lồng 5 tầng `if` và tạo factory thừa thãi quá, viết gọn lại giúp mình."* | `code-simplification` | `refactor-safe` | Dùng early return + lookup table, xóa wrapper thừa, giữ nguyên behavior |
| *"Giải thích từ bản chất thuật toán Monotonic Stack, chạy tay minh họa và chứng minh vì sao là $O(n)$."* | `dsa-explainer` | `leetcode-helper` | Trực giác → bảng chạy tay 4–6 bước → chứng minh $O(n)$ → code mẫu |
| *"Mình đang làm LeetCode 560 bị Wrong Answer khi có số âm, gợi ý hướng sửa chứ đừng đưa full code vội."* | `leetcode-helper` | `dsa-explainer` | Chỉ ra vì sao Sliding Window sai, đưa Hint 1 & Hint 2, **không** spoil code AC |
| *"Cập nhật lại `README.md` cho repo sau khi mình đổi từ npm sang pnpm."* | `readme-generator` | `docs-writer` | Đọc `package.json`/lockfile thật và chỉ cập nhật lệnh có thật trong repo |
| *"Viết TSDoc cho hàm `acquireLock` và runbook xử lý lỗi Redis timeout."* | `docs-writer` | `readme-generator` | Ghi rõ invariants, errors trong docstring; viết runbook theo trình tự triage → fix |

---

## 2. Kiểm Thử Kỷ Luật Cốt Lõi (Hard Gates)

| Prompt thử nghiệm | Skill kỳ vọng | Hành vi bắt buộc phải thấy |
|---|---|---|
| *"Làm cho mình hệ thống thông báo realtime cho app này."* | `grill-me` | **Dừng lại hỏi 3–5 câu** về kênh gửi, độ trễ, persistence, edge cases; **không** viết code ngay |
| *"Chốt spec cho tính năng mã giảm giá vừa trao đổi xong."* | `spec-writer` | Có Goals, **Non-Goals**, contracts, bảng Edge Cases, Acceptance Criteria dạng Given/When/Then |
| *"Chia task implement spec coupon và chọn queue `pg-boss` vs `BullMQ`."* | `architecture-decision` → `project-planner` | Tạo ADR so sánh 2 phương án trung thực, rồi chia task có cột `Verify` từng bước |
| *"Implement hàm tính thuế VAT theo TDD."* | `tdd-workflow` | Viết test fail trước → chạy thấy fail (RED) → mới viết code tối thiểu (GREEN) → refactor |
| *"API `GET /products?q=` bị 500 trên prod nhưng unit test vẫn pass, sửa giúp mình."* | `systematic-debugging` | Tái hiện lỗi → đọc stack trace → nêu 1 giả thuyết → kiểm chứng → sửa + thêm regression test |
| *"Xong chưa bạn, báo kết quả để mình merge."* | `verification-before-done` | Chạy lệnh test/typecheck/lint **sau lần sửa cuối**, báo đúng output quan sát được và phần chưa test |

---

## 3. Kiểm Thử Slash Commands

Chạy trực tiếp trong OpenCode TUI sau khi cài `commands/`:

1. `/grill Tạo tính năng xuất hóa đơn PDF` → chạy dưới `agent: plan`, không sửa file.
2. `/review src/routes/` → chạy dưới `agent: plan`, review có `file:line`.
3. `/security src/auth/` → chạy dưới `agent: plan`, rà auth/IDOR/injection/secrets.
4. `/tdd Viết validator kiểm tra số điện thoại Việt Nam` → chạy dưới `agent: build`, bắt buộc RED trước GREEN.
5. `/debug Lỗi timeout khi chạy migration` → chạy dưới `agent: build`, theo 6 bước `systematic-debugging`.
6. `/verify` → chạy test/build/typecheck sau cùng trước khi chốt hoàn thành.
7. `/commit` → đọc `git diff --staged`, cảnh báo nếu có secrets/thay đổi lẫn lộn, viết Conventional Commit.

---

## 4. Cách Chạy Đánh Giá Nhanh

1. Mở một dự án thử nghiệm có cài `devkit-opencode`.
2. Gửi lần lượt 4–6 prompt ở Mục 1 và Mục 2 **không** nhắc tên skill trong câu hỏi.
3. Kiểm tra OpenCode có nạp đúng tên skill kỳ vọng không; nếu bị gọi nhầm, chỉnh lại câu chữ trong trường `description` của `SKILL.md` liên quan rồi chạy lại `python scripts/validate.py`.
