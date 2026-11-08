# Bài 07 — RDS: Cơ sở dữ liệu quan hệ được quản lý

## Mục tiêu bài học
- Hiểu `RDS (Relational Database Service)` là gì: database quan hệ (`SQL`) do AWS quản lý thay bạn.
- Phân biệt rạch ròi hai tính năng bị nhầm nhiều nhất đề SAA-C03: `Multi-AZ` và `Read Replica`.
- Nắm chính sách backup: `Automated backups` 1–35 ngày vs `Manual snapshots` giữ vô hạn.
- Nhớ bẫy `encryption` của RDS: phải bật lúc tạo DB, muốn mã hóa DB cũ phải đi đường vòng qua snapshot.
- Biết `RDS Proxy` dùng để làm gì ở mức khái niệm.

## Lý thuyết chính (tiếng Việt dễ hiểu, giữ nguyên thuật ngữ English)

### 1. RDS là gì?
RDS là dịch vụ database quan hệ được quản lý (`managed service`). Thay vì tự cài database lên EC2 rồi tự lo patch, backup, failover, bạn khai báo engine, dung lượng, và AWS lo phần vận hành nặng nhọc.

Các engine trong bài này:
- **MySQL**
- **PostgreSQL**
- **MariaDB**
- **Oracle**
- **Microsoft SQL Server**

**Aurora** cũng thuộc họ RDS nhưng đặc biệt hơn hẳn, nên được tách riêng sang Bài 08. Trong đề thi, thấy chữ Aurora là phải nghĩ đến các con số riêng của Aurora, không dùng giới hạn của RDS thường.

Bạn vẫn phải tự lo: chọn instance size, thiết kế schema, tối ưu câu query, và quyết định các tính năng HA/read scaling dưới đây.

### 2. Multi-AZ — cho High Availability, KHÔNG cho tăng tốc đọc
Đây là trọng tâm của domain Resilient (26%).

Khi bật `Multi-AZ deployment`, AWS tạo một bản **standby** (bản dự phòng) ở một `Availability Zone` khác trong cùng Region, và dữ liệu được đồng bộ **đồng bộ — `synchronous replication`** từ primary sang standby: ghi xong ở cả hai nơi mới coi là xong.

Khi primary hỏng (AZ sập, instance chết), RDS tự `failover`: đổi DNS sang standby, ứng dụng chỉ gián đoạn ngắn rồi chạy tiếp, thường không phải sửa connection string.

Điều phải khắc cốt ghi tâm:
- Standby **không nhận query đọc**. Nó chỉ ngồi chờ để tiếp quản.
- Vì vậy Multi-AZ = **High Availability / disaster recovery trong Region**, **KHÔNG tăng hiệu năng đọc, KHÔNG giảm tải cho primary**.

### 3. Read Replica — cho tăng tốc đọc, KHÔNG phải để failover chính
`Read Replica` là một bản sao chỉ-đọc (`read-only`) của database chính, dữ liệu được sao chép **bất đồng bộ — `asynchronous replication`** (có độ trễ nhỏ, `replication lag`).

- Mục đích: chia tải đọc. App có 90% query là SELECT (xem sản phẩm, đọc báo cáo) thì đẩy phần đọc sang replica, primary nhẹ hẳn.
- Replica có thể đặt ở **AZ khác, thậm chí Region khác** (`cross-Region read replica`).
- **Tối đa 15 Read Replicas** cho RDS (MySQL, PostgreSQL...).
- Replica có thể được promote (thăng cấp) thành DB độc lập khi cần, nhưng đó không phải cơ chế failover tự động mượt như Multi-AZ.

Một kiến trúc chuẩn trong đề: **Multi-AZ để chống sập + Read Replica để scale đọc** — hai tính năng bổ sung cho nhau, không thay thế nhau.

### 4. Backup — Automated Backups vs Manual Snapshots
- **Automated backups:** RDS tự backup hàng ngày + giữ `transaction logs`, cho phép khôi phục về một thời điểm bất kỳ (`point-in-time restore`) trong thời gian giữ. **Thời gian giữ (`retention period`): 1–35 ngày.** Hết 35 ngày là bản backup tự bị xóa.
- **Manual snapshots:** bạn tự bấm tạo (hoặc tạo qua script). **Giữ không giới hạn thời gian, cho đến khi bạn tự xóa.** Dùng cho mốc quan trọng cần giữ lâu: trước khi nâng cấp lớn, snapshot cuối năm để lưu trữ compliance.

