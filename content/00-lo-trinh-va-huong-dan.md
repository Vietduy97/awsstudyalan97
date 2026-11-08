# Học AWS SAA-C03 — Thư viện tài liệu tiếng Việt

> Bộ tài liệu tự học hoàn chỉnh cho người **chưa biết gì về AWS**, mục tiêu cuối là thi đỗ **AWS Certified Solutions Architect – Associate (SAA-C03)**.
> Ngôn ngữ: tiếng Việt (thuật ngữ chuyên môn và keyword đề thi giữ nguyên tiếng Anh, vì đề thi **không có bản tiếng Việt**).

## Thông tin kỳ thi SAA-C03 (nắm trước khi học)

| Hạng mục | Chi tiết |
|---|---|
| Số câu | 65 câu (50 câu tính điểm + 15 câu không tính điểm, không phân biệt được) |
| Thời gian | 130 phút (≈ 2 phút/câu) |
| Điểm đạt | 720 / 1000 (điểm thang quy đổi) |
| Lệ phí | $150 USD |
| Hiệu lực chứng chỉ | 3 năm |
| Ngôn ngữ đề | Tiếng Anh (không có tiếng Việt) |
| Domain 1 — Design Secure Architectures | **30%** |
| Domain 2 — Design Resilient Architectures | **26%** |
| Domain 3 — Design High-Performing Architectures | **24%** |
| Domain 4 — Design Cost-Optimized Architectures | **20%** |

## Cách dùng thư viện này

Học theo đúng thứ tự 3 giai đoạn. Mỗi bài học có cùng cấu trúc: **Mục tiêu → Lý thuyết → Ví dụ đời thường → Phân biệt dễ nhầm → Bẫy đề thi → Tóm tắt 5 dòng → Quiz 5 câu** (đáp án ở cuối mỗi file — tự làm trước, đối chiếu sau).

### Giai đoạn 1 — Beginner: từ số 0 (Bài 00–12, khoảng 45–60 giờ)

- [ ] `bai-00-cloud-la-gi.md` — Cloud là gì, hạ tầng toàn cầu AWS, Shared Responsibility
- [ ] `bai-01-iam-va-bao-mat-tai-khoan.md` — IAM và bảo mật tài khoản
- [ ] `bai-02-billing-va-free-tier-an-toan.md` — Billing, Free Tier an toàn (đọc TRƯỚC khi tạo tài khoản!)
- [ ] `bai-03-ec2-may-ao.md` — EC2: máy ảo trên mây
- [ ] `bai-04-lambda-serverless.md` — Lambda và tư duy serverless
- [ ] `bai-05-s3-luu-tru-doi-tuong.md` — S3: lưu trữ đối tượng
- [ ] `bai-06-ebs-efs.md` — EBS, EFS và Instance Store
- [ ] `bai-07-rds-quan-he.md` — RDS: cơ sở dữ liệu quan hệ
- [ ] `bai-08-dynamodb-va-aurora.md` — DynamoDB và Aurora
- [ ] `bai-09-vpc-mang-rieng.md` — VPC: mạng riêng ảo
- [ ] `bai-10-route53-cloudfront.md` — Route 53 (DNS) và CloudFront (CDN)
- [ ] `bai-11-giam-sat-cloudwatch-cloudtrail.md` — CloudWatch, CloudTrail, AWS Config
- [ ] `bai-12-kms-ma-hoa.md` — KMS và mã hóa dữ liệu

Song song giai đoạn 1: học khóa **AWS Cloud Practitioner Essentials** (miễn phí trên Skill Builder) và làm lab **First Cloud Journey** (tiếng Việt) — link trong `kho-tai-lieu-tham-khao.md`.

### Giai đoạn 2 — SAA nâng cao (Bài 13–20)

- [ ] `bai-13-elb-asg-ha.md` — ELB, Auto Scaling và High Availability
- [ ] `bai-14-sqs-sns-eventbridge.md` — SQS, SNS, EventBridge: tách rời hệ thống (decoupling)
- [ ] `bai-15-api-gateway.md` — API Gateway
- [ ] `bai-16-cloudformation.md` — CloudFormation: Infrastructure as Code
- [ ] `bai-17-ecs-eks-container.md` — Container: ECS, EKS, Fargate
- [ ] `bai-18-disaster-recovery.md` — Disaster Recovery: RPO, RTO và 4 chiến lược
- [ ] `bai-19-toi-uu-chi-phi.md` — Tối ưu chi phí (Cost Optimization)
- [ ] `bai-20-kien-truc-tong-hop-saa.md` — Kiến trúc tổng hợp + chiến thuật làm bài thi

