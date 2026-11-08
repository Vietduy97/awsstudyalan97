# Bài 05 — S3: Lưu trữ đối tượng (Object Storage)

## Mục tiêu bài học
- Hiểu S3 là gì: `object storage`, khác hoàn toàn với ổ đĩa `block storage` như EBS.
- Nắm rõ 3 khái niệm gốc: `bucket`, `object`, `key`.
- Phân biệt được 7 `storage class` và biết chọn class nào cho rẻ mà vẫn đúng yêu cầu truy cập.
- Biết dùng `Versioning`, `Lifecycle rules`, `Replication`, `encryption` và `Presigned URL` đúng tình huống đề thi hay hỏi.
- Đọc được keyword tiếng Anh trong đề SAA-C03 và map về đúng tính năng S3.

## Lý thuyết chính (tiếng Việt dễ hiểu, giữ nguyên thuật ngữ English)

### 1. S3 là object storage
S3 (Simple Storage Service) là dịch vụ lưu file dạng `object`. Bạn không format ổ đĩa, không chia partition. Bạn chỉ tạo một `bucket` (như một thùng chứa), rồi ném file vào đó.

Mỗi file là một `object`, gồm dữ liệu + `metadata`. Tên đầy đủ của object trong bucket gọi là `key`. Ví dụ: bucket `anh-du-lich-da-lat`, key `2026/hue/mua-xuan.jpg` — nhìn giống đường dẫn thư mục nhưng thực chất S3 là phẳng (flat), dấu `/` chỉ để tổ chức cho dễ nhìn.

Điểm mạnh nhất của S3 là `durability` (độ bền dữ liệu) **99.999999999% — 11 số 9**. Hiểu đơn giản: nếu bạn lưu 10.000 object, trung bình 10 triệu năm mới mất 1 object. Lưu ý: durability khác `availability` (tính sẵn sàng để truy cập được). Đề thi rất hay bẫy hai chữ này.

### 2. Storage Classes — chọn class là chọn tiền
Đây là phần ăn điểm Cost-Optimized (20% đề thi).

- **S3 Standard:** mặc định, truy cập thường xuyên, đắt nhất trong nhóm Standard nhưng bền và nhanh.
- **S3 Standard-IA (Infrequent Access):** ít truy cập, rẻ hơn Standard, nhưng có phí khi lấy file ra (`retrieval fee`).
- **S3 One Zone-IA:** giống Standard-IA nhưng chỉ lưu ở 1 `Availability Zone (AZ)`. Rẻ hơn nữa, đổi lại AZ đó sập thì mất dữ liệu. Chỉ dùng cho dữ liệu tạo lại được.
- **S3 Glacier Instant Retrieval:** lưu trữ lạnh (`archive`) nhưng cần lấy lại thì lấy ngay được (mili-giây). Phù hợp ảnh y tế, backup quý ít khi mở nhưng mở là cần ngay.
- **S3 Glacier Flexible Retrieval:** archive rẻ hơn, lấy lại mất từ vài phút đến vài giờ.
- **S3 Glacier Deep Archive:** rẻ nhất, cho dữ liệu giữ 7-10 năm vì luật. Lấy lại mất khoảng 12 giờ.
- **S3 Intelligent-Tiering:** không đoán được tần suất truy cập? Để AWS tự theo dõi và tự chuyển class giúp bạn, tốn thêm phí giám sát nhỏ nhưng tránh chọn sai.

Quy tắc nhớ: càng lạnh (cold) càng rẻ, càng lấy lại lâu và càng có phí retrieval.

### 3. Lifecycle Rules — tự động dọn nhà
`Lifecycle rules` cho phép bạn đặt luật tự động:
- Sau X ngày thì chuyển object sang class rẻ hơn. Ví dụ: 30 ngày Standard → 90 ngày Standard-IA → 1 năm Glacier Deep Archive.
- Sau X ngày thì tự xóa (`expiration`). Ví dụ: log chỉ giữ 90 ngày rồi xóa.

Đây là đáp án kinh điển khi đề hỏi "how to reduce S3 storage costs automatically?"

### 4. Versioning, MFA Delete và Object Lock — chống xóa nhầm, chống ransomware
- **Versioning:** bật lên thì mỗi lần ghi đè file, S3 giữ lại bản cũ. Xóa file thực ra chỉ tạo `delete marker`, vẫn khôi phục được bản trước. Tắt Versioning không xóa các version cũ.
- **MFA Delete:** muốn xóa vĩnh viễn một version hoặc tắt Versioning thì phải nhập mã `Multi-Factor Authentication`. Thêm một lớp chống xóa nhầm.
- **S3 Object Lock:** cơ chế `WORM` (Write Once, Read Many) — file đã khóa thì trong thời gian giữ (`retention period`) không ai xóa/sửa được, kể cả chủ tài khoản. Có 2 mode:
  - `Governance mode`: người có quyền đặc biệt vẫn gỡ khóa được.
  - `Compliance mode`: không ai gỡ được cho đến khi hết hạn — đáp án cho mọi câu hỏi về `compliance / regulatory requirement`.

