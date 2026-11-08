# Cheatsheet Tổng Hợp SAA-C03 — Ôn Thi Nước Rút

> Cách dùng: học thuộc bảng keyword trước. Đề thi SAA-C03 thường không hỏi thẳng tên dịch vụ — đề cho **tình huống + keyword**, đáp án nằm ở keyword đó.

---

## 1. Bảng Keyword Trong Đề → Dịch Vụ / Đáp án

| # | Keyword / tình huống trong đề | Dịch vụ / Đáp án |
|---|---|---|
| 1 | sudden spike in traffic, unpredictable workload | DynamoDB On-Demand / Lambda |
| 2 | predictable traffic, steady workload (để rẻ hơn) | DynamoDB Provisioned + Auto Scaling |
| 3 | decouple components, loose coupling | SQS |
| 4 | fanout (1 tin → nhiều nơi nhận) | SNS + SQS (SNS publish, nhiều SQS queue subscribe) |
| 5 | order matters, exactly-once processing | SQS FIFO |
| 6 | petabyte data warehouse, OLAP, complex queries | Redshift |
| 7 | in-memory cache, sub-millisecond latency | ElastiCache / DynamoDB DAX |
| 8 | cache cho DynamoDB, microsecond latency | DAX |
| 9 | cache session, leaderboard, pub/sub | ElastiCache for Redis |
| 10 | global users, low latency static content | CloudFront |
| 11 | 2 static IP addresses, TCP/UDP, gaming, IoT | Global Accelerator |
| 12 | WORM, compliance, cannot delete / immutable backup | S3 Object Lock (Governance / Compliance mode) |
| 13 | rotate secrets automatically | Secrets Manager |
| 14 | store configuration / parameter, free tier | SSM Parameter Store |
| 15 | audit who did what, API calls history | CloudTrail |
| 16 | resource configuration history, compliance rules | AWS Config |
| 17 | metrics and alarms, logs, performance monitoring | CloudWatch |
| 18 | managed NAT cho private subnet ra internet | NAT Gateway |
| 19 | free private access to S3 / DynamoDB from VPC | Gateway VPC Endpoint |
| 20 | private access to AWS services (hầu hết dịch vụ còn lại) | Interface VPC Endpoint (PrivateLink) |
| 21 | SQL with joins, relational database | RDS / Aurora |
| 22 | key-value, millions of requests per second, serverless DB | DynamoDB |
| 23 | shared file system for Linux instances, nhiều AZ | EFS |
| 24 | block storage for one instance | EBS |
| 25 | archive, rarely accessed, cheapest storage | S3 Glacier Deep Archive |
| 26 | disaster recovery, RPO/RTO minutes, scaled-down environment running | Warm Standby |
| 27 | graph database, relationships, recommendation | Neptune |
| 28 | ledger database, immutable verifiable history | QLDB |
| 29 | time-series database | Timestream (khái niệm) |
| 30 | data lake query with SQL, serverless, pay per query | Athena (truy vấn S3 bằng SQL) |
| 31 | ETL, serverless data integration, crawler | Glue |
| 32 | streaming data, real-time ingestion | Kinesis (Data Streams / Firehose / Video Streams) |
| 33 | workflow orchestration visual, state machine, human approval | Step Functions |
| 34 | container without managing servers | Fargate (ECS/EKS on Fargate) |
| 35 | send email | SES |
| 36 | transcoding video | MediaConvert (Elastic Transcoder là dịch vụ cũ — khái niệm) |
| 37 | single sign-on workforce, nhiều tài khoản AWS | IAM Identity Center |
| 38 | preventive guardrails multi-account | SCP (Service Control Policies) |
| 39 | detective guardrails | AWS Config rules / Security Hub / GuardDuty (tùy ngữ cảnh) |
| 40 | DDoS protection, Layer 7 | WAF (+ Shield Advanced — khái niệm) |
| 41 | third-party firewall appliance in VPC, inspect traffic | Gateway Load Balancer (GWLB) |
| 42 | hybrid DNS, on-prem ↔ VPC | Route 53 Resolver |
| 43 | shared VPC / resources across accounts | AWS RAM (Resource Access Manager) |
| 44 | private API, chỉ truy cập từ VPC | API Gateway private endpoint + resource policy |
| 45 | REST API, caching, throttling, API key | API Gateway |
| 46 | event-driven, schedule (cron), event bus, SaaS events | EventBridge |
| 47 | notification: email / SMS / push / HTTP | SNS |
| 48 | migrate database, minimal downtime | DMS (+ SCT để convert schema) |
| 49 | migrate servers on-prem → AWS | AWS Application Migration Service (MGN) |
| 50 | hybrid storage, on-prem truy cập S3, NFS/SMB, backup tape | Storage Gateway |
| 51 | transfer data lớn qua mạng chậm / offline, petabyte | Snowball / Snowmobile (họ Snow) |
| 52 | sync / transfer files giữa S3, EFS, on-prem, tăng tốc | DataSync / Transfer Family (SFTP/FTP vào S3/EFS) |
| 53 | centralized backup across AWS services | AWS Backup |
| 54 | encrypt data, managed keys, audit key usage | KMS |
| 55 | dedicated hardware security module, FIPS, own keys hoàn toàn | CloudHSM |
| 56 | threat detection, malicious activity, GuardDuty findings | GuardDuty |
| 57 | scan vulnerabilities trên EC2 / container images | Inspector |
| 58 | scan S3 tìm PII / sensitive data | Macie |
| 59 | tập hợp findings bảo mật về 1 chỗ | Security Hub |
| 60 | phân tích IAM policy, external access, unused access | IAM Access Analyzer |
| 61 | website static hosting rẻ nhất | S3 Static Website Hosting (+ CloudFront) |
| 62 | pre-signed URL | Chia sẻ S3 object tạm thời, có thời hạn, không cần public |
| 63 | tăng tốc upload/download S3 đường dài | S3 Transfer Acceleration / CloudFront |
| 64 | upload file lớn lên S3 (trên 5 GB single PUT) | S3 Multipart Upload |
| 65 | replicate S3 sang Region khác, compliance / latency | S3 Cross-Region Replication (CRR) |
| 66 | tự động chuyển S3 object sang lớp rẻ hơn theo tuổi | S3 Lifecycle Policies |
| 67 | xóa object sau X ngày tự động | S3 Lifecycle — Expiration |
| 68 | scale compute tự động theo traffic | Auto Scaling Group (ASG) |
| 69 | distribute traffic HTTP, path/host-based routing, Layer 7 | ALB |
| 70 | extreme performance, static IP, TCP/UDP, Layer 4 | NLB |
| 71 | sticky session | ALB (target group) / CLB cũ |
| 72 | SSL/TLS termination, quản lý certificate miễn phí | ACM (AWS Certificate Manager) + ALB/CloudFront |
| 73 | DNS, failover routing, health check | Route 53 |
| 74 | users gần nhất về mặt địa lý / latency thấp nhất | Route 53 Latency-based / Geolocation routing |
| 75 | blue/green, canary deployment | Route 53 Weighted / CodeDeploy / ALB weighted target groups |
| 76 | Infrastructure as Code | CloudFormation (AWS-native) / CDK / Terraform |
| 77 | serverless application, Lambda + API GW đóng gói | SAM |
| 78 | deploy container, không cần Kubernetes | ECS |
| 79 | Kubernetes chuẩn, đội đã biết K8s | EKS |
| 80 | message bị xử lý lỗi nhiều lần, poison pill | SQS Dead Letter Queue (DLQ) |
| 81 | message tồn đọng, xử lý batch, thứ tự không quan trọng | SQS Standard |
| 82 | long polling giảm request rỗng / giảm chi phí SQS | SQS Long Polling (WaitTimeSeconds > 0) |
| 83 | database read quá tải, tách read khỏi write | RDS Read Replica / Aurora Replica |
| 84 | database failover tự động, high availability | RDS Multi-AZ / Aurora |
| 85 | giảm tải database bằng cache read-through / lazy loading | ElastiCache + pattern lazy loading / write-through |
| 86 | kết nối on-prem ↔ AWS: nhanh, private, ổn định | Direct Connect (DX) |
| 87 | kết nối on-prem ↔ AWS: nhanh gọn qua internet, mã hóa | Site-to-Site VPN |
| 88 | DX cần dự phòng rẻ | VPN làm backup cho Direct Connect |
| 89 | nhiều VPC kết nối hub-and-spoke, quản lý tập trung | Transit Gateway |
| 90 | kết nối 2 VPC với nhau (cùng/khác account, khác Region được) | VPC Peering (không transitive) |
| 91 | IPv6 + security (cặp quen thuộc trong đề) | Security Group hỗ trợ IPv6; Egress-only Internet Gateway cho IPv6 |
| 92 | chỉ cho phép 1 dịch vụ / prefix list qua SG (vd S3, DynamoDB) | Managed Prefix List trong Security Group rule |
| 93 | block IP cụ thể ở tầng subnet | NACL (SG không có Deny, không block IP riêng lẻ theo kiểu deny) |
| 94 | Windows shared file system | FSx for Windows File Server |
| 95 | high-performance computing, Lustre, scratch file system | FSx for Lustre |
| 96 | real-time processing, windowed aggregation trên stream | Kinesis Data Analytics / Managed Service for Apache Flink (khái niệm) |
| 97 | load data streaming vào S3/Redshift gần real-time, không code | Kinesis Data Firehose |
| 98 | Big Data processing, Hadoop, Spark | EMR |
| 99 | search / log analytics, full-text search | OpenSearch Service |
| 100 | cost optimization: tắt tài nguyên idle, right-sizing | Trusted Advisor / Compute Optimizer / Cost Explorer |

