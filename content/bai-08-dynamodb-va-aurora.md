# Bài 08 — DynamoDB & Aurora: NoSQL tốc độ cao và SQL “xịn” của AWS

## Mục tiêu bài học
- Hiểu `DynamoDB` là database `NoSQL` key-value/document, khi nào bỏ SQL để chọn DynamoDB.
- Nắm `partition key` + `sort key`, hai chế độ `Provisioned` vs `On-Demand`, và phân biệt `Strongly` vs `Eventually consistent reads`.
- Biết `DAX`, `DynamoDB Streams`, `Global Tables`, `TTL` giải quyết bài toán gì.
- Hiểu `Aurora` hơn RDS thường ở điểm nào: storage 128 TB, 15 replicas, `Aurora Serverless`, `Aurora Global Database`.
- Có bảng so sánh nhanh RDS vs Aurora vs DynamoDB để chốt đáp án khi đề cho tình huống lẫn lộn.

## Lý thuyết chính (tiếng Việt dễ hiểu, giữ nguyên thuật ngữ English)

### Phần A — DynamoDB: NoSQL không cần server để quản

DynamoDB là database NoSQL được quản lý hoàn toàn (`serverless` ở góc độ vận hành — bạn không quản lý instance nào cả). Nó lưu dữ liệu dạng `key-value` và `document`.

**Khóa chính (primary key) gồm:**
- `Partition key` (bắt buộc): quyết định dữ liệu nằm ở phân vùng nào. Chọn partition key tốt (phân tán đều) là yếu tố sống còn về hiệu năng.
- `Sort key` (tùy chọn): kết hợp partition key + sort key tạo khóa ghép. Cùng một partition key có thể có nhiều item khác nhau theo sort key, và query theo khoảng sort key rất nhanh. Ví dụ: partition key = `user_id`, sort key = `order_date`.

**Capacity — hai cách trả tiền cho thông lượng:**
- **Provisioned capacity:** bạn khai báo trước số `RCU/WCU` (đơn vị đọc/ghi mỗi giây). Rẻ hơn nếu tải ổn định, đoán trước được. Khai báo thiếu thì bị `throttling` (từ chối request).
- **On-Demand capacity:** không khai báo gì, dùng bao nhiêu trả bấy nhiêu, tự co giãn theo tải tăng đột biến. Đắt hơn theo đơn vị, phù hợp tải không đều, khó đoán, app mới.

**Mức nhất quán khi đọc (consistency):**
- **Eventually consistent reads (mặc định):** đọc có thể nhận dữ liệu cũ hơn vài tích tắc sau khi ghi, đổi lại rẻ hơn và nhanh hơn. Phù hợp đa số trường hợp.
- **Strongly consistent reads:** đọc luôn nhận dữ liệu mới nhất vừa ghi. Tốn capacity gấp đôi. Chỉ chọn khi đề nhấn mạnh "must read the latest data immediately after a write".

**Các tính năng hay thi của DynamoDB:**
- **DAX (DynamoDB Accelerator):** cache `in-memory` nằm trước DynamoDB, giảm độ trễ đọc xuống mức **microsecond** (micro-giây). Từ khóa nhận diện: "microsecond latency", "in-memory cache for DynamoDB".
- **DynamoDB Streams:** dòng sự kiện ghi lại mọi thay đổi (thêm/sửa/xóa item) theo thứ tự thời gian. Thường kết hợp Lambda để xử lý sự kiện: item mới tạo → kích hoạt Lambda gửi thông báo, đồng bộ sang hệ thống khác.
- **Global Tables:** bảng DynamoDB trải nhiều Region theo mô hình **multi-Region active-active** — ghi ở Region nào cũng được, dữ liệu tự đồng bộ sang các Region còn lại. Khác hẳn mô hình primary-standby thụ động.
- **TTL (Time To Live):** đặt một thuộc tính thời gian hết hạn cho từng item, DynamoDB **tự xóa item khi hết hạn** mà không tốn công bạn viết job dọn dẹp. Dùng cho session, giỏ hàng tạm, dữ liệu chỉ có giá trị trong 24 giờ...

### Phần B — Aurora: database quan hệ do AWS tự xây

Aurora thuộc họ RDS nhưng là engine riêng của AWS, **tương thích với MySQL và PostgreSQL** (`MySQL-compatible`, `PostgreSQL-compatible`) — app đang dùng MySQL/PostgreSQL chuyển sang Aurora gần như không phải sửa code.

