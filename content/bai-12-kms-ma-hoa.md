# Bài 12 — KMS & Mã Hóa: Bảo Vệ Dữ Liệu

## Mục tiêu bài học

- Phân biệt mã hóa at rest và in transit, mã hóa phía client và phía server.
- Hiểu Envelope Encryption — cơ chế cốt lõi đằng sau AWS KMS.
- Phân biệt các loại KMS key và vai trò của Key Policy.
- Phân biệt KMS vs CloudHSM, Secrets Manager vs Parameter Store.

Bài này thuộc domain **Secure — chiếm 30% đề SAA-C03**, là domain nặng nhất. Học chắc bài này là đầu tư có lãi nhất.

## Lý thuyết chính (tiếng Việt, giữ thuật ngữ English)

### 1. Hai trạng thái dữ liệu cần mã hóa

- **Encryption at rest:** mã hóa dữ liệu khi nó đang **nằm yên** trong nơi lưu trữ: S3, EBS volume, RDS database, file trên ổ đĩa. Nếu kẻ xấu lấy được ổ đĩa vật lý hay snapshot, họ chỉ thấy dữ liệu đã mã hóa.
- **Encryption in transit:** mã hóa dữ liệu khi nó đang **di chuyển** trên đường truyền: từ user tới ALB, giữa các dịch vụ. Công nghệ quen thuộc là TLS/HTTPS.

Hệ thống đạt chuẩn thường phải có **cả hai**. Đề hay hỏi tách riêng: "dữ liệu trên đường truyền" -> TLS; "dữ liệu lưu trong database" -> at rest.

### 2. Mã hóa phía Server vs phía Client

- **Server-side encryption:** dữ liệu được bên nhận (AWS service) mã hóa sau khi nhận. Ví dụ S3 tự mã hóa object khi lưu xuống đĩa. Bạn đã gặp ở các bài S3 (SSE-S3, SSE-KMS...), EBS và RDS — tất cả đều là server-side.
- **Client-side encryption:** dữ liệu được mã hóa **ngay tại phía bạn, trước khi gửi lên AWS**. AWS chỉ nhận và lưu bản đã mã hóa, không bao giờ thấy bản gốc.

### 3. AWS KMS là gì?

**AWS Key Management Service (KMS)** là dịch vụ quản lý khóa mã hóa (encryption key) của AWS. Các dịch vụ như S3, EBS, RDS đều tích hợp với KMS để lấy khóa mã hóa dữ liệu. Bạn gần như không bao giờ mã hóa dữ liệu lớn trực tiếp bằng KMS key — KMS quản lý **khóa**, còn cơ chế thực tế là Envelope Encryption ở mục dưới.

### 4. Envelope Encryption — Khái niệm quan trọng nhất bài

**Envelope Encryption (mã hóa phong bì)** hoạt động theo hai lớp:

1. KMS sinh ra một **Data Key** để mã hóa chính dữ liệu của bạn. Bản gốc của Data Key (plaintext) dùng xong sẽ bị hủy khỏi bộ nhớ sau khi mã hóa xong.
2. Bản sao của Data Key sẽ được **mã hóa bởi KMS key** (khóa chủ), tạo thành **Encrypted Data Key**, và được lưu **cùng với** dữ liệu đã mã hóa.

Khi cần giải mã: đưa Encrypted Data Key cho KMS, KMS dùng khóa chủ giải mã nó để lấy lại Data Key, rồi dùng Data Key đó giải mã dữ liệu.

Lợi ích: muốn đổi khóa chủ (rotation) thì chỉ cần mã hóa lại các Data Key, không phải mã hóa lại toàn bộ dữ liệu khổng lồ. Và KMS key thật **không bao giờ rời khỏi KMS** — mọi thao tác với khóa chủ đều thực hiện bên trong KMS, có ghi log qua CloudTrail.

### 5. Các loại KMS Key

