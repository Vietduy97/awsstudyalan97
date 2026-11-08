# Cheatsheet Theo Dịch Vụ SAA-C03 — Mỗi Dịch Vụ 1 Mục

> Format mỗi mục: **Là gì / Điểm hay bị hỏi / Giới hạn kinh điển / 1 câu ghi nhớ.**

---

## IAM

- **Là gì:** Quản lý identity (user, group, role) và quyền truy cập AWS qua policy JSON.
- **Hay bị hỏi:** Role > User cho EC2/application (không hard-code access key); Policy đánh giá: Explicit Deny thắng tất cả; Least privilege; IAM Access Analyzer; MFA.
- **Giới hạn / bẫy:** IAM là **global** service (không theo Region). Root user chỉ dùng việc bất khả kháng, khóa + bật MFA ngay.
- **Ghi nhớ:** *Cấp quyền bằng Role, không nhúng key vào code.*

## Organizations

- **Là gì:** Quản lý nhiều tài khoản AWS tập trung: OU, consolidated billing.
- **Hay bị hỏi:** **SCP = preventive guardrail** ở tầng account/OU — SCP không cấp quyền, chỉ giới hạn trần quyền. Consolidated billing = volume discount.
- **Giới hạn / bẫy:** SCP không áp dụng lên Management Account theo cách chặn như account con; SCP deny thì IAM policy allow đến mấy cũng vô dụng.
- **Ghi nhớ:** *SCP chặn trần, IAM cấp sàn — muốn làm được việc phải qua cả hai.*

## EC2

- **Là gì:** Máy ảo thuê theo giờ/giây, toàn quyền OS.
- **Hay bị hỏi:** Pricing: On-Demand (linh hoạt), Reserved / Savings Plans (ổn định, rẻ hơn), Spot (rẻ nhất, bị thu hồi — cho batch/fault-tolerant), Dedicated Host (license/compliance). Placement Group: Cluster (low latency), Spread (chống lỗi phần cứng), Partition (Hadoop...). Hibernate khác Stop.
- **Giới hạn / bẫy:** Spot không dùng cho workload không chịu được gián đoạn (database, stateful quan trọng). Security Group gán theo ENI/instance.
- **Ghi nhớ:** *Ổn định → Reserved/Savings Plans. Gián đoạn được → Spot.*

## Lambda

- **Là gì:** Chạy code theo sự kiện, không server, tính tiền theo request + thời gian chạy.
- **Hay bị hỏi:** Trigger từ S3, API Gateway, SQS, EventBridge...; IAM Role cho Lambda; biến môi trường + Secrets Manager; concurrency; Lambda + VPC (truy cập RDS được nhưng mất kết nối internet mặc định nếu không có NAT).
- **Giới hạn kinh điển:** Timeout tối đa **15 phút**. Việc dài hơn → Step Functions / ECS.
- **Ghi nhớ:** *Ngắn + sự kiện + không server = Lambda.*

## S3

- **Là gì:** Object storage toàn cục theo bucket, scale gần như vô hạn.
- **Hay bị hỏi:** Storage classes + Lifecycle; Versioning; MFA Delete; Object Lock (WORM); Replication (CRR/SRR) — **phải bật Versioning**; Pre-signed URL; Encryption: SSE-S3 / SSE-KMS / SSE-C / client-side; Block Public Access; S3 Static Website.
- **Giới hạn kinh điển:** Durability **11 số 9**; object tối đa **5 TB**, single PUT **5 GB** → Multipart Upload.
- **Ghi nhớ:** *Mặc định bucket là private — public là do policy/config sai.*

## EBS

- **Là gì:** Block storage (ổ cứng ảo) gắn vào EC2, bền vững độc lập với instance.
- **Hay bị hỏi:** Volume types (xem file phân biệt); Snapshot = backup tăng dần, lưu trên S3 (ẩn); Encryption at rest; Multi-Attach chỉ cho họ io1/io2 trong điều kiện riêng.
- **Giới hạn / bẫy:** 1 EBS volume thường gắn **1 instance tại 1 AZ** (volume nằm trong 1 AZ). Muốn chia sẻ nhiều instance → EFS.
- **Ghi nhớ:** *EBS = ổ cứng của 1 EC2, trong 1 AZ.*

## EFS

- **Là gì:** NFS file system dùng chung, tự scale, multi-AZ trong 1 Region.
- **Hay bị hỏi:** Nhiều EC2 (Linux) mount cùng lúc; Storage class EFS-IA để giảm chi phí file ít dùng; Throughput modes.
- **Giới hạn / bẫy:** Chỉ Linux/NFS (Windows → FSx for Windows). Đắt hơn EBS nhưng chia sẻ được.
- **Ghi nhớ:** *Nhiều server Linux cùng đọc/ghi 1 thư mục = EFS.*