Điểm vượt trội phải nhớ:
- **Storage tự tăng tới 128 TB:** lớp lưu trữ của Aurora tự động mở rộng theo dữ liệu, bạn không phải cấp phát dung lượng trước như RDS thường.
- **Tối đa 15 Aurora Replicas:** các replica đọc dùng chung lớp storage với primary nên độ trễ sao chép rất thấp. Con số 15 này trùng với Read Replica của RDS thường, nhưng kiến trúc bên dưới khác nhau.
- **Backup liên tục + Point-in-Time Restore:** Aurora backup liên tục lên S3, cho phép khôi phục về **bất kỳ thời điểm nào** trong cửa sổ backup (`point-in-time restore`).
- **Aurora Serverless:** phiên bản tự co giãn — tự tăng/giảm capacity theo tải, tự về mức rất thấp khi không có tải. Sinh ra cho **tải không đều, khó đoán** (app lúc cao điểm lúc vắng, môi trường dev/test chạy không liên tục). Từ khóa đề: "unpredictable / intermittent workload".
- **Aurora Global Database:** triển khai Aurora qua nhiều Region, replication sang Region phụ với **độ trễ thường dưới 1 giây (`typically less than 1 second`)**. Dùng cho ứng dụng toàn cầu và disaster recovery xuyên Region.

### Bảng so sánh nhanh RDS vs Aurora vs DynamoDB

| Tiêu chí | RDS (thường) | Aurora | DynamoDB |
|---|---|---|---|
| Loại dữ liệu | Quan hệ (SQL) | Quan hệ (SQL) | NoSQL key-value / document |
| Engine | MySQL, PostgreSQL, MariaDB, Oracle, SQL Server | Tương thích MySQL / PostgreSQL | Engine riêng của AWS |
| Replicas đọc | Tối đa 15 Read Replicas | Tối đa 15 Aurora Replicas | Không dùng khái niệm replica kiểu này |
| Storage | Cấp phát trước (EBS) | Tự tăng tới 128 TB | Serverless, không quản lý storage |
| Multi-Region nổi bật | Cross-Region Read Replica | Aurora Global Database (lag thường < 1s) | Global Tables (active-active) |
| Co giãn tự động | Hạn chế | Có Aurora Serverless | Có On-Demand capacity |
| Chọn khi | Cần Oracle / SQL Server, SQL truyền thống | Cần SQL hiệu năng cao, scale lớn, vẫn tương thích MySQL/PostgreSQL | Cần NoSQL scale cực lớn, latency thấp, không cần join phức tạp |

## Ví dụ đời thường
**DynamoDB** giống như tủ locker thông minh ở ga tàu. Mỗi locker có mã số riêng (`partition key`) — bạn chỉ cần biết mã là mở đúng ngăn trong tích tắc, không cần hỏi nhân viên, không cần đi qua từng quầy. Thêm mã phụ (`sort key`) giống như dãy locker của cùng một khách được xếp theo ngày gửi đồ. Ga có thêm 1 triệu khách thì AWS tự lắp thêm locker, bạn không phải xây nhà ga mới. Tờ giấy ghi giờ hết hạn gửi đồ chính là `TTL`: quá giờ, nhân viên tự dọn ngăn.

**DAX** là anh nhân viên đứng ngay cửa, nhớ sẵn những locker hay được mở nhất và đưa đồ ngay trong tích tắc (microsecond) thay vì bắt bạn đi vào tận kho.

**Aurora** thì giống một nhà hàng bạn quen: vẫn là món phở, công thức cũ của MySQL/PostgreSQL (tương thích), nhưng bếp được AWS thiết kế lại — nồi nước dùng tự to ra khi khách đông (storage tới 128 TB), có tới 15 quầy phụ phục vụ cùng một nồi nước (replica dùng chung storage). `Aurora Serverless` là kiểu nhà hàng chỉ mở bếp đúng số lượng khách đang có mặt: vắng khách thì bếp tự thu nhỏ, bạn không trả tiền cho bếp trống.

## Phân biệt dễ nhầm
| Cặp dễ nhầm | Cách phân biệt |
|---|---|
| Provisioned vs On-Demand (DynamoDB) | Provisioned: đặt trước RCU/WCU, rẻ khi tải đều. On-Demand: trả theo dùng, cho tải đột biến/khó đoán. |
| Strongly vs Eventually Consistent | Strongly: đọc ngay dữ liệu mới nhất, tốn gấp đôi capacity. Eventually: có thể cũ vài tích tắc, mặc định và rẻ hơn. |
| DAX vs ElastiCache (ngữ cảnh DynamoDB) | Đề nhắc cache riêng cho DynamoDB, microsecond → DAX. DAX chỉ dành cho DynamoDB. |
| Global Tables vs Global Database | Global Tables là của **DynamoDB**, active-active nhiều Region. Global Database là của **Aurora**. Hai tên rất giống nhau, đề cố tình để lẫn. |
| Aurora Replicas vs RDS Read Replicas | Cùng tối đa 15, nhưng Aurora Replicas dùng chung storage với primary nên lag rất thấp. |
| Aurora Serverless vs RDS thường | Tải không đều / intermittent / unpredictable → Serverless. Tải đều đặn 24/7 → bản thường có thể rẻ hơn. |