---

## 2. Số Liệu Hay Hỏi

### Giới hạn kinh điển — thuộc lòng

| Dịch vụ | Số liệu | Ghi chú thi |
|---|---|---|
| Lambda | Timeout tối đa **15 phút** | Quá 15 phút → nghĩ Step Functions / ECS / EC2 |
| Lambda | Đồng bộ payload / async | Hỏi theo ngữ cảnh, đừng nhầm timeout với API Gateway |
| API Gateway | Timeout tích hợp mặc định hay gặp **29 giây** (REST API) | Tác vụ dài → trả về ngay + SQS/Lambda async |
| SQS | Retention tối đa **14 ngày** | Mặc định 4 ngày |
| SQS | Visibility timeout tối đa **12 giờ** | Mặc định 30 giây |
| SQS FIFO | **300 TPS** không batch, **3.000 TPS** khi batching | Standard = gần như không giới hạn, best-effort ordering |
| S3 | Durability **99.999999999% (11 số 9)** | Durability ≠ Availability — đề rất thích bẫy cặp này |
| S3 | Object tối đa **5 TB**; single PUT tối đa **5 GB** | Lớn hơn → Multipart Upload |
| RDS | Automated backup retention **1–35 ngày** | 0 ngày = tắt automated backup |
| Aurora | Storage tự scale tối đa **128 TB** | Aurora storage tự động mở rộng |
| Aurora | Tối đa **15 Aurora Replicas** | RDS Read Replica thường tối đa 5 (đa số engine cổ điển) |
| DynamoDB DAX | Độ trễ **microsecond** | ElastiCache thường được mô tả sub-millisecond |
| ElastiCache | Độ trễ **sub-millisecond** | So sánh với DAX ở trên |
| CloudFront | — | Cache tại edge; origin: S3, ALB, EC2, HTTP bất kỳ |