- **AWS owned keys:** khóa do AWS sở hữu và quản lý hoàn toàn cho nhiều dịch vụ. Bạn không nhìn thấy, không quản lý được — chỉ biết là có dùng ở một số dịch vụ.
- **AWS managed keys:** khóa KMS do AWS tạo và quản lý **trong tài khoản của bạn** cho từng dịch vụ, dạng tên `aws/s3`, `aws/ebs`... Bạn xem được nhưng không tự xóa, không tự đặt policy chi tiết hay rotation theo ý mình được.
- **Customer managed keys:** khóa **bạn tự tạo** trong KMS. Bạn toàn quyền: tạo, **xóa** (lên lịch xóa), bật/tắt, đặt Key Policy, và bật **automatic rotation**. Đây là loại đề thi hỏi nhiều nhất vì nó gắn với yêu cầu kiểm soát chặt.

### 6. Key Policy

**Key Policy** là tài liệu chính sách gắn trực tiếp trên một KMS key, là **nơi kiểm soát chính** quyền sử dụng key đó: ai được dùng key để mã hóa/giải mã, ai được quản trị key.

Điểm cần nhớ: một KMS key luôn phải có Key Policy. IAM policy của user chỉ phát huy tác dụng khi Key Policy cho phép tài khoản ủy quyền qua IAM. Khi đề hỏi "ai kiểm soát quyền dùng key" hoặc "user có IAM policy đầy đủ vẫn không dùng được key" — hãy nghĩ tới Key Policy.

Ngoài ra còn có **Grants** — cơ chế cấp quyền tạm thời, chi tiết hơn cho các dịch vụ AWS dùng key thay mặt bạn — chỉ cần biết tên ở mức SAA.

### 7. Automatic Key Rotation

Với **Customer managed key**, KMS hỗ trợ **Automatic Rotation**: định kỳ tự tạo vật liệu khóa mới cho key, ở mức khái niệm là **chu kỳ 1 năm** khi tính năng này được bật. KMS key ID giữ nguyên, vật liệu khóa cũ vẫn được giữ lại để giải mã dữ liệu cũ. Rotation tốt cho bảo mật và compliance, và nhờ Envelope Encryption nên bạn không phải mã hóa lại toàn bộ dữ liệu khi key được rotate.

### 8. KMS vs CloudHSM

**AWS CloudHSM** cung cấp cụm **HSM (Hardware Security Module) chuyên dụng — dedicated** cho riêng bạn. Bạn tự quản lý khóa hoàn toàn bên trong phần cứng đó, AWS không truy cập được khóa của bạn.

Chọn CloudHSM khi có **yêu cầu compliance đặc biệt** bắt buộc phải dùng HSM riêng do mình kiểm soát, hoặc các chuẩn mã hóa chuyên biệt. Đổi lại, CloudHSM phức tạp và tốn công vận hành hơn nhiều. Mặc định, 99% tình huống trong đề: chọn **KMS**. Chỉ chọn CloudHSM khi đề nhấn mạnh "dedicated HSM", "single-tenant hardware", "customer fully controls the keys / AWS must not have access".

### 9. Secrets Manager vs Parameter Store

Cả hai đều lưu cấu hình và bí mật, nhưng khác nhau ở trọng tâm:

- **AWS Secrets Manager:** chuyên cho **credentials / secrets** thật sự: mật khẩu database, API key. Tính năng nhận diện: **xoay vòng secret tự động (automatic rotation)**, tích hợp sẵn vòng xoay cho RDS và một số dịch vụ. Có phí theo số secret.
- **AWS Systems Manager Parameter Store:** lưu tham số cấu hình nói chung (cả giá trị thường lẫn SecureString được mã hóa bằng KMS). Phù hợp cho config, và cũng lưu được secret đơn giản, nhưng **không có cơ chế xoay vòng tự động tích hợp sẵn** như Secrets Manager.

Nhận diện nhanh: đề nhắc "tự động rotate mật khẩu database" -> **Secrets Manager**, không tranh cãi.

## Ví dụ đời thường

Envelope Encryption giống cách gửi một món đồ quý qua đường bưu điện bằng két sắt hai lớp:

- Bạn khóa món đồ bằng một **chìa khóa nhỏ dùng một lần** (Data Key) — khóa này mở nhanh, tiện cho món đồ to.
- Rồi bạn bỏ chính cái chìa nhỏ đó vào một **két sắt lớn** khóa bằng chìa chủ (KMS key) mà chỉ kho bảo mật KMS mới mở được.
- Gói hàng gửi đi gồm: món đồ đã khóa + két sắt chứa chìa nhỏ đã bị khóa.
- Người nhận muốn mở đồ thì phải nhờ KMS mở két lấy chìa nhỏ ra trước, rồi mới dùng chìa nhỏ mở món đồ.