## Bẫy đề thi
- Thấy "microsecond latency for DynamoDB reads" → đáp án là **DAX**, không phải tăng Provisioned capacity.
- Thấy "automatically delete expired items / sessions at no extra cost" → **TTL** của DynamoDB.
- Thấy "capture changes to DynamoDB items and trigger processing" → **DynamoDB Streams** (thường + Lambda).
- Thấy "multi-Region, active-active, users write in their local Region" → **DynamoDB Global Tables**. Nếu là Aurora thì Global Database **không** phải active-active ghi nhiều nơi như vậy, nó là primary + secondary Region với lag < 1 giây.
- Đề cho Aurora: thuộc lòng 3 con số — **storage 128 TB, tối đa 15 replicas, Global Database lag thường < 1 giây**.
- App cần SQL và join phức tạp → đừng chọn DynamoDB dù nó scale tốt đến đâu. Ngược lại, app cần key-value scale cực lớn, không join → đừng gò vào RDS.
- "Unpredictable workload" cho database quan hệ → **Aurora Serverless**. Cùng từ khóa đó cho DynamoDB → **On-Demand capacity**.

## Tóm tắt 5 dòng
DynamoDB là NoSQL key-value/document với partition key + sort key, chọn Provisioned cho tải đều và On-Demand cho tải khó đoán.
Strongly consistent reads cho dữ liệu mới nhất tốn gấp đôi, eventually consistent là mặc định rẻ hơn; DAX cho latency microsecond, TTL tự xóa item hết hạn.
DynamoDB Streams bắt sự kiện thay đổi dữ liệu, Global Tables cho multi-Region active-active.
Aurora tương thích MySQL/PostgreSQL, storage tự tăng tới 128 TB, tối đa 15 replicas, backup liên tục kèm point-in-time restore.
Aurora Serverless hợp tải không đều, Aurora Global Database replication khác Region với lag thường dưới 1 giây.

## Quiz — 5 câu hỏi tiếng Anh kiểu đề thi (A/B/C/D)

**Question 1.** A DynamoDB-based application needs read latency in microseconds for frequently accessed items. Which feature should be implemented?
A. DynamoDB Streams
B. DynamoDB Accelerator (DAX)
C. Provisioned capacity with auto scaling
D. Strongly consistent reads

**Question 2.** A gaming company runs a DynamoDB table in three AWS Regions. Players must be able to read and write data in their nearest Region with changes replicated to the other Regions. Which feature provides this?
A. DynamoDB Global Tables
B. Aurora Global Database
C. S3 Cross-Region Replication
D. Read Replicas

**Question 3.** An application using Aurora experiences unpredictable workloads — very busy at launch events and almost idle at night. The company wants the database capacity to scale automatically and minimize costs during idle periods. Which option fits best?
A. RDS Multi-AZ with the largest instance class
B. Aurora Serverless
C. DynamoDB with Provisioned capacity
D. Aurora Global Database

**Question 4.** User session records stored in DynamoDB must be automatically deleted 24 hours after creation without running a custom cleanup job. Which feature should be used?
A. DynamoDB Streams
B. DAX
C. Time To Live (TTL)
D. Global Tables

**Question 5.** A company runs Aurora with a primary DB cluster in one Region and needs a secondary Region for disaster recovery and low-latency reads globally. Replication lag to the secondary Region should typically be under one second. Which feature should be used?
A. Aurora Global Database
B. DynamoDB Global Tables
C. RDS Manual Snapshots copied daily
D. S3 Lifecycle rules

## Đáp án quiz

**Câu 1 — Đáp án B.** Từ khóa `microseconds` chỉ thuộc về DAX — cache in-memory chuyên cho DynamoDB. Streams dùng để bắt sự kiện thay đổi, tăng capacity hay strongly consistent đều không đưa độ trễ xuống microsecond.

**Câu 2 — Đáp án A.** Ghi/đọc ở mọi Region (`active-active`) là đặc trưng của DynamoDB Global Tables. Aurora Global Database là cho database quan hệ Aurora (primary + secondary), không phải bảng DynamoDB, còn Read Replica là khái niệm của RDS.

**Câu 3 — Đáp án B.** Workload không đều, khó đoán (`unpredictable`), cần tự co giãn và rẻ khi idle — đây là mô tả chuẩn của Aurora Serverless. Chọn instance lớn cố định (đáp án A) sẽ lãng phí tiền lúc vắng khách.

**Câu 4 — Đáp án C.** TTL cho phép gắn thời gian hết hạn lên từng item, DynamoDB tự xóa item hết hạn — sinh ra đúng cho session, token, dữ liệu tạm 24 giờ. Không cần viết job dọn dẹp riêng.

**Câu 5 — Đáp án A.** Aurora Global Database replication sang Region phụ với độ trễ thường dưới 1 giây — con số `< 1 second` là keyword nhận diện trong đề. Global Tables là của DynamoDB nên loại ngay, snapshot copy hàng ngày thì độ trễ tính bằng giờ, không thể dưới 1 giây.