### DR — xếp theo RTO tăng dần (chậm → nhanh), chi phí tăng theo

| Thứ tự | Chiến lược | RTO tương đối | Chi phí tương đối | Ý tưởng |
|---|---|---|---|---|
| 1 (chậm nhất) | Backup and Restore | Giờ | Thấp nhất | Chỉ có backup, khi có sự cố mới dựng lại |
| 2 | Pilot Light | Chục phút – giờ | Thấp | Phần lõi tối thiểu luôn chạy, còn lại bật khi cần |
| 3 | Warm Standby | Phút | Trung bình | Môi trường thu nhỏ (scaled-down) đang chạy sẵn |
| 4 (nhanh nhất) | Multi-Site Active-Active | Gần real-time | Cao nhất | Cả 2 nơi đều phục vụ traffic |

> Quy tắc chọn DR: **RTO/RTO càng nhỏ → càng đắt.** Đề cho ngân sách thấp → Backup and Restore. Đề cho "minutes" → Warm Standby. Đề cho "scaled-down version running" → chính là định nghĩa Warm Standby.

### Cặp số liệu hay bị bẫy

| Bẫy | Phân biệt đúng |
|---|---|
| Durability vs Availability (S3) | Durability = không mất dữ liệu (11 số 9). Availability = truy cập được, thấp hơn durability |
| SQS visibility timeout vs retention | Visibility = đang xử lý thì ẩn tin bao lâu (≤12h). Retention = tin sống trong queue bao lâu (≤14 ngày) |
| Multi-AZ vs Read Replica | Multi-AZ = HA / failover, **không** tăng read. Read Replica = tăng read, **không** tự failover kiểu Multi-AZ |
| CloudTrail retention | CloudTrail Event History mặc định 90 ngày; muốn lâu hơn → gửi log vào S3 |

---

## 3. Cây Quyết Định (ASCII)

### 3.1 Chọn Storage

