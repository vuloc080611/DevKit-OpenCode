# Khung Báo Cáo Đồ Án / Bài Tập Lớn Chuẩn (Capstone Report Template)

Tài liệu tham khảo cho `assignment-helper` giúp sinh viên trình bày báo cáo logic, bám sát code thật và sẵn sàng bảo vệ trước hội đồng.

## Cấu Trúc Chương Chuẩn

### Chương 1: Tổng quan đề tài
1.1. Đặt vấn đề & Lý do chọn đề tài (bài toán thực tế giải quyết vấn đề gì?)  
1.2. Mục tiêu & Phạm vi đề tài (liệt kê rõ chức năng cốt lõi vs ngoài phạm vi)  
1.3. Đối tượng sử dụng & Quy trình nghiệp vụ hiện tại  
1.4. Công nghệ lựa chọn & Lý do (so sánh ngắn gọn thay vì chỉ liệt kê tên công nghệ)

### Chương 2: Phân tích & Thiết kế hệ thống
2.1. Yêu cầu chức năng (bảng Use Case / User Stories theo từng vai trò)  
2.2. Yêu cầu phi chức năng (bảo mật, hiệu năng, sao lưu, responsive...)  
2.3. Kiến trúc tổng thể (Frontend ↔ Backend ↔ Database ↔ External Services)  
2.4. Thiết kế cơ sở dữ liệu (Sơ đồ ERD + mô tả chi tiết bảng, khóa chính/ngoại, ràng buộc toàn vẹn, index)  
2.5. Thiết kế API / Module chính & Sơ đồ tuần tự (Sequence Diagram cho 2–3 luồng quan trọng nhất)

### Chương 3: Cài đặt & Triển khai
3.1. Cấu trúc mã nguồn dự án (giải thích vai trò từng thư mục chính)  
3.2. Các module / thuật toán trọng tâm đã hiện thực (trích ngắn gọn logic cốt lõi, xử lý edge case, transaction/auth)  
3.3. Đóng gói & Môi trường chạy (`.env.example`, Docker Compose / hướng dẫn chạy local tái lập được)

### Chương 4: Kiểm thử & Đánh giá (Chỉ dùng số liệu thật!)
4.1. Chiến lược kiểm thử (Unit test / Integration test / Manual test case)  
4.2. Bảng tổng hợp Test Cases thực tế:

| ID | Kịch bản kiểm thử | Đầu vào | Kết quả kỳ vọng | Kết quả thực tế | Trạng thái |
|---|---|---|---|---|---|
| TC-01 | ... | ... | ... | *(Ghi đúng output quan sát được)* | Pass / Fail |

4.3. Hạn chế hiện tại của hệ thống (trung thực nêu rõ phần nào chưa làm hoặc cần cải thiện)

### Chương 5: Kết luận & Hướng phát triển
5.1. Kết quả đạt được đối chiếu với mục tiêu Chương 1  
5.2. Hướng mở rộng tiếp theo (tính năng, tối ưu, CI/CD...)

---

## Checklist Chuẩn Bị Bảo Vệ (Viva / Q&A)
- Giải thích được **luồng đi của 1 request từ UI → Controller → Service → DB → Response**.
- Giải thích được **tại sao chọn schema/quan hệ bảng và index đó**.
- Chỉ ra được **ít nhất 2 edge case hoặc lỗ hổng bảo mật đã xử lý** (ví dụ: race condition, IDOR, validation, hash mật khẩu).
- Demo được kịch bản **lỗi** (nhập sai, mất quyền, dữ liệu trùng) chứ không chỉ happy path.