Cần giữ backup quá 35 ngày → đề sẽ muốn bạn chọn manual snapshot (hoặc copy automated backup đi nơi khác), không có cách kéo automated retention lên vô hạn.

### 5. Encryption — bẫy kinh điển, phải bật lúc TẠO DB
RDS encryption (`encryption at rest` bằng KMS) **chỉ bật được tại thời điểm tạo database**. Một DB đã tạo mà chưa mã hóa thì **không có nút bấm để bật encryption lên sau**.

Muốn mã hóa một DB cũ đang chạy, quy trình bắt buộc trong đề thi là:
1. Tạo `snapshot` của DB chưa mã hóa.
2. **Copy snapshot đó và bật encryption** trong lúc copy (`encrypted copy`).
3. **Restore** một DB mới từ snapshot đã mã hóa.
4. Chuyển ứng dụng sang DB mới.

Thấy đề hỏi "existing unencrypted RDS database must be encrypted" → đáp án luôn là chuỗi 3 bước snapshot → copy encrypted → restore này.

Lưu ý thêm: bật Multi-AZ hay tạo Read Replica đều không tự biến DB chưa mã hóa thành đã mã hóa.

### 6. RDS Proxy — gom connection cho Lambda (mức khái niệm)
Database quan hệ có giới hạn số `connection` đồng thời. `AWS Lambda` thì mỗi lần chạy lại mở connection mới, hàng nghìn function chạy cùng lúc sẽ làm DB quá tải connection ("too many connections").

`RDS Proxy` là một lớp trung gian đứng giữa app/Lambda và RDS: nó **gom và tái sử dụng connection** (`connection pooling`), giảm số connection thực sự mở vào DB, đồng thời giúp failover êm hơn. Trong đề, thấy tổ hợp "Lambda + RDS + quá nhiều connection" → nghĩ ngay RDS Proxy.

## Ví dụ đời thường
Tưởng tượng bạn mở một nhà hàng bún chả đông khách ở Hà Nội.

`Multi-AZ` giống như bạn thuê sẵn một mặt bằng dự phòng ở quận khác, bếp bên đó được cập nhật thực đơn và nguyên liệu **y hệt, ngay lập tức** (synchronous). Quán chính bị mất điện thì bạn dắt khách sang quán dự phòng trong ít phút. Nhưng khi quán chính đang hoạt động bình thường, quán dự phòng **không bán hàng** — nó chỉ đứng chờ. Khách đông hơn không làm quán chính đỡ đông nhờ quán dự phòng. Đó là lý do Multi-AZ không tăng tốc đọc.

`Read Replica` giống như bạn mở thêm các quầy "chỉ bán mang về / chỉ xem menu" xung quanh thành phố. Nguyên liệu được xe chở sang định kỳ nên có thể chậm hơn quán chính vài phút (asynchronous). Khách chỉ đến xem menu, hỏi giá (đọc) thì ghé quầy phụ, bếp chính rảnh tay lo nấu (ghi). Bạn mở được tới 15 quầy phụ như vậy, kể cả ở tỉnh khác.

`Automated backup 1–35 ngày` như camera an ninh của quán tự ghi hình và chỉ giữ 35 ngày gần nhất. Còn `manual snapshot` như bạn tự chụp lại sổ sách kế toán cuối năm và cất vào két — giữ bao lâu tùy bạn, không ai tự xóa.

## Phân biệt dễ nhầm
| Tiêu chí | Multi-AZ | Read Replica |
|---|---|---|
| Mục đích chính | High Availability, failover | Tăng tốc / mở rộng đọc (read scaling) |
| Đồng bộ | Synchronous (đồng bộ) | Asynchronous (bất đồng bộ, có lag) |
| Đọc được không? | **Không** — standby không phục vụ query | **Có** — chỉ phục vụ đọc |
| Phạm vi | AZ khác, cùng Region | Khác AZ, khác cả Region được |
| Failover | Tự động, đổi DNS | Không tự động; promote thủ công khi cần |

Phân biệt thêm:
- **Automated backup vs Manual snapshot:** 1–35 ngày, tự xóa vs giữ vô hạn đến khi tự xóa.
- **RDS thường vs Aurora:** RDS thường tối đa 15 Read Replicas và backup theo snapshot; Aurora (Bài 08) storage tới 128 TB, cũng 15 replicas nhưng kiến trúc khác hẳn. Đừng lẫn giới hạn giữa hai bên khi đề nhắc đích danh engine.