## RDS

- **Là gì:** Relational DB có quản trị: MySQL, PostgreSQL, MariaDB, Oracle, SQL Server.
- **Hay bị hỏi:** **Multi-AZ = failover/HA** (standby không đọc được); **Read Replica = scale read** (có thể cross-Region, có thể promote); Automated backup vs Manual snapshot; Encryption khi tạo DB (muốn mã hóa DB chưa mã hóa → snapshot → copy encrypted → restore).
- **Giới hạn kinh điển:** Automated backup giữ **1–35 ngày**. Muốn giữ lâu hơn → manual snapshot.
- **Ghi nhớ:** *HA hỏi Multi-AZ, read nhiều hỏi Replica.*

## Aurora

- **Là gì:** Relational DB do AWS xây dựng, tương thích MySQL/PostgreSQL, tách compute và storage.
- **Hay bị hỏi:** Storage tự scale tới **128 TB**; tối đa **15 Aurora Replicas**; failover nhanh; Aurora Serverless (workload thất thường); Global Database (cross-Region); Backtrack (khái niệm).
- **Giới hạn / bẫy:** Chỉ tương thích MySQL/PostgreSQL — cần Oracle/SQL Server thì quay về RDS.
- **Ghi nhớ:** *RDS "pro": hiệu năng + scale tốt hơn, vẫn là SQL quan hệ.*

## DynamoDB

- **Là gì:** NoSQL key-value/document serverless, scale triệu request/s, single-digit millisecond.
- **Hay bị hỏi:** Partition Key / Sort Key quyết định hiệu năng; GSI vs LSI; Provisioned vs On-Demand; Streams (trigger Lambda); Global Tables (multi-Region active-active); Point-in-Time Recovery; DAX cache.
- **Giới hạn / bẫy:** Không JOIN, không query tùy tiện như SQL — thiết kế bảng theo access pattern. Item size có giới hạn kinh điển 400 KB.
- **Ghi nhớ:** *Biết trước cách truy vấn thì DynamoDB nhanh vô địch; cần JOIN thì đừng chọn nó.*

## ElastiCache

- **Là gì:** In-memory cache managed: Redis hoặc Memcached.
- **Hay bị hỏi:** Redis: persistence, replication, failover, pub/sub, sorted set (leaderboard), session. Memcached: đơn giản, multi-thread, không persistence/replication. Pattern: Lazy Loading, Write-Through. Dùng để giảm tải RDS/DynamoDB + lưu session (stateless web tier).
- **Giới hạn / bẫy:** Cache không phải database chính — mất cache không được mất dữ liệu gốc (trừ use case session chấp nhận được).
- **Ghi nhớ:** *Đọc lặp lại nhiều + cần sub-millisecond = cache trước database.*

## VPC

- **Là gì:** Mạng riêng ảo: subnet public/private, route table, IGW, NAT, SG, NACL.
- **Hay bị hỏi:** Public subnet = có route ra IGW; Private subnet ra internet qua **NAT Gateway** (ở public subnet); Bastion/Jump host; VPC Peering (không transitive); Transit Gateway (hub-and-spoke); VPC Endpoints; VPC Flow Logs (bắt traffic metadata → CloudWatch/S3).
- **Giới hạn / bẫy:** Peering không bắc cầu: A–B, B–C không suy ra A–C. NAT Gateway là managed + theo AZ, muốn HA thì mỗi AZ 1 cái.
- **Ghi nhớ:** *Public ra thẳng IGW, private đi nhờ NAT.*

## Route 53

- **Là gì:** DNS có quản trị + đăng ký domain + health check.
- **Hay bị hỏi:** Routing policies: Simple, Weighted, Latency, Failover, Geolocation, Geoproximity, Multi-value. Alias record trỏ AWS resource (S3, CloudFront, ALB) — ưu tiên hơn CNAME ở zone apex. Health check → failover.
- **Giới hạn / bẫy:** DNS có TTL/cache — đổi record không có hiệu lực tức thì toàn cầu.
- **Ghi nhớ:** *Câu hỏi nhắc DNS / failover theo Region / chia traffic theo % → Route 53.*

## CloudFront