Nhờ vậy, chìa chủ không bao giờ phải mang đi khắp nơi, và đổi chìa chủ thì chỉ cần thay cái két — không phải mở hết đồ ra khóa lại.

Còn hình dung đời thường cho các dịch vụ:

- **KMS** giống két sắt của ngân hàng: bạn gửi chìa chủ ở đó, ngân hàng ghi sổ mỗi lần ai tới mở két (CloudTrail log).
- **CloudHSM** giống bạn thuê nguyên một hầm két riêng trong ngân hàng, chỉ bạn có chìa hầm, nhân viên ngân hàng cũng không vào được — an toàn tối đa nhưng đắt và tự quản mệt.
- **Secrets Manager** giống trợ lý đổi mật khẩu nhà giúp bạn mỗi tháng một lần đều đặn mà bạn không cần nhớ (automatic rotation).
- **Parameter Store** giống cuốn sổ tay ghi mọi thông số trong nhà — có ngăn khóa cho vài thứ nhạy cảm, nhưng không ai tự đi đổi khóa giúp bạn.

## Phân biệt dễ nhầm

### AWS Managed Key vs Customer Managed Key

| Tiêu chí | AWS managed key | Customer managed key |
|---|---|---|
| Ai tạo | AWS tạo trong tài khoản của bạn | Bạn tự tạo |
| Tên dạng | `aws/s3`, `aws/ebs` | Tên do bạn đặt |
| Tự xóa được | Không | Có (lên lịch xóa) |
| Tự bật rotation | Không kiểm soát được | Có, automatic rotation |
| Đặt Key Policy riêng | Hạn chế | Toàn quyền |

### KMS vs CloudHSM

- KMS: managed, đa khách hàng (multi-tenant) ở tầng dịch vụ, AWS vận hành, tích hợp sẵn với hầu hết dịch vụ AWS.
- CloudHSM: HSM dedicated riêng cho bạn, bạn tự quản khóa hoàn toàn, dùng khi compliance đặc biệt yêu cầu.

### Secrets Manager vs Parameter Store

- Cần **rotation tự động** cho DB credentials -> Secrets Manager.
- Chỉ cần lưu config / tham số, có thể mã hóa bằng KMS -> Parameter Store là đủ.

### At Rest vs In Transit

- Dữ liệu nằm trong S3/EBS/RDS -> at rest.
- Dữ liệu đi qua HTTPS/TLS -> in transit.
Hai lớp độc lập nhau: bật được lớp này không có nghĩa là lớp kia tự có.

## Bẫy đề thi

1. **"Rotate mật khẩu database tự động"** — Chọn Secrets Manager. Parameter Store không có rotation tích hợp sẵn, đây là bẫy so sánh kinh điển.
2. **KMS key không mã hóa trực tiếp dữ liệu lớn** — Cơ chế đúng là Envelope Encryption với Data Key. Phương án nào nói "dùng KMS key mã hóa trực tiếp file vài GB" là phương án sai về kiến trúc.
3. **Không dùng được key dù IAM đã cấp đủ quyền** — Thủ phạm thường là **Key Policy** chưa cho phép. Key Policy là nơi kiểm soát chính của KMS key.
4. **CloudHSM chỉ khi có từ khóa compliance đặc biệt / dedicated** — Đề bình thường mà chọn CloudHSM thay KMS thường là chọn quá tay: đắt và phức tạp không cần thiết.
5. **Xóa Customer Managed Key là hành động nguy hiểm** — Key bị xóa thì mọi dữ liệu mã hóa bằng key đó (qua data key của nó) sẽ không giải mã được nữa. Vì vậy KMS bắt buộc phải lên lịch xóa và có thời gian chờ, không xóa tức thì.
6. **Nhầm loại key khi cần kiểm soát chặt** — Yêu cầu "tự quản lý khóa, tự bật rotation, tự audit" phải là Customer Managed Key, không phải AWS managed key.

## Tóm tắt 5 dòng