### Giai đoạn 3 — Ôn nước rút + luyện đề

Tài liệu ôn nhanh (đọc đi đọc lại nhiều lần):

- [ ] `cheatsheet-tong-hop-saa.md` — Bảng keyword → dịch vụ, số liệu hay hỏi, cây quyết định
- [ ] `cheatsheet-theo-dich-vu.md` — Cheat sheet từng dịch vụ cốt lõi
- [ ] `phan-biet-cac-dich-vu.md` — Bảng so sánh các dịch vụ hay bị nhầm lẫn + quy tắc chọn

Đề mô phỏng (câu hỏi tự biên soạn theo format đề thật — làm tính giờ 130 phút/bộ, chỉ mở file đáp án sau khi làm xong):

- [ ] `de-mo-phong-01.md` + `de-mo-phong-01-dap-an.md` — 65 câu (trọng tâm: bảo mật, S3, VPC, HA)
- [ ] `de-mo-phong-02.md` + `de-mo-phong-02-dap-an.md` — 65 câu (trọng tâm: DynamoDB, Lambda, decoupling, cache)
- [ ] `de-mo-phong-03.md` + `de-mo-phong-03-dap-an.md` — 65 câu (trọng tâm: kiến trúc tổng hợp, migration, chi phí)

Khi đạt ổn định **80%+ ở các bộ đề tính giờ**, hãy làm thêm đề chính thức (Official Practice Exam) rồi đặt lịch thi thật. Các nguồn luyện đề uy tín và khóa học bổ sung: xem `kho-tai-lieu-tham-khao.md`.

## Lộ trình theo tuần (tham khảo, 1–2 giờ/ngày)

| Tuần | Nội dung |
|---|---|
| 1 | Bài 00–02 + tạo tài khoản an toàn + làm thử 20 câu Official Practice Question Set (miễn phí) để chẩn đoán |
| 2 | Bài 03–04 (Compute) + lab EC2/Lambda |
| 3 | Bài 05–06 (Storage) + lab S3 |
| 4 | Bài 07–08 (Database) |
| 5 | Bài 09–10 (Networking) + lab dựng VPC |
| 6 | Bài 11–12 (Giám sát & mã hóa) + đọc lại cheat sheet lần 1 |
| 7 | Bài 13–15 (HA, decoupling, API) |
| 8 | Bài 16–18 (IaC, container, DR) |
| 9 | Bài 19–20 (chi phí, tổng hợp) + bắt đầu đề mô phỏng 01 |
| 10 | Đề mô phỏng 02–03 tính giờ, sửa lỗi theo domain, ôn cheat sheet |

## Quy tắc an toàn tiền bạc (thuộc lòng)

1. Đọc Bài 02 và đặt **AWS Budget + cảnh báo chi phí TRƯỚC** khi tạo bất kỳ tài nguyên nào.
2. Tài khoản mới (từ 15/07/2025): $100 credit ngay + tối đa $100 nữa trong 6 tháng — gói cũ "12 tháng miễn phí" không còn áp dụng.
3. Học xong lab nào, **terminate tài nguyên lab đó trong ngày** (stop EC2 vẫn tốn tiền ổ EBS).
4. Tuyệt đối không đăng access key lên mạng/GitHub.

---

*Thư viện được biên soạn ngày 08/11/2026. Đánh dấu [x] vào từng mục khi hoàn thành để theo dõi tiến độ.*
*Trạng thái biên soạn: ĐÃ HOÀN THÀNH và tải lên Drive ngày 08/11/2026 — đủ 21 bài học, 2 cheat sheet, 1 file phân biệt dịch vụ, 3 bộ đề mô phỏng (mỗi bộ 65 câu + file đáp án riêng) và kho tài liệu tham khảo. Các ô [ ] phía trên là tiến độ HỌC của bạn, không phải tiến độ biên soạn.*
