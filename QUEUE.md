# QUEUE — Hàng đợi việc

> Repo công khai — không ghi dữ liệu cá nhân/nhạy cảm, không tên thật, không email, không ID/link Drive, không số tiền.

## Việc hiện tại

| ID | Việc | Người làm | Trạng thái | Cần ai duyệt | Ghi chú |
|---|---|---|---|---|---|
| MP003-P3 | Xác minh scheduler chạy tự động 04.11.2026; dừng/xóa scheduler hạn 10.11.2026 | Minh (xác minh), Owner (dừng/xóa) | CHỜ 04.11 | Owner | Lịch chạy 04.11 10:06Z; Minh kiểm 04.11 10:20Z (cũng là MP005-P1-b). Dừng/xóa scheduler chỉ Owner làm |
| MP004-T1 | Báo cáo trạng thái sau P3 | Minh | CHỜ P3 | Owner (nhận báo cáo) | CẦN XÁC NHẬN: làm riêng hay gộp vào bảng hiện trạng của MP005-P1 |
| MP004-T3 | Workspace tối thiểu (QUEUE.md, AUTHORITY.md, README.md) | Minh/Tín | XONG 03.11.2026 | Tín kiểm sạch → Kiến nghiệm thu → Owner merge | PR #1 merge (ec8b5b7); Kiến nghiệm thu ĐẠT |
| MP004-T4 | Pilot sản phẩm thực tế | Minh/Tín (qua MP005-P2d) | CHỜ MP005-P2d | Kiến, Owner | Gộp vào MP005-P2d (hồ sơ pilot) rồi MP005-P4; không làm riêng |
| MP004-D3 | Quyết định quyền Drive `create_file` | Owner | CHỜ P3 | Owner | — |
| S1 | Công cụ kiểm trước PR (`pr-check`) | Minh/Tín | XONG 03.11.2026 | Tín kiểm sạch → Kiến nghiệm thu → Owner merge | PR #2 merge (afbfdd7); PR thử #3, #4, #5 đúng kỳ vọng, đóng không merge; required check `pr-check` trên main (kiểm 18:54Z và 18:58Z) |
| AEC-PQ | Phân quyền kỹ thuật vào AUTHORITY.md | Minh | XONG 03.11.2026 | Owner (quyết + merge) | PR #6 merge (609e9db) |
| MP005-T1 | Kiểm kê + kế hoạch P1–P5 + luồng S1 | Minh | XONG 03.11.2026 (không PR) | Kiến | Kiến nhận, giao S1 |
| MP005-T2 | Kiểm kê chỉ-đọc WSL (P1-a) | Minh/Tín; Owner duyệt chạy 1 lần | XONG 03.11.2026 (không PR) | Kiến | PASS; chạy 03.11 17:35Z; vùng quét không đổi |
| MP005-P2a | Overview v2 | Minh/Tín | ĐANG LÀM | Tín kiểm sạch → Kiến nghiệm thu | Bản mới trên Drive, không ghi đè bản cũ |
| MP005-P2b | QUEUE.md mới (file này) + sửa AUTHORITY.md mục Luồng | Minh/Tín | ĐANG LÀM | Tín kiểm sạch → Kiến nghiệm thu → Owner merge | Nhánh `claude/*` + PR |
| MP005-P2c | Đối chiếu một nguồn sự thật (Overview, Registry, QUEUE, AUTHORITY) | Minh, Tín sạch | ĐANG LÀM | Kiến | — |
| MP005-P2d | Hồ sơ pilot sản phẩm | Minh/Tín | ĐANG LÀM (chỉ đọc) | Kiến đề xuất → Owner quyết | Thay MP004-T4; hồ sơ đã có, trình cùng bản tổng hợp P2 |
| MP005-P3 | Tối ưu quyền: `.claude/settings.json` Tầng 1 | Minh/Tín | CHỜ P2 xong + MP003 đóng | Tín kiểm sạch → Kiến nghiệm thu → Owner merge | Đổi cấu hình = mức B |
| MP005-P4 | Pilot sản phẩm | Tín | CHỜ P3 xong + Owner quyết pilot | Kiến, Owner | — |
| MP005-P5 | Tự động hóa (báo cáo tuần, scheduled task chỉ đọc) | Minh | CHỜ P4 xong | Owner (OK từng task) | Báo cáo tuần đang tắt từ 28.10 |

**Trạng thái dùng:** ĐANG CHỜ · CHỜ <điều kiện> · ĐANG LÀM … · XONG <ngày> · BLOCKED. Giờ ghi theo UTC (Z).
Khi xong, không xóa dòng mà đổi Trạng thái thành `XONG <ngày>` và ghi nguồn (PR/báo cáo) ở Ghi chú.

## Cách thêm việc

1. Dự án mới: Kiến đề xuất + thẩm định, chỉ vào hàng đợi khi **Owner đã quyết làm**. Việc thường trong dự án đã duyệt: Owner giao bằng lệnh GIAO. Im lặng không phải đồng ý.
2. Minh thêm dòng trên nhánh `claude/*` và mở PR; `pr-check` phải đạt; Owner merge. Không sửa thẳng `main`.
3. Mỗi dòng phải đủ 6 cột. Chưa rõ thì ghi `CẦN XÁC NHẬN`, không tự đặt hạn hay con số.
