# Bài 01 — IAM và Bảo mật tài khoản

## Mục tiêu bài học
- Hiểu IAM là gì và vì sao domain Security chiếm 30% đề thi SAA-C03
- Phân biệt rõ IAM User, Group, Role, Policy
- Đọc được JSON Policy ở mức cơ bản: Effect, Action, Resource
- Nắm nguyên tắc Least Privilege và cách áp dụng
- Biết cách bảo vệ Root Account: bật MFA, không dùng hằng ngày
- Hiểu IAM Role dùng Temporary Credentials qua STS, khác gì với Access Key cố định
- Biết Federation / SSO với IAM Identity Center và AWS Organizations + SCP ở mức khái niệm
- Nắm Password Policy và Access Key hygiene — không bao giờ lộ key

## Lý thuyết chính

### 1. IAM là gì?

**AWS Identity and Access Management (IAM)** là dịch vụ quản lý danh tính và quyền truy cập vào AWS. IAM là **global service** — không thuộc Region nào, miễn phí, và là thứ bạn phải cấu hình ngay khi tạo tài khoản.

Câu hỏi cốt lõi IAM trả lời: **Ai (Identity) được làm gì (Permission) trên tài nguyên nào (Resource)?**

Domain **Secure Applications and Architectures chiếm 30%** đề SAA-C03 — cao nhất trong 4 domain. IAM xuất hiện trong gần như mọi scenario.

### 2. Bốn khái niệm trung tâm

**IAM User:** Một danh tính cụ thể cho một người hoặc một ứng dụng. Mỗi User có username/password để vào Console, và/hoặc Access Key để gọi API/CLI. Một người thật = một User riêng, tuyệt đối không dùng chung User.

**IAM Group:** Một nhóm các User có cùng quyền. Ví dụ: nhóm `Developers`, nhóm `Admins`, nhóm `Auditors`. Gắn Policy vào Group thì mọi User trong Group đều có quyền đó. Group giúp quản lý hàng loạt, tránh gắn quyền từng người một. Lưu ý hay thi: **Group không phải là identity** — không đăng nhập bằng Group được, Group cũng không thể nằm trong Group khác (no nested groups).

**IAM Role:** Khái niệm quan trọng nhất cho đề thi. Role giống User ở chỗ có Policy gắn kèm, nhưng Role **không có password hay Access Key cố định**. Role được "đeo vào" (assume) tạm thời bởi: một User, một ứng dụng chạy trên EC2, một dịch vụ AWS (Lambda, EC2), hoặc người dùng từ hệ thống bên ngoài. Khi Assume Role, bạn nhận được **Temporary Credentials** qua **AWS Security Token Service (STS)** — bộ key này tự hết hạn sau một thời gian ngắn.

**IAM Policy:** Một tài liệu JSON định nghĩa quyền. Policy mới là thứ thực sự nói "được phép" hay "bị cấm". User/Group/Role tự chúng không có quyền gì cho đến khi được gắn Policy.

### 3. JSON Policy ở mức cơ bản