- **Là gì:** CDN — phân phối nội dung từ edge location, cache + tăng tốc + HTTPS.
- **Hay bị hỏi:** Origin: S3, ALB, EC2, HTTP server bất kỳ. OAC/OAI để S3 chỉ cho CloudFront đọc (bucket vẫn private). Signed URL/Cookie cho nội dung trả phí. Invalidation khi cần xóa cache gấp. Geo restriction.
- **Giới hạn / bẫy:** Cache có TTL — nội dung mới không hiện ngay nếu chưa hết TTL/invalidate.
- **Ghi nhớ:** *Người dùng toàn cầu + nội dung tĩnh/chậm thay đổi = CloudFront trước origin.*

## ELB (ALB / NLB / GWLB)

- **Là gì:** Load balancer có quản trị, phân phối traffic vào nhiều target/AZ.
- **Hay bị hỏi:** **ALB = Layer 7 HTTP/HTTPS**, routing theo path/host/header, target: EC2/container/IP/Lambda. **NLB = Layer 4 TCP/UDP**, hiệu năng cực cao, static IP/EIP. **GWLB = Layer 3**, đưa traffic qua firewall/appliance bên thứ ba. CLB là đời cũ — chỉ chọn khi đề nhắc tính năng legacy.
- **Giới hạn / bẫy:** Cần IP tĩnh cho load balancer → NLB (ALB IP thay đổi, dùng DNS name). Cần đọc path URL → bắt buộc ALB.
- **Ghi nhớ:** *Đọc được HTTP thì ALB, chỉ chuyển gói cực nhanh thì NLB, chèn firewall thì GWLB.*

## Auto Scaling (ASG)

- **Là gì:** Tự thêm/bớt EC2 (hoặc tài nguyên) theo chính sách để giữ đúng số lượng mong muốn.
- **Hay bị hỏi:** Min / Desired / Max; Scaling policies: Target Tracking (dễ nhất, hay đúng), Step, Simple, Scheduled; Launch Template; kết hợp ALB health check để thay instance hỏng; nhiều AZ.
- **Giới hạn / bẫy:** ASG bản thân không cân bằng tải — phải có ELB. Scale-out không cứu được nghẽn ở database.
- **Ghi nhớ:** *ASG giữ đàn khỏe và đúng cỡ, ELB chia việc cho đàn.*

## SQS

- **Là gì:** Hàng đợi message (queue) — decouple producer và consumer.
- **Hay bị hỏi:** Standard vs FIFO; Visibility Timeout; DLQ; Long Polling (giảm chi phí + giảm empty receive); consumer scale bằng Lambda/ASG; message retention.
- **Giới hạn kinh điển:** Retention tối đa **14 ngày**; visibility tối đa **12 giờ**; FIFO **300 TPS / 3.000 TPS khi batch**.
- **Ghi nhớ:** *Cần buffer / chống quá tải / tách rời hệ thống = SQS.*

## SNS

- **Là gì:** Pub/Sub notification: 1 message → nhiều subscriber (email, SMS, HTTP, Lambda, SQS...).
- **Hay bị hỏi:** Topic + Subscription; Fanout SNS → SQS; FIFO topic đi với FIFO queue; lọc message bằng filter policy.
- **Giới hạn / bẫy:** SNS không lưu message để consumer "rảnh thì lấy" như queue — offline là nguy cơ mất tin, nên fanout bền vững phải qua SQS.
- **Ghi nhớ:** *SNS bắn tin đi khắp nơi, SQS giữ tin chờ xử lý.*

## EventBridge

- **Là gì:** Event bus serverless: sự kiện từ AWS, SaaS và app tự định nghĩa → route tới target theo rule.
- **Hay bị hỏi:** Schedule bằng cron/rate (thay CloudWatch Events); Schema Registry; Archive & replay event; tích hợp nhiều dịch vụ hơn SNS kiểu cũ cho bài toán event-driven.
- **Giới hạn / bẫy:** Cần thứ tự nghiêm ngặt + exactly-once kiểu queue → vẫn là SQS FIFO, không phải EventBridge.
- **Ghi nhớ:** *"Khi sự kiện X xảy ra thì gọi Y, theo lịch cũng được" = EventBridge.*

## API Gateway

- **Là gì:** Cửa ngõ API: tạo, bảo mật, throttle, cache REST/HTTP/WebSocket API trước Lambda/backend.
- **Hay bị hỏi:** Integration với Lambda; API Key + Usage Plan (throttling/quota cho khách hàng); Authorizer: Cognito / Lambda authorizer / IAM; Private API + VPC endpoint + resource policy; Caching giảm tải backend.
- **Giới hạn kinh điển:** Timeout tích hợp REST API hay bị hỏi ở mức ~**29 giây** — tác vụ dài thì thiết kế async.
- **Ghi nhớ:** *Quản lý ai được gọi API, gọi bao nhiêu, gọi vào đâu = API Gateway.*

## CloudFormation