```
Cần lưu trữ gì?
│
├─ Object (file, ảnh, video, backup, data lake, static web)?
│   └─ S3
│       ├─ Truy cập thường xuyên ──────────► S3 Standard
│       ├─ Ít truy cập, vẫn cần nhanh ─────► S3 Standard-IA / One Zone-IA
│       ├─ Không rõ pattern truy cập ──────► S3 Intelligent-Tiering
│       └─ Archive lâu, hiếm khi lấy ──────► Glacier Instant / Flexible / Deep Archive (rẻ nhất)
│
├─ Block storage gắn vào 1 EC2 (như ổ cứng)?
│   └─ EBS
│       ├─ General purpose ────────────────► gp3 (mặc định nên chọn)
│       ├─ IOPS cực cao, database ─────────► io2 / io1
│       ├─ Throughput cao, big data ───────► st1 (HDD)
│       └─ Rẻ nhất, archive lạnh ──────────► sc1 (HDD)
│   (Cần tốc độ vật lý tạm thời, mất khi stop/terminate? → Instance Store)
│
├─ File system chia sẻ cho NHIỀU instance cùng mount?
│   ├─ Linux / NFS ────────────────────────► EFS
│   ├─ Windows / SMB ──────────────────────► FSx for Windows
│   └─ HPC, throughput cực cao ────────────► FSx for Lustre
│
└─ Hybrid: on-prem cần truy cập storage AWS như file local?
    └─ Storage Gateway
```

### 3.2 Chọn Database

```
Dữ liệu có cấu trúc quan hệ (relational, JOIN, transaction phức tạp)?
│
├─ CÓ
│   ├─ Muốn AWS-managed tương thích MySQL/PostgreSQL, scale tốt hơn RDS thường?
│   │   └─ Aurora
│   ├─ Cần engine cụ thể (Oracle, SQL Server...) / kiểm soát truyền thống?
│   │   └─ RDS
│   └─ Phân tích OLAP, data warehouse, petabyte, query tổng hợp?
│       └─ Redshift
│
└─ KHÔNG (NoSQL / chuyên biệt)
    ├─ Key-value, scale triệu request/s, serverless ──► DynamoDB (+ DAX nếu cần microsecond)
    ├─ Document / key-value tương thích MongoDB ───────► DocumentDB (khái niệm)
    ├─ Graph: quan hệ giữa các thực thể là trọng tâm ──► Neptune
    ├─ In-memory: cache / session / leaderboard ──────► ElastiCache (Redis / Memcached)
    ├─ Ledger: lịch sử bất biến, kiểm chứng được ─────► QLDB
    ├─ Time-series: dữ liệu theo thời gian, IoT ──────► Timestream (khái niệm)
    └─ Search: full-text, log analytics ──────────────► OpenSearch

Chỉ cần truy vấn data lake trên S3 bằng SQL, không muốn dựng DB?
└─ Athena (query) + Glue (catalog / ETL)
```

### 3.3 Chọn Compute

```
Chạy code / workload gì?
│
├─ Event-driven, chạy ngắn (≤15 phút), không muốn quản server?
│   └─ Lambda
│       └─ Workflow nhiều bước / chờ người duyệt / chạy dài theo bước?
│           └─ Lambda + Step Functions
│
├─ Container?
│   ├─ Không muốn quản server ─────────────► ECS / EKS on Fargate
│   ├─ AWS-native, đơn giản ────────────────► ECS
│   └─ Cần Kubernetes chuẩn / portability ─► EKS
│
├─ Cần toàn quyền OS, license riêng, workload dài hạn ổn định?
│   └─ EC2 (+ Auto Scaling Group + ELB cho HA/scale)
│       ├─ Traffic thay đổi ───────────────► ASG + ALB/NLB
│       └─ Batch / HPC rời rạc ────────────► EC2 Spot / Batch (AWS Batch)
│
├─ Web app / API, không muốn quản hạ tầng, chấp nhận platform của AWS?
│   └─ Elastic Beanstalk (PaaS) / App Runner (khái niệm)
│
└─ Chỉ là website tĩnh?
    └─ Không cần compute: S3 Static Hosting + CloudFront
```

---

## 4. Năm Câu Thần Chú Trước Khi Vào Phòng Thi

1. **Decouple = SQS. Fanout = SNS + SQS. Order/exactly-once = SQS FIFO.**
2. **Audit người = CloudTrail. Config của resource = AWS Config. Metrics = CloudWatch.**
3. **Multi-AZ = HA, Read Replica = scale read. Đừng bao giờ đánh đồng.**
4. **Security Group = stateful + chỉ Allow. NACL = stateless + có Deny.**
5. **Rẻ nhất thường là đáp án sai nếu đề đòi hỏi HA / low latency / RTO nhỏ — đọc yêu cầu hiệu năng trước, giá sau.**