Một Policy gồm các **Statement**, mỗi Statement có:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::my-bucket/*"
    }
  ]
}
```

- **Effect:** `Allow` (cho phép) hoặc `Deny` (cấm). **Explicit Deny luôn thắng Allow** — đây là bẫy kinh điển.
- **Action:** Hành động, ví dụ `s3:GetObject`, `ec2:StartInstances`, `s3:*` (mọi hành động của S3).
- **Resource:** Tài nguyên áp dụng, viết dạng ARN — ví dụ một S3 bucket cụ thể. Dấu `*` nghĩa là mọi tài nguyên.
- **Condition (tùy chọn):** Điều kiện thêm, ví dụ chỉ cho phép từ một IP nhất định, hoặc bắt buộc có MFA.
- **Principal:** Ai được áp dụng — hay gặp trong Resource-based Policy như S3 Bucket Policy.

Có hai loại Policy hay gặp:
- **Identity-based Policy:** Gắn vào User/Group/Role.
- **Resource-based Policy:** Gắn trực tiếp vào tài nguyên, ví dụ S3 Bucket Policy, và có trường `Principal`.

Ngoài ra còn có **Managed Policy** (AWS tạo sẵn như `AmazonS3ReadOnlyAccess`, hoặc bạn tự tạo và tái sử dụng) và **Inline Policy** (nhúng thẳng vào đúng một User/Group/Role, không tái sử dụng được).

### 4. Nguyên tắc Least Privilege

**Principle of Least Privilege:** Chỉ cấp đúng quyền tối thiểu cần thiết để làm việc, không hơn.

Ví dụ: nhân viên chỉ cần xem file trong S3 thì chỉ cấp `s3:GetObject` trên đúng bucket đó, không cấp `s3:*` hay tệ hơn là `AdministratorAccess`.

Đề thi rất thích tình huống: "Làm sao giảm rủi ro mà vẫn cho developer làm việc?" — đáp án thường là áp dụng Least Privilege, dùng IAM Role, bật MFA, dùng Policy có `Resource` giới hạn cụ thể thay vì `*`.

Công cụ hỗ trợ: **IAM Access Analyzer** (tìm quyền thừa, tài nguyên bị share ra ngoài), **IAM Policy Simulator** (test policy trước khi áp dụng), **Access Advisor** (xem dịch vụ nào User thực sự đã dùng để thu hẹp quyền).

### 5. Bảo vệ Root Account — việc số 1 ngày đầu tiên

**Root Account** là tài khoản chủ tạo ra khi đăng ký AWS, có quyền không giới hạn, kể cả đóng tài khoản, đổi thông tin thanh toán. Root **không thể bị giới hạn bởi IAM Policy**.

Checklist bảo vệ Root:
- **Bật MFA (Multi-Factor Authentication) cho Root ngay lập tức** — ưu tiên hardware key hoặc authenticator app.
- **Không dùng Root cho công việc hằng ngày.** Tạo IAM User / dùng IAM Identity Center cho việc thường ngày, cất Root đi.
- **Không tạo Access Key cho Root.** Nếu đã tạo thì xóa ngay.
- Đặt password Root mạnh, duy nhất, lưu trong password manager.
- Bật cảnh báo billing để phát hiện bất thường sớm.

MFA là lớp bảo vệ thứ hai ngoài password: cái bạn biết (password) + cái bạn có (mã từ điện thoại/hardware key).

### 6. IAM Role và Temporary Credentials qua STS

Vì sao đề thi luôn ưu tiên Role hơn Access Key cố định?

- Access Key của IAM User là **long-term credentials** — không tự hết hạn, lộ là nguy hiểm dài hạn.
- Role cho ra **temporary credentials** qua **STS (Security Token Service)**, lệnh hay gặp là `AssumeRole`. Credentials này hết hạn sau vài phút đến vài giờ, lộ cũng ít thiệt hại hơn, và tự động được xoay (rotate).

Case kinh điển nhất định phải nhớ: **EC2 cần gọi S3**. Cách đúng: tạo IAM Role có quyền S3, gắn vào EC2 qua **Instance Profile**. Tuyệt đối không hard-code Access Key vào code trên EC2. Tương tự: Lambda gọi DynamoDB cũng dùng Execution Role của Lambda.

STS còn dùng cho **Federation** và cross-account access.

### 7. Federation / SSO với IAM Identity Center

**Federation** là việc dùng danh tính từ hệ thống bên ngoài (ví dụ tài khoản công ty, Microsoft Active Directory, Google Workspace) để đăng nhập AWS mà không cần tạo IAM User riêng cho từng người.

**AWS IAM Identity Center** (tên cũ là AWS SSO) là dịch vụ Single Sign-On được AWS khuyến nghị hiện nay: người dùng đăng nhập một lần qua Identity Center, sau đó được cấp quyền tạm thời vào nhiều AWS Account. Đây là cách quản lý người dùng ở quy mô công ty — không phải tạo hàng trăm IAM User thủ công.

### 8. AWS Organizations và SCP ở mức khái niệm

Khi công ty có nhiều AWS Account, dùng **AWS Organizations** để quản lý tập trung: một **Management Account** quản lý nhiều **Member Accounts**, có thể gom vào **Organizational Units (OU)** như OU Production, OU Development.

**Service Control Policies (SCP):** Policy ở tầng Organization, đặt ra "hàng rào" quyền tối đa cho các account bên dưới. SCP **không cấp quyền**, nó chỉ **giới hạn** quyền tối đa. Ví dụ: SCP cấm dùng Region ngoài Singapore, hoặc cấm tắt CloudTrail — dù Admin trong account con có gắn AdministratorAccess cũng không vượt qua được SCP. Keyword đề thi: SCP = guardrail, không phải grant.

### 9. Password và Access Key hygiene

- Đặt **IAM Password Policy:** độ dài tối thiểu, yêu cầu ký tự đặc biệt, bắt đổi sau X ngày, không cho dùng lại mật khẩu cũ.
- **Access Key:** Mỗi User tối đa 2 Access Key để tiện rotate. Phải **rotate định kỳ**, xóa key không dùng, không bao giờ commit key lên GitHub, không để key trong code, không chia sẻ qua email/chat.
- **Tuyệt đối không lộ Access Key.** Lộ key là kẻ xấu có thể đào coin, tạo tài nguyên tốn hàng nghìn đô trong vài giờ.
- Dùng **IAM Credential Report** để kiểm kê ai có key nào, key nào lâu không dùng.
- Ưu tiên theo thứ tự: Temporary Credentials (Role/STS) > IAM Identity Center > IAM User có MFA. Tránh long-term Access Key khi có thể.

## Ví dụ đời thường

**IAM giống như hệ thống thẻ ra vào và chìa khóa trong một tòa nhà văn phòng.**

- **Root Account** là chủ tòa nhà, giữ chìa khóa tổng mở được mọi phòng kể cả phòng két tiền. Bạn không đưa chìa khóa tổng cho nhân viên đi làm hằng ngày — bạn cất nó trong két và chỉ lấy ra khi thật cần. Đó là lý do không dùng Root hằng ngày và phải bật MFA cho Root.
- **IAM User** là mỗi nhân viên có một thẻ riêng ghi tên mình. Mất thẻ của ai thì khóa thẻ người đó, không ảnh hưởng người khác. Dùng chung thẻ giống như cả công ty dùng chung một mật khẩu — có chuyện gì không biết ai làm.
- **IAM Group** là phòng ban: thẻ của phòng Kế toán mở được phòng Kế toán, thẻ của phòng Kỹ thuật mở được phòng Server. Đổi quyền cả phòng thì chỉ sửa một lần ở Group Policy.
- **IAM Policy** là tờ quy định dán trên cửa: "Thẻ này được mở phòng A, B từ 8h–17h, cấm vào phòng két."
- **IAM Role** giống như thẻ khách tạm thời ở lễ tân: khách đến họp thì nhận thẻ thăm, thẻ chỉ mở đúng phòng họp và tự hết giá trị cuối ngày. Nhân viên giao hàng (giống EC2) cũng nhận thẻ tạm như vậy, thay vì được cấp chìa khóa vĩnh viễn — đó chính là Temporary Credentials qua STS.
- **Least Privilege** là thực tế ở Việt Nam: giúp việc theo giờ chỉ có chìa khóa cổng, không có chìa khóa phòng ngủ và két sắt. Cần gì cấp nấy thôi.

## Phân biệt dễ nhầm

| Cặp dễ nhầm | Cách phân biệt |
|---|---|
| User vs Role | User có password/key cố định, là danh tính lâu dài. Role không có key cố định, được assume tạm thời, cho ra temporary credentials |
| Group vs Role | Group chứa User để gắn quyền hàng loạt. Role là danh tính tạm được người/dịch vụ đeo vào |
| Authentication vs Authorization | Authentication (AuthN) = bạn là ai (đăng nhập). Authorization (AuthZ) = bạn được làm gì (Policy) |
| IAM Policy vs SCP | IAM Policy cấp/giới hạn quyền trong account. SCP ở tầng Organizations chỉ đặt trần tối đa, không tự cấp quyền |
| MFA vs Password Policy | Password Policy quy định mật khẩu mạnh thế nào. MFA là lớp xác thực thứ hai sau mật khẩu |
| Identity-based vs Resource-based Policy | Identity-based gắn vào User/Role. Resource-based gắn vào tài nguyên (S3 bucket) và có Principal |

## Bẫy đề thi

- **Explicit Deny luôn thắng mọi Allow.** Nếu có một Statement Deny áp dụng, kết quả cuối cùng là Deny dù có bao nhiêu Allow khác.
- Đề hỏi "cách an toàn nhất cho EC2 truy cập S3": đáp án đúng là **IAM Role + Instance Profile**, sai là "tạo IAM User rồi nhúng Access Key vào code" — lựa chọn chứa Access Key hard-code gần như luôn là đáp án sai.
- Đề hỏi việc đầu tiên sau khi tạo tài khoản mới: **bật MFA cho Root, tạo user quản trị riêng, không dùng Root**.
- SCP không cấp quyền: nếu một User không có IAM Policy nào cho phép, SCP có Allow cũng không giúp User làm được việc. SCP chỉ lọc bớt quyền.
- IAM là **global service**, không chọn Region cho IAM. Câu hỏi đánh lừa về "IAM ở Region nào" — trả lời là global.
- Đề cho scenario công ty có 500 nhân viên, muốn đăng nhập AWS bằng tài khoản công ty sẵn có: đáp án là **Federation / IAM Identity Center**, không phải tạo 500 IAM User.
- Nhớ: Group không chứa được Group, Role không có password.

## Tóm tắt 5 dòng
IAM quản lý ai được làm gì trên tài nguyên nào, gồm User (danh tính lâu dài), Group (nhóm User), Role (danh tính tạm) và Policy (tài liệu JSON định nghĩa quyền).
Policy có Effect Allow/Deny, Action và Resource — Explicit Deny luôn thắng, và phải luôn áp dụng Least Privilege: chỉ cấp quyền tối thiểu.
Root Account có quyền tuyệt đối nên phải bật MFA, không tạo Access Key cho Root và không dùng Root cho việc hằng ngày.
Role cho ra Temporary Credentials qua STS và là cách đúng cho EC2/Lambda gọi dịch vụ AWS khác — không bao giờ hard-code Access Key.
IAM Identity Center lo SSO/Federation cho nhiều người, AWS Organizations + SCP đặt hàng rào quản trị cho nhiều account.

## Quiz

**Câu 1:** A company wants its Amazon EC2 instances to access Amazon S3 securely without storing long-term credentials on the instances. What is the BEST solution?

A. Create an IAM user and embed the access keys in the application code
B. Create an IAM role with S3 permissions and attach it to the EC2 instances via an instance profile
C. Store the root account credentials in a configuration file on the instances
D. Make the S3 bucket public so no credentials are needed

**Câu 2:** Which of the following actions should be taken FIRST to secure a new AWS account's root user?

A. Create access keys for the root user for programmatic access
B. Enable Multi-Factor Authentication (MFA) for the root user
C. Use the root user for daily administrative tasks
D. Share the root credentials with the development team

**Câu 3:** An IAM policy contains an Allow statement for all S3 actions, but another policy contains an explicit Deny for `s3:DeleteBucket`. What is the effective permission for deleting a bucket?

A. Allowed, because Allow takes precedence
B. Denied, because an explicit Deny overrides any Allow
C. Allowed only with MFA
D. Denied only during business hours

**Câu 4:** A company with multiple AWS accounts wants to set a maximum permissions boundary so that no account can disable AWS CloudTrail, even if an administrator in a member account tries to allow it. Which feature should they use?

A. IAM inline policies
B. Service Control Policies (SCPs) in AWS Organizations
C. S3 Bucket Policies
D. Security Groups

**Câu 5:** What is the main security benefit of using IAM Roles compared to IAM User access keys?

A. Roles provide permanent credentials that never expire
B. Roles provide temporary credentials that automatically expire
C. Roles do not require any policies
D. Roles bypass the need for MFA

## Đáp án quiz

**Câu 1 — B.** Đây là case kinh điển nhất của IAM trong đề thi. IAM Role + Instance Profile cho EC2 nhận Temporary Credentials tự động xoay, không cần lưu key. A và C là hard-code long-term credentials/root — luôn sai. D làm lộ dữ liệu, sai hoàn toàn về bảo mật.

**Câu 2 — B.** Việc đầu tiên với Root là bật MFA. Tạo Access Key cho Root (A), dùng Root hằng ngày (C) và chia sẻ Root (D) đều là những điều sách giáo khoa dặn tuyệt đối không làm.

**Câu 3 — B.** Nguyên tắc đánh giá quyền của IAM: Explicit Deny thắng tất cả. Dù có Allow `s3:*` thì một Deny rõ ràng cho `s3:DeleteBucket` vẫn khiến hành động bị cấm.

**Câu 4 — B.** SCP trong AWS Organizations là guardrail ở tầng tổ chức: nó đặt trần quyền tối đa cho member account. Lưu ý SCP không cấp quyền, nó chỉ giới hạn — và Admin trong account con cũng không vượt qua được SCP của Management Account.

**Câu 5 — B.** Điểm mạnh cốt lõi của Role là Temporary Credentials qua STS: tự hết hạn, tự xoay, giảm thiểu rủi ro khi lộ. A nói ngược sự thật, C và D đều sai — Role vẫn cần Policy và vẫn kết hợp được với MFA.