Mã hóa at rest bảo vệ dữ liệu đang lưu (S3/EBS/RDS), in transit bảo vệ dữ liệu đang truyền (TLS); client-side mã hóa trước khi gửi, server-side mã hóa tại phía AWS.
KMS dùng Envelope Encryption: Data Key mã hóa dữ liệu, Data Key lại được mã hóa bởi KMS key và lưu kèm dữ liệu.
Customer Managed Key cho bạn toàn quyền tạo/xóa/đặt Key Policy và bật Automatic Rotation với chu kỳ ở mức khái niệm là 1 năm; Key Policy là nơi kiểm soát chính quyền dùng key.
CloudHSM là HSM dedicated riêng cho bạn, chỉ chọn khi có yêu cầu compliance đặc biệt; mặc định hãy chọn KMS.
Secrets Manager chuyên lưu credentials và xoay vòng tự động, Parameter Store lưu tham số cấu hình nói chung và không có rotation tích hợp sẵn.

## Quiz — 5 câu hỏi tiếng Anh kiểu đề thi (A/B/C/D)

**Question 1:** How does AWS KMS encrypt a large file stored in Amazon S3 using envelope encryption?

A. The KMS key directly encrypts the entire file
B. A data key encrypts the file, and the data key itself is encrypted by the KMS key
C. The file is split and each part is encrypted by a different AWS owned key
D. S3 generates a public key and shares the private key with KMS

**Question 2:** A company must automatically rotate its RDS database credentials on a regular schedule without custom code. Which service should be used?

A. AWS Systems Manager Parameter Store
B. AWS Secrets Manager
C. AWS KMS
D. AWS CloudHSM

**Question 3:** A developer has an IAM policy that allows full KMS access, but calls to use a specific KMS key are still denied. What is the MOST likely cause?

A. The key is an AWS managed key in another Region
B. The Key Policy of that key does not allow the developer to use it
C. Automatic rotation is enabled on the key
D. The key was created with envelope encryption

**Question 4:** A regulated company is required to use dedicated, single-tenant hardware security modules under its full control, and AWS personnel must not be able to access the keys. Which service meets this requirement?

A. AWS KMS with customer managed keys
B. AWS KMS with AWS managed keys
C. AWS CloudHSM
D. Amazon S3 server-side encryption with SSE-S3

**Question 5:** Which statement about customer managed KMS keys is correct?

A. They cannot be deleted by the customer
B. They do not support a key policy
C. They support automatic key rotation and customer-controlled key policies
D. They are the same as AWS owned keys

## Đáp án quiz

**Câu 1 — Đáp án B.**
Giải thích tiếng Việt: Đây là định nghĩa của **Envelope Encryption**: Data Key mã hóa dữ liệu thật, còn Data Key được mã hóa bởi KMS key và lưu kèm dữ liệu. KMS key không bao giờ mã hóa trực tiếp dữ liệu lớn và không rời khỏi KMS.

**Câu 2 — Đáp án B.**
Giải thích tiếng Việt: **Secrets Manager** có tính năng xoay vòng tự động tích hợp sẵn cho credentials của RDS — đúng yêu cầu "automatic rotation không cần code riêng". Parameter Store lưu được secret nhưng không có cơ chế rotation tích hợp như vậy.

**Câu 3 — Đáp án B.**
Giải thích tiếng Việt: **Key Policy** là nơi kiểm soát chính quyền sử dụng một KMS key. IAM policy cấp quyền là chưa đủ nếu Key Policy trên key không cho phép user đó — đây là bẫy phân quyền kinh điển của KMS.

**Câu 4 — Đáp án C.**
Giải thích tiếng Việt: Từ khóa "dedicated, single-tenant HSM, AWS không được truy cập khóa, yêu cầu compliance đặc biệt" trỏ thẳng tới **CloudHSM**. KMS ở mọi loại key đều là dịch vụ do AWS vận hành, không đáp ứng yêu cầu phần cứng riêng này.

**Câu 5 — Đáp án C.**
Giải thích tiếng Việt: Customer Managed Key là loại key bạn toàn quyền: tự tạo, lên lịch xóa được, đặt **Key Policy** riêng và bật **Automatic Rotation**. Các phương án còn lại mô tả sai — hoặc lẫn sang AWS owned / AWS managed key.