- **Là gì:** Infrastructure as Code của AWS: khai báo template (YAML/JSON) → Stack.
- **Hay bị hỏi:** Stack, Change Set (xem trước thay đổi), Drift Detection, Stack Policy, Rollback khi lỗi, Nested Stack, Export/Import cross-stack.
- **Giới hạn / bẫy:** Xóa stack = xóa tài nguyên do stack tạo (trừ khi có DeletionPolicy Retain — hay dùng cho database/S3 quan trọng).
- **Ghi nhớ:** *Dựng/hủy cả hệ thống lặp lại được, có kiểm soát = CloudFormation.*

## ECS / EKS / Fargate

- **Là gì:** Chạy container. ECS = orchestrator của AWS. EKS = Kubernetes managed. Fargate = launch type serverless cho cả ECS/EKS.
- **Hay bị hỏi:** ECS EC2 launch type (tự quản instance, rẻ/chủ động hơn khi workload ổn định, cần GPU/đặc thù) vs Fargate (không quản server, trả theo task). Task Definition, Service, Cluster. EKS khi đội chuẩn K8s / đa đám mây.
- **Giới hạn / bẫy:** Fargate không cho vào instance "chọc ngoáy" — cần kiểm soát OS/kernel → EC2 launch type hoặc EC2 thuần.
- **Ghi nhớ:** *Container không server = Fargate. Kubernetes = EKS. Còn lại mặc định nghĩ ECS.*

## KMS

- **Là gì:** Quản lý khóa mã hóa (keys) tập trung, tích hợp hầu hết dịch vụ AWS, audit qua CloudTrail.
- **Hay bị hỏi:** Customer Managed Key vs AWS Managed Key; Key Policy + IAM cùng quyết định quyền dùng khóa; Envelope Encryption; Automatic key rotation (cho customer managed key đối xứng); Grants; khóa cross-account.
- **Giới hạn / bẫy:** KMS mã hóa **dữ liệu nhỏ / khóa dữ liệu** theo mô hình envelope — không dùng KMS để tự mã hóa trực tiếp file nhiều GB từng cái một trong đáp án thi.
- **Ghi nhớ:** *"Ai được dùng khóa nào, dùng khi nào, có audit" = KMS.*

## CloudWatch

- **Là gì:** Giám sát metrics, logs, alarms, dashboards, events (nay nhiều phần qua EventBridge).
- **Hay bị hỏi:** Metric → Alarm → Action (SNS, ASG, EC2 action); Logs + Log Groups + Metric Filter; Container/ Lambda insights (khái niệm); Alarm thiếu dữ liệu xử lý thế nào.
- **Giới hạn / bẫy:** CloudWatch **không** trả lời "ai đã gọi API xóa bucket" — đó là CloudTrail.
- **Ghi nhớ:** *Hệ thống khỏe không, chậm không, tốn tài nguyên không = CloudWatch.*

## CloudTrail

- **Là gì:** Ghi lại mọi API call trong tài khoản: ai, làm gì, khi nào, từ IP nào.
- **Hay bị hỏi:** Management Events vs Data Events (Data Events tốn thêm và phải bật riêng, vd S3 object-level, Lambda invoke); Trail → S3 + Log File Validation (chống sửa log); Organizations trail cho mọi account; Event History 90 ngày.
- **Giới hạn / bẫy:** CloudTrail ghi API — không ghi metric hiệu năng, không thay CloudWatch.
- **Ghi nhớ:** *Hỏi "who did what" là CloudTrail, khỏi suy nghĩ.*

## AWS Config

- **Là gì:** Ghi lại cấu hình resource theo thời gian + đánh giá tuân thủ bằng Config Rules.
- **Hay bị hỏi:** "Resource đã từng được cấu hình thế nào?", "S3 bucket nào không mã hóa?", "SG nào mở 0.0.0.0/0?" → Config. Remediation tự động qua SSM Automation. Aggregator multi-account/Region.
- **Giới hạn / bẫy:** Config là **detective**, không ngăn chặn từ đầu — ngăn chặn là SCP/IAM.
- **Ghi nhớ:** *Config = hồ sơ cấu hình + máy chấm điểm compliance.*

## WAF / Shield (khái niệm)

- **Là gì:** WAF = tường lửa Layer 7 cho HTTP (lọc SQL injection, XSS, IP, geo, rate). Shield = chống DDoS; Shield Standard mặc định miễn phí, Shield Advanced trả phí + bảo vệ sâu hơn + đội DRT.
- **Hay bị hỏi:** WAF gắn vào CloudFront / ALB / API Gateway. DDoS Layer 3/4 → Shield; tấn công ứng dụng Layer 7 → WAF.
- **Giới hạn / bẫy:** WAF không thay Security Group: WAF lọc nội dung HTTP, SG lọc IP/port ở tầng mạng.
- **Ghi nhớ:** *DDoS = Shield, request HTTP độc hại = WAF.*

