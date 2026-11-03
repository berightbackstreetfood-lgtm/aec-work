# QUEUE — Hàng đợi việc

> Repo công khai — không ghi dữ liệu cá nhân/nhạy cảm, không tên thật, không email, không ID/link Drive, không số tiền.

## Việc hiện tại

| ID | Việc | Người làm | Trạng thái | Cần ai duyệt | Ghi chú |
|---|---|---|---|---|---|
| MP003-P3 | Xác minh scheduler chạy tự động; dừng/xóa scheduler | Minh (xác minh), Owner (đổi lịch, tắt, xóa) | XONG 03.11.2026 | Kiến nghiệm thu, Owner | Owner dời lịch sang 03.11 22:00 Vienna; scheduled fire 21:06Z SUCCEEDED, NO-OP (0 file mới); Owner tắt rồi xóa scheduler sau khi lưu bằng chứng (báo cáo bằng chứng trên Drive, không đưa ID vào repo) |
| MP004-T1 | Báo cáo trạng thái sau P3 | Minh | CHỜ Owner chọn cách báo cáo (P3 đã xong) | Owner (nhận báo cáo) | CẦN XÁC NHẬN: làm riêng hay gộp vào bảng hiện trạng của MP005-P1 |
| MP004-T3 | Workspace tối thiểu (QUEUE.md, AUTHORITY.md, README.md) | Minh/Tín | XONG 03.11.2026 | Tín kiểm sạch → Kiến nghiệm thu → Owner merge | PR #1 merge (ec8b5b7); Kiến nghiệm thu ĐẠT |
| MP004-T4 | Pilot sản phẩm thực tế | Minh/Tín (qua MP005-P2d) | CHỜ MP005-P2d | Kiến, Owner | Gộp vào MP005-P2d (hồ sơ pilot) rồi MP005-P4; không làm riêng |
| MP004-D3 | Quyết định quyền Drive `create_file` | Owner | CHỜ Owner quyết (P3 đã xong) | Owner | — |
| S1 | Công cụ kiểm trước PR (`pr-check`) | Minh/Tín | XONG 03.11.2026 | Tín kiểm sạch → Kiến nghiệm thu → Owner merge | PR #2 merge (afbfdd7); PR thử #3, #4, #5 đúng kỳ vọng, đóng không merge; required check `pr-check` trên main (kiểm 18:54Z và 18:58Z) |
| AEC-PQ | Phân quyền kỹ thuật vào AUTHORITY.md | Minh | XONG 03.11.2026 | Owner (quyết + merge) | PR #6 merge (609e9db) |
| MP005-T1 | Kiểm kê + kế hoạch P1–P5 + luồng S1 | Minh | XONG 03.11.2026 (không PR) | Kiến | Kiến nhận, giao S1 |
| MP005-T2 | Kiểm kê chỉ-đọc WSL (P1-a) | Minh/Tín; Owner duyệt chạy 1 lần | XONG 03.11.2026 (không PR) | Kiến | PASS; chạy 03.11 17:35Z; vùng quét không đổi |
| MP005-P2a | Overview v2 | Minh/Tín | XONG 03.11.2026 | Tín kiểm sạch → Kiến nghiệm thu | Kiến ĐẠT; bản mới trên Drive, không ghi đè bản cũ |
| MP005-P2b | QUEUE.md mới (file này) + sửa AUTHORITY.md mục Luồng | Minh/Tín | XONG 03.11.2026 | Tín kiểm sạch → Kiến nghiệm thu → Owner merge | PR #7 merge (bf7be6d); Kiến ĐẠT |
| MP005-P2c | Đối chiếu một nguồn sự thật (Overview, Registry, QUEUE, AUTHORITY) | Minh, Tín sạch | XONG 03.11.2026 | Kiến | Kiến ĐẠT |
| MP005-P2d | Hồ sơ pilot sản phẩm | Minh/Tín | XONG 03.11.2026 (thiết kế) | Kiến đề xuất → Owner quyết | Kiến ĐẠT; chọn menu-check làm ứng viên P4, HOÃN triển khai tới mốc phối hợp tự động |
| MP005-P2e | AI-BRIDGE v2: thử W0 (mỗi bên 1 task chạy 1 lần ghi 1 file vào thư mục pilot Drive) | Minh/Tín; Owner/Kiến (task ChatGPT) | ĐANG LÀM | Owner (Q1–Q3 đã OK) → Kiến nghiệm thu | Q1 thư mục: XONG; Q2 task ChatGPT: chạy 03.11 22:03Z; Q3 task Claude: BLOCKED (công cụ tạo task khác khuôn, đã tắt trước giờ chạy, Kiến chấp nhận). BRIDGE-P0 chưa được chạy |
| MP005-P3 | Tối ưu quyền: `.claude/settings.json` Tầng 1 | Minh/Tín | CHỜ Minh đề xuất (P2a–d xong, MP003 đóng) | Tín kiểm sạch → Kiến nghiệm thu → Owner merge | Đổi cấu hình = mức B |
| MP005-P4 | Pilot sản phẩm | Tín | CHỜ P3 xong + Owner quyết pilot | Kiến, Owner | — |
| MP005-P5 | Tự động hóa (báo cáo tuần, scheduled task chỉ đọc) | Minh | CHỜ P4 xong | Owner (OK từng task) | Báo cáo tuần đang tắt từ 28.10 |

**Trạng thái dùng:** ĐANG CHỜ · CHỜ <điều kiện> · ĐANG LÀM … · XONG <ngày> · BLOCKED. Giờ ghi theo UTC (Z).
Khi xong, không xóa dòng mà đổi Trạng thái thành `XONG <ngày>` và ghi nguồn (PR/báo cáo) ở Ghi chú.

## Cách thêm việc

1. Dự án mới: Kiến đề xuất + thẩm định, chỉ vào hàng đợi khi **Owner đã quyết làm**. Việc thường trong dự án đã duyệt: Owner giao bằng lệnh GIAO. Im lặng không phải đồng ý.
2. Minh thêm dòng trên nhánh `claude/*` và mở PR; `pr-check` phải đạt; Owner merge. Không sửa thẳng `main`.
3. Mỗi dòng phải đủ 6 cột. Chưa rõ thì ghi `CẦN XÁC NHẬN`, không tự đặt hạn hay con số.