## Bẫy đề thi
- Đề hỏi "improve read performance / handle read-heavy workload" mà đáp án chọn Multi-AZ → **sai**. Phải là Read Replica.
- Đề hỏi "ensure database availability if an AZ fails / automatic failover" mà đáp án chọn Read Replica → **thiếu**. Phải là Multi-AZ.
- Con số phải thuộc: **Read Replica tối đa 15**, **automated backup retention 1–35 ngày**, manual snapshot **không giới hạn**.
- "Encrypt an existing unencrypted RDS instance" → không có đáp án "enable encryption in settings". Đáp án đúng là **snapshot → encrypted copy → restore**.
- Tổ hợp `Lambda + too many database connections` → **RDS Proxy**.
- Multi-AZ standby không đọc được — câu bẫy xuất hiện trong đề dưới dạng "use the standby instance to serve read queries to reduce cost". Sai hoàn toàn.

## Tóm tắt 5 dòng
RDS là SQL database được quản lý, gồm MySQL, PostgreSQL, MariaDB, Oracle, SQL Server (Aurora học riêng ở Bài 08).
Multi-AZ là standby đồng bộ ở AZ khác để HA/failover, không hề tăng tốc đọc.
Read Replica là bản sao bất đồng bộ để scale đọc, đặt được ở Region khác, tối đa 15 replicas.
Automated backups giữ 1–35 ngày, manual snapshots giữ vô hạn đến khi tự xóa.
Encryption phải bật lúc tạo DB; DB cũ muốn mã hóa phải snapshot → copy có encryption → restore, còn Lambda nhiều connection thì dùng RDS Proxy.

## Quiz — 5 câu hỏi tiếng Anh kiểu đề thi (A/B/C/D)

**Question 1.** A company's RDS for MySQL database experiences heavy read traffic that slows down the primary instance. The company wants to scale read performance without changing the write workload. What is the best solution?
A. Enable Multi-AZ deployment
B. Create Read Replicas and direct read queries to them
C. Enable automated backups with 35-day retention
D. Increase the retention period of manual snapshots

**Question 2.** An RDS database must remain available with automatic failover if an Availability Zone becomes unavailable. Which feature should be enabled?
A. Read Replica in another Region
B. RDS Proxy
C. Multi-AZ deployment with a synchronous standby
D. Manual snapshots taken daily

**Question 3.** An existing RDS database was created without encryption. A new compliance rule requires encryption at rest. How can this be achieved?
A. Enable encryption in the RDS console for the running instance
B. Turn on Multi-AZ and the standby will be encrypted
C. Create a snapshot, copy it with encryption enabled, then restore a new DB from the encrypted copy
D. Create a Read Replica with encryption enabled

**Question 4.** Hundreds of AWS Lambda functions connect directly to an RDS database and frequently cause "too many connections" errors. Which service should be placed between Lambda and RDS?
A. Amazon EFS
B. RDS Proxy
C. S3 Transfer Acceleration
D. DynamoDB DAX

**Question 5.** A company needs to retain an RDS backup for 2 years for year-end auditing. Automated backups are already enabled. What should the company do?
A. Set the automated backup retention period to 730 days
B. Create a manual snapshot and keep it until it is no longer needed
C. Enable Multi-AZ deployment
D. Create a Read Replica in another Region

## Đáp án quiz

**Câu 1 — Đáp án B.** Tải đọc nặng (`read-heavy`) là bài toán của Read Replica: sao chép bất đồng bộ, phục vụ query đọc, tối đa 15 replicas. Multi-AZ chỉ để failover, standby của nó không đọc được nên không giảm tải chút nào.

**Câu 2 — Đáp án C.** Yêu cầu "automatic failover khi 1 AZ sập" là định nghĩa của Multi-AZ: standby đồng bộ (`synchronous`) ở AZ khác, RDS tự đổi DNS sang standby. Read Replica ở Region khác phục vụ đọc và không tự failover thay primary theo cách này.

**Câu 3 — Đáp án C.** Đây là bẫy nổi tiếng nhất của RDS: encryption chỉ bật được lúc tạo DB. Với DB cũ chưa mã hóa, quy trình duy nhất đúng là snapshot → copy snapshot có bật encryption → restore DB mới từ bản copy đó.

**Câu 4 — Đáp án B.** RDS Proxy làm `connection pooling` — gom và tái sử dụng connection giữa Lambda và RDS, giải quyết đúng lỗi "too many connections". Các đáp án còn lại không liên quan đến connection của RDS.

**Câu 5 — Đáp án B.** Automated backups tối đa chỉ giữ 35 ngày, không đặt được 730 ngày. Muốn giữ backup 2 năm phải tạo manual snapshot — loại này giữ không giới hạn cho đến khi bạn tự xóa.