## Step Functions

- **Là gì:** Điều phối workflow dạng state machine trực quan: chuỗi Lambda/dịch vụ, rẽ nhánh, retry, chờ duyệt.
- **Hay bị hỏi:** Standard vs Express workflow (Standard: chạy dài, exactly-once, human approval; Express: ngắn, throughput cao — khái niệm); Error handling Retry/Catch tích hợp; thay thế "Lambda gọi Lambda" rối rắm; việc dài hơn Lambda 15 phút nhưng chia được thành bước.
- **Giới hạn / bẫy:** Step Functions điều phối, không tự tính toán — tính toán vẫn do Lambda/ECS... làm.
- **Ghi nhớ:** *Nhiều bước + rẽ nhánh + retry + chờ người = Step Functions.*

## Kinesis (khái niệm)

- **Là gì:** Họ thu thập/xử lý dữ liệu streaming real-time.
- **Hay bị hỏi:** **Data Streams**: tự xây consumer, real-time thật, lưu stream ngắn hạn để replay. **Data Firehose**: nạp stream vào S3/Redshift/OpenSearch gần real-time, gần như không code, có buffering. **Video Streams**: stream video từ thiết bị.
- **Giới hạn / bẫy:** Cần đơn giản "gửi sự kiện A → B" thôi thì SQS/SNS/EventBridge đủ — đừng chọn Kinesis quá tay. Cần phân tích/tiêu thụ stream tốc độ cao, nhiều consumer đọc lại → mới Kinesis Data Streams.
- **Ghi nhớ:** *Firehose = đổ vào kho. Streams = tự xử lý dòng chảy.*

## Athena / Glue (khái niệm)

- **Là gì:** Athena = truy vấn SQL trực tiếp trên S3, serverless, trả theo dữ liệu scan. Glue = ETL serverless + Data Catalog (metadata) + Crawler tự khám phá schema.
- **Hay bị hỏi:** Cặp đôi kinh điển: Glue Crawler tạo Catalog → Athena query S3 như bảng. Glue ETL transform/clean data trước khi phân tích. Tối ưu Athena: partition dữ liệu, dùng định dạng cột (Parquet...) để scan ít hơn.
- **Giới hạn / bẫy:** Athena là công cụ truy vấn ad-hoc trên data lake — cần data warehouse hiệu năng ổn định, concurrency cao cho BI → Redshift.
- **Ghi nhớ:** *Data nằm yên trên S3 mà vẫn query SQL được = Athena (+ Glue Catalog).*

---

## Bảng Tóm Tắt 1 Dòng — Tất Cả

| Dịch vụ | 1 dòng |
|---|---|
| IAM | Người/role + policy quyền |
| Organizations | Nhiều account + SCP + billing chung |
| EC2 | Máy ảo toàn quyền |
| Lambda | Code theo sự kiện, ≤15 phút |
| S3 | Object storage, 11 số 9 durability |
| EBS | Ổ block cho 1 EC2, 1 AZ |
| EFS | File chung NFS cho nhiều EC2 Linux |
| RDS | SQL managed truyền thống |
| Aurora | SQL managed hiệu năng cao của AWS |
| DynamoDB | NoSQL key-value serverless, scale cực lớn |
| ElastiCache | Cache in-memory Redis/Memcached |
| VPC | Mạng riêng, subnet, NAT, endpoint |
| Route 53 | DNS + routing + health check |
| CloudFront | CDN edge cache |
| ELB | ALB=L7, NLB=L4, GWLB=firewall appliance |
| Auto Scaling | Tự co giãn số lượng tài nguyên |
| SQS | Queue — decouple, buffer |
| SNS | Pub/sub — fanout thông báo |
| EventBridge | Event bus + lịch cron |
| API Gateway | Cửa ngõ quản lý API |
| CloudFormation | IaC dạng stack/template |
| ECS/EKS/Fargate | Container: AWS-native / K8s / serverless |
| KMS | Quản lý khóa mã hóa |
| CloudWatch | Metrics, logs, alarms |
| CloudTrail | Audit API: ai làm gì |
| AWS Config | Lịch sử cấu hình + compliance rules |
| WAF/Shield | Lọc HTTP độc / chống DDoS |
| Step Functions | Workflow nhiều bước có trạng thái |
| Kinesis | Streaming data real-time |
| Athena/Glue | Query S3 bằng SQL / ETL + catalog |
