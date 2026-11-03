# QUEUE — Hàng đợi việc

> Repo công khai — không ghi dữ liệu cá nhân/nhạy cảm, không ID/link Drive, không số tiền.

## Việc hiện tại

| ID | Việc | Người làm | Trạng thái | Cần ai duyệt | Ghi chú |
|---|---|---|---|---|---|
| MP003-P3 | Xác minh scheduler chạy tự động 04.11.2026; dừng/xóa scheduler hạn 10.11.2026 | Minh (xác minh), Owner (dừng/xóa) | ĐANG CHỜ | Owner | Dừng/xóa scheduler chỉ Owner làm |
| MP004-T1 | Báo cáo trạng thái sau P3 | Minh | CHỜ P3 | Owner (nhận báo cáo) | — |
| MP004-T3 | Workspace tối thiểu (QUEUE.md, AUTHORITY.md, README.md) | Minh/Tín | ĐANG LÀM (PR #1) | Tín kiểm sạch → Kiến nghiệm thu → Owner merge | "Xong" = Owner merge |
| MP004-T4 | Pilot sản phẩm thực tế | chưa chọn | CHỜ Kiến đề xuất + Owner quyết | Kiến, Owner | — |
| MP004-D3 | Quyết định quyền Drive `create_file` | Owner | CHỜ P3 | Owner | — |

**Trạng thái dùng:** ĐANG CHỜ · CHỜ <điều kiện> · ĐANG LÀM · XONG · BLOCKED.
Khi xong, không xóa dòng mà đổi Trạng thái thành `XONG <ngày>` và ghi nguồn (PR/báo cáo) ở Ghi chú.

## Cách thêm việc

1. Việc mới bắt đầu từ đề xuất của Kiến và chỉ vào hàng đợi khi **Owner đã quyết làm**. Im lặng không phải đồng ý.
2. Minh thêm dòng trên nhánh `claude/*` và mở PR. Không sửa thẳng `main`.
3. Mỗi dòng phải đủ 6 cột. Chưa rõ thì ghi `CẦN XÁC NHẬN`, không tự đặt hạn hay con số.
4. Không ghi dữ liệu cá nhân/nhạy cảm, ID/link Drive hay số tiền vào bảng.