### 5. Replication — sao chép sang bucket khác
- **CRR (Cross-Region Replication):** bucket nguồn và đích ở khác `Region`.
- **SRR (Same-Region Replication):** hai bucket cùng Region.

Điều kiện bắt buộc cho cả hai: **phải bật Versioning ở cả bucket nguồn và bucket đích**. Replication là bất đồng bộ (`asynchronous`). Chỉ object mới tạo sau khi bật replication mới được sao tự động, object cũ muốn sao phải dùng cách khác (S3 Batch Replication) — đây là bẫy hay gặp.

### 6. Encryption — mã hóa
- **SSE-S3:** S3 tự quản lý key, mã hóa bằng AES-256. Mặc định, ít việc nhất.
- **SSE-KMS:** dùng AWS KMS key. Kiểm soát được ai dùng key, có log trong CloudTrail. Đáp án khi đề nhắc `audit`, `control access to encryption keys`.
- **SSE-C:** khách hàng tự mang key (`customer-provided key`), gửi kèm mỗi request. AWS không lưu key của bạn.
- **Client-side encryption:** bạn tự mã hóa file trước khi upload lên S3, S3 chỉ thấy dữ liệu đã mã hóa.

### 7. Ai được truy cập? Bucket Policy, ACL và Block Public Access
- **Bucket policy:** file JSON gắn vào bucket, quyết định ai (user, account, IP...) được/không được làm gì. Đây là cách chính, nên ưu tiên dùng. Là `resource-based policy`.
- **ACL (Access Control List):** cơ chế cũ, gắn vào từng object/bucket, kiểm soát thô hơn. Đề thi hiện nay ưu tiên bucket policy, ACL thường là đáp án sai nếu có lựa chọn bucket policy.
- **S3 Block Public Access:** công tắc chặn toàn bộ truy cập public ở cấp account hoặc bucket. Khi đề nói "ensure bucket is never public", hãy nghĩ đến tính năng này.

### 8. Presigned URL và các tính năng hay thi
- **Presigned URL:** tạo một link tạm thời có chữ ký, có thời hạn hết hạn, để người ngoài (không có tài khoản AWS) vẫn download/upload được 1 object riêng tư. Ví dụ: cho khách tải hóa đơn trong 15 phút. Hết hạn là link vô dụng.
- **Static website hosting:** bật lên, bucket thành web server tĩnh chứa HTML/CSS/JS. Không chạy được code phía server như PHP.
- **S3 Transfer Acceleration:** ở mức khái niệm, tính năng này dùng mạng biên (edge locations) của CloudFront để upload file từ xa về bucket nhanh hơn khi người dùng ở cách xa Region của bucket.

## Ví dụ đời thường
Hãy hình dung S3 như một **kho giữ đồ khổng lồ ở sân bay**.

Bucket là một gian kho bạn thuê, có tên duy nhất toàn cầu như biển số xe — không ai trùng được. Object là từng vali bạn gửi vào kho, key là mã tem dán trên vali để nhân viên tìm ra ngay.

Storage class giống như vị trí để vali: để ngay cửa kho (Standard) thì lấy nhanh nhưng tiền thuê chỗ đắt. Để sâu trong kho lạnh (Glacier Deep Archive) thì siêu rẻ, nhưng khi cần lấy phải hẹn trước nửa ngày để nhân viên đi tìm.

Lifecycle rule là tờ giấy bạn dặn quản kho: "Vali nào để quá 30 ngày không ai đụng thì tự chuyển vào kho rẻ phía sau, quá 1 năm thì hủy." Bạn không phải tự đi kiểm tra từng ngày.

Presigned URL giống như bạn viết giấy ủy quyền có ghi rõ "giấy này chỉ có giá trị đến 17h hôm nay, chỉ được lấy đúng vali số 12" rồi đưa cho shipper. Shipper không cần chìa khóa kho, hết giờ giấy tự hết giá trị.

## Phân biệt dễ nhầm
| Cặp dễ nhầm | Cách phân biệt |
|---|---|
| Durability vs Availability | Durability 11 số 9 là **không mất dữ liệu**. Availability là **truy cập được ngay lúc đó hay không**. |
| Standard-IA vs One Zone-IA | Standard-IA lưu ở nhiều AZ. One Zone-IA chỉ 1 AZ nên rẻ hơn nhưng rủi ro mất dữ liệu cao hơn. |
| Glacier Instant vs Flexible vs Deep Archive | Instant: lấy ngay. Flexible: vài phút – vài giờ. Deep Archive: ~12 giờ, rẻ nhất. |
| SSE-S3 vs SSE-KMS vs SSE-C | S3 giữ key / KMS giữ key có audit / bạn tự mang key theo mỗi request. |
| Bucket Policy vs ACL | Bucket Policy là JSON, hiện đại, kiểm soát chi tiết cho cả bucket — ưu tiên. ACL là cách cũ, thô. |
| Versioning vs Object Lock | Versioning giữ lại bản cũ, vẫn xóa được. Object Lock **cấm xóa/sửa** trong thời hạn retention. |

## Bẫy đề thi
- Đề cho `11 nines` — đáp án đang nói về **durability**, không phải availability.
- Thấy chữ `compliance`, `WORM`, `cannot be deleted even by root` → chọn ngay **S3 Object Lock – Compliance mode**.
- Câu hỏi về replication mà đáp án không nhắc Versioning là thiếu điều kiện bắt buộc. **CRR/SRR đều bắt buộc bật Versioning ở cả 2 phía.**
- Dữ liệu ít truy cập nhưng "must be retrieved immediately / milliseconds" → không chọn Glacier Flexible, phải chọn **Glacier Instant Retrieval** hoặc Standard-IA tùy ngữ cảnh.
- Cho người dùng bên ngoài tải file private trong thời gian ngắn → **Presigned URL**, không phải mở bucket public, không phải tạo IAM user cho khách.
- Tiết kiệm chi phí tự động theo tuổi của object → **Lifecycle rules**. Tiết kiệm khi không đoán được pattern truy cập → **Intelligent-Tiering**.
- Bucket policy là resource-based, còn IAM policy là user-based. Đề hay hỏi điểm khác biệt này.

## Tóm tắt 5 dòng
S3 là object storage với bucket / object / key, durability 11 số 9.
Chọn storage class theo tần suất truy cập: Standard → IA → Glacier → Deep Archive càng lạnh càng rẻ.
Lifecycle rules tự chuyển class và tự xóa object để tối ưu chi phí.
Versioning + MFA Delete chống xóa nhầm, Object Lock Compliance đáp ứng yêu cầu WORM/compliance.
Replication (CRR/SRR) bắt buộc Versioning, Presigned URL chia sẻ file private có thời hạn.

## Quiz — 5 câu hỏi tiếng Anh kiểu đề thi (A/B/C/D)

**Question 1.** A company must store audit logs for 7 years. The logs must not be deleted or modified by anyone, including the root user, during the retention period. Which S3 feature should be used?
A. S3 Versioning
B. S3 Object Lock in Compliance mode
C. S3 Lifecycle rules
D. MFA Delete

**Question 2.** A company wants to replicate objects from a bucket in `ap-southeast-1` to a bucket in `eu-west-1` for disaster recovery. What is a prerequisite for S3 replication?
A. Enable S3 Transfer Acceleration on both buckets
B. Enable Versioning on both the source and destination buckets
C. Make both buckets public
D. Enable static website hosting

**Question 3.** Users in another continent complain that uploading large files to an S3 bucket is slow, and the company also needs to give an external customer temporary download access to a private invoice file for 15 minutes. Which combination is correct?
A. Block Public Access and ACL
B. S3 Transfer Acceleration for uploads and a Presigned URL for the download
C. Glacier Deep Archive and bucket policy set to public
D. MFA Delete and SSE-C

**Question 4.** An application stores images that are accessed frequently in the first 30 days, rarely after that, and must be kept for 1 year before deletion. The solution must be automatic and cost-effective. What should be used?
A. S3 Intelligent-Tiering with MFA Delete
B. S3 Lifecycle rules to transition objects to cheaper storage classes and expire them after 1 year
C. CRR to another Region
D. S3 Object Lock in Governance mode

**Question 5.** A security audit requires that encryption keys for data in S3 are centrally controlled and every use of the keys is logged. Which encryption option meets this requirement?
A. SSE-S3
B. SSE-C
C. SSE-KMS
D. Client-side encryption with keys stored in the application code

## Đáp án quiz

**Câu 1 — Đáp án B.** Object Lock ở Compliance mode là cơ chế WORM duy nhất trong các lựa chọn khiến không ai, kể cả root, xóa/sửa được object trước khi hết retention period. Versioning chỉ giữ bản cũ, MFA Delete chỉ thêm bước xác thực, Lifecycle chỉ chuyển class/xóa theo lịch — không khóa dữ liệu vì compliance.

**Câu 2 — Đáp án B.** Replication khác Region là CRR, và điều kiện bắt buộc cho cả CRR lẫn SRR là phải bật Versioning ở cả bucket nguồn và bucket đích. Transfer Acceleration, public bucket hay website hosting đều không liên quan.

**Câu 3 — Đáp án B.** Transfer Acceleration giúp upload nhanh hơn từ xa nhờ edge locations. Presigned URL là cách chuẩn để cấp quyền tải 1 object private cho người ngoài trong thời gian giới hạn (15 phút) mà không cần mở bucket ra public.

**Câu 4 — Đáp án B.** Pattern truy cập đã biết rõ theo thời gian (nóng 30 ngày đầu, lạnh dần, xóa sau 1 năm) là bài toán kinh điển của Lifecycle rules: tự transition sang Standard-IA / Glacier và đặt expiration sau 1 năm — vừa tự động vừa rẻ nhất.

**Câu 5 — Đáp án C.** SSE-KMS dùng key trong AWS KMS nên bạn kiểm soát được quyền dùng key và mọi lần dùng key đều được ghi log (qua CloudTrail). SSE-S3 thì AWS quản lý hết, SSE-C là bạn tự mang key theo request chứ không quản lý tập trung trong KMS.
