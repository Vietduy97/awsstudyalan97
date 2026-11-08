# Phân Biệt Các Dịch Vụ SAA-C03 — Bảng So Sánh & Quy Tắc Chọn

> Nguyên tắc đọc: mỗi nhóm gồm **bảng so sánh** + **quy tắc chọn** (câu chốt để chọn đáp án trong phòng thi).

---

## 1. S3 vs EBS vs EFS

| Tiêu chí | S3 | EBS | EFS |
|---|---|---|---|
| Kiểu lưu trữ | Object | Block | File (NFS) |
| Gắn vào | Không gắn — truy cập qua API/HTTP | 1 EC2 (thường), cùng AZ | Nhiều EC2 cùng lúc |
| Phạm vi | Region (bucket), toàn cục qua HTTP | 1 Availability Zone | Multi-AZ trong 1 Region |
| Quy mô | Gần như vô hạn, object tới 5 TB | Theo size volume chọn trước | Tự scale theo dung lượng |
| Dùng cho | File, ảnh, backup, data lake, static web | Boot volume, database trên EC2, ổ cứng | Thư mục dùng chung, home directory, CMS |
| Hệ điều hành | Không liên quan OS | Theo instance gắn vào | Linux (NFS) |

**Quy tắc chọn:**
- Nhiều instance **cùng mount** 1 hệ thống file → **EFS**.
- Ổ đĩa cho **1 instance** → **EBS**.
- Lưu **file/object** truy cập qua mạng, backup, web tĩnh → **S3**.

---

## 2. RDS vs Aurora vs DynamoDB vs Redshift vs ElastiCache

| Tiêu chí | RDS | Aurora | DynamoDB | Redshift | ElastiCache |
|---|---|---|---|---|---|
| Mô hình | Relational SQL | Relational SQL | NoSQL key-value/document | Relational cột — Data Warehouse | In-memory cache |
| Workload | OLTP truyền thống | OLTP hiệu năng/scale cao | OLTP scale cực lớn, access pattern rõ | OLAP, BI, phân tích petabyte | Cache, session, leaderboard |
| JOIN / SQL phức tạp | Có | Có | **Không** | Có (query tổng hợp nặng) | Không |
| Tương thích | MySQL, PostgreSQL, MariaDB, Oracle, SQL Server | Chỉ MySQL, PostgreSQL | API riêng | PostgreSQL-based SQL | Redis / Memcached protocol |
| Scale | Multi-AZ + Read Replica | 15 replicas, storage 128 TB | On-demand/provisioned, gần như vô hạn | Cluster / Serverless, petabyte | Thêm node / replica |
| Serverless? | Không (có biến thể riêng) | Có Aurora Serverless | Có (bản chất serverless) | Có Redshift Serverless | Có biến thể serverless (khái niệm) |

**Quy tắc chọn:**
- Cần **Oracle / SQL Server** → **RDS** (Aurora không có).
- SQL + muốn AWS tối ưu mạnh hơn RDS → **Aurora**.
- Triệu request/s, key-value, không JOIN → **DynamoDB**.
- Truy vấn **phân tích** trên dữ liệu khổng lồ → **Redshift**.
- Không phải DB chính — chỉ **tăng tốc đọc lặp lại** → **ElastiCache** đặt trước DB.

---

## 3. ALB vs NLB vs GWLB (vs CLB cũ)

| Tiêu chí | ALB | NLB | GWLB | CLB (Classic) |
|---|---|---|---|---|
| Layer | 7 — HTTP/HTTPS | 4 — TCP/UDP/TLS | 3 — IP packet | 4/7 đời cũ |
| Routing theo | Path, host, header, query | Port/protocol | Chèn appliance kiểm tra traffic | Cơ bản |
| Target | EC2, IP, container, Lambda | EC2, IP, container, ALB | Firewall/IDS appliance bên thứ ba | EC2 |
| IP tĩnh / Elastic IP | Không — dùng DNS name | **Có** | — | Không |
| Hiệu năng / độ trễ | Tốt | Cực cao, ultra-low latency | Theo appliance | Thấp nhất |
| Use case điển hình | Web, API, microservices | Gaming, IoT, TCP/UDP, cần IP tĩnh | Kiểm tra/chặn traffic tập trung | Chỉ khi đề nhắc legacy |

**Quy tắc chọn:**
- Đề nhắc **path/host-based routing, HTTP** → **ALB**.
- Đề nhắc **static IP, TCP/UDP, extreme performance** → **NLB**.
- Đề nhắc **third-party firewall appliance, inspect all traffic** → **GWLB**.
- **CLB** gần như luôn là đáp án sai trong đề mới, trừ ngữ cảnh legacy rõ ràng.

---

## 4. SQS vs SNS vs EventBridge (vs Step Functions)

| Tiêu chí | SQS | SNS | EventBridge | Step Functions |
|---|---|---|---|---|
| Bản chất | Queue (hàng đợi) | Pub/Sub push | Event bus + rule + schedule | Workflow / state machine |
| Mô hình nhận | Consumer **pull** (tự lấy) | Subscriber nhận **push** | Target được gọi theo rule | Các bước chạy theo thứ tự/trạng thái |
| Lưu tin chờ? | Có — tới 14 ngày | Không lưu kiểu queue | Có archive/replay event | Lưu trạng thái workflow đang chạy |
| Thứ tự / exactly-once | Có với FIFO | Có với FIFO topic + FIFO queue | Không phải thế mạnh | Điều phối có trạng thái, retry/catch |
| Fanout | Không tự fanout | **Thế mạnh chính** | Route 1 sự kiện → nhiều target | Không phải để fanout |
| Lịch cron | Không | Không | **Có** | Có thể được trigger theo lịch |
| Use case | Decouple, buffer, chống quá tải | Thông báo, fanout SNS→SQS | Sự kiện AWS/SaaS, lịch, event-driven | Nhiều bước, rẽ nhánh, chờ người duyệt |

**Quy tắc chọn:**
- **Decouple + xử lý sau cũng được** → SQS.
- **1 tin → nhiều nơi nhận ngay** → SNS.
- **Sự kiện + rule phức tạp + cron + SaaS/AWS events** → EventBridge.
- **Quy trình nhiều bước có trạng thái, retry, approval** → Step Functions.
- Fanout bền vững kinh điển: **SNS publish → nhiều SQS queue → mỗi consumer tự xử lý.**

---

## 5. CloudWatch vs CloudTrail vs AWS Config

| Tiêu chí | CloudWatch | CloudTrail | AWS Config |
|---|---|---|---|
| Trả lời câu hỏi | Hệ thống **khỏe/chậm** thế nào? | **Ai** đã làm **gì**? | Resource **đang/đã từng cấu hình** thế nào, có **tuân thủ** không? |
| Dữ liệu | Metrics, logs, alarms | API call records | Configuration items, config history |
| Ví dụ | CPU > 80% → alarm | User X xóa S3 bucket lúc 3h | Bucket nào tắt encryption? SG nào mở port 22 ra internet? |
| Hành động | Alarm → SNS / ASG / EC2 action | Gửi log vào S3, validation chống sửa | Rule không tuân thủ → remediation (SSM) |
| Loại kiểm soát | Monitoring | Audit (detective) | Compliance (detective) |

**Quy tắc chọn:**
- Thấy chữ **metrics / alarm / log performance** → CloudWatch.
- Thấy chữ **who / API call / audit** → CloudTrail.
- Thấy chữ **configuration history / compliance rule / resource compliant?** → AWS Config.

---

## 6. Security Group vs NACL

| Tiêu chí | Security Group (SG) | Network ACL (NACL) |
|---|---|---|
| Gắn vào | Instance / ENI | Subnet |
| Stateful? | **Stateful** — traffic trả về tự được phép | **Stateless** — phải mở cả 2 chiều |
| Rule | Chỉ **Allow**, không có Deny | Có cả **Allow và Deny** |
| Đánh giá rule | Tất cả rule cùng áp dụng | Theo **số thứ tự, thấp trước**, dừng ở rule khớp đầu tiên |
| Phạm vi mặc định | Mặc định chặn inbound, cho outbound | Mặc định cho tất cả (default NACL); custom NACL mặc định chặn tất cả |
| Dùng chặn 1 IP cụ thể | Không (không có Deny) | **Có — Deny rule theo IP** |

**Quy tắc chọn:**
- **Block 1 IP / dải IP cụ thể** → NACL (SG không Deny được).
- Kiểm soát port cho **từng instance/ứng dụng** → SG.
- Thực tế tốt nhất: dùng cả hai lớp (defense in depth), SG là lớp chính.

---

## 7. Gateway Endpoint vs Interface Endpoint

| Tiêu chí | Gateway VPC Endpoint | Interface VPC Endpoint (PrivateLink) |
|---|---|---|
| Dịch vụ hỗ trợ | Chỉ **S3 và DynamoDB** | Hầu hết dịch vụ AWS còn lại + dịch vụ PrivateLink |
| Cách hoạt động | Thêm route vào route table | Tạo ENI có IP riêng trong subnet |
| Chi phí | **Miễn phí** | Có phí theo giờ ENI + dữ liệu |
| Security Group | Không dùng SG (dùng endpoint policy + route) | Dùng SG trên ENI |
| Dùng khi | VPC truy cập S3/DynamoDB **riêng tư, không qua internet** | API Gateway private, Secrets Manager, ... từ VPC |

**Quy tắc chọn:**
- **S3 / DynamoDB + private + free** → Gateway Endpoint.
- Dịch vụ khác cần truy cập private từ VPC → Interface Endpoint.

---

## 8. EBS Volume Types (+ Instance Store)

| Loại | Đĩa | Dùng cho | Ghi chú thi |
|---|---|---|---|
| gp3 | SSD | Mặc định cân bằng: boot, app thường | Lựa chọn mặc định tốt nhất, tách IOPS/throughput khỏi dung lượng |
| gp2 | SSD | Đời trước của gp3 | IOPS gắn với dung lượng volume |
| io2 / io1 | SSD | Database, workload cần IOPS cực cao, ổn định | Đắt nhất; io2 bền/tốt hơn io1 |
| st1 | HDD | Throughput cao: big data, log, data warehouse | Không dùng làm boot volume |
| sc1 | HDD | Rẻ nhất: archive lạnh, ít truy cập | Không dùng làm boot volume, throughput thấp nhất |
| Instance Store | Vật lý gắn kèm host | Cache, buffer, dữ liệu **tạm** tốc độ cực cao | **Mất dữ liệu khi stop/terminate** — không phải storage bền |

**Quy tắc chọn:**
- Không biết chọn gì → **gp3**.
- "Highest IOPS / mission-critical database" → **io2**.
- "Cheap + throughput, không cần IOPS" → **st1**. "Cheapest, cold" → **sc1**.
- "Ephemeral / temporary / mất cũng không sao nhưng phải cực nhanh" → **Instance Store**.

---

## 9. S3 Storage Classes

| Class | Availability / AZ | Chi phí | Thời gian truy xuất | Min storage duration | Dùng khi |
|---|---|---|---|---|---|
| Standard | Multi-AZ, cao nhất nhóm thường | Cao nhất | Milliseconds | Không có | Truy cập thường xuyên |
| Intelligent-Tiering | Multi-AZ | Tự tối ưu | Milliseconds | Không có | Pattern truy cập **không đoán được** |
| Standard-IA | Multi-AZ | Thấp | Milliseconds | **30 ngày** | Ít truy cập nhưng cần lấy ngay, vẫn cần bền |
| One Zone-IA | **Chỉ 1 AZ** | Thấp hơn Standard-IA | Milliseconds | **30 ngày** | Ít truy cập + dữ liệu **tạo lại được** (mất AZ là mất dữ liệu) |
| Glacier Instant Retrieval | Multi-AZ | Thấp | Milliseconds | 90 ngày* | Archive nhưng thỉnh thoảng cần lấy ngay |
| Glacier Flexible Retrieval | Multi-AZ | Thấp hơn nữa | Phút – giờ (theo tier lấy) | **90 ngày** | Archive, lấy chậm được |
| Glacier Deep Archive | Multi-AZ | **Rẻ nhất** | Giờ | **180 ngày** | Archive 7–10 năm, compliance, gần như không lấy |

\* Glacier Instant Retrieval 90 ngày là mốc quen thuộc thường được dạy kèm nhóm Glacier; khi đề không nhấn vào con số này, chỉ cần nhớ: *archive → càng lạnh càng rẻ, lấy càng chậm.*

**Quy tắc chọn:**
- Không rõ tần suất truy cập → **Intelligent-Tiering**.
- Ít truy cập, cần ngay, dữ liệu quan trọng → **Standard-IA**.
- Ít truy cập, dữ liệu **reproducible** → **One Zone-IA** (rẻ hơn, đánh đổi 1 AZ).
- Rẻ nhất tuyệt đối, chờ hàng giờ được → **Deep Archive**.
- Bẫy kinh điển: thu hồi sớm hơn min duration vẫn **bị tính phí đủ** min duration.

---

## 10. Multi-AZ vs Read Replica (RDS)

| Tiêu chí | Multi-AZ | Read Replica |
|---|---|---|
| Mục đích | High Availability / failover | Scale **read** |
| Bản sao có đọc được không? | Standby — **không** phục vụ read | **Có** — phục vụ read |
| Đồng bộ | Synchronous (standby) | Asynchronous |
| Failover | **Tự động**, DNS chuyển sang standby | Không tự — có thể promote thủ công thành DB độc lập |
| Phạm vi | Trong 1 Region (khác AZ) | Cùng Region hoặc **cross-Region** |
| Tăng hiệu năng write? | Không | Không (chỉ giảm tải read cho primary) |

**Quy tắc chọn:**
- Đề hỏi **disaster / failover / availability** → Multi-AZ.
- Đề hỏi **read traffic quá tải, báo cáo làm chậm DB chính** → Read Replica.
- Cần cả hai → dùng **cả hai**, đây là tổ hợp rất hay ra thi.

---

## 11. Provisioned vs On-Demand (DynamoDB)

| Tiêu chí | Provisioned | On-Demand |
|---|---|---|
| Cách tính | Đặt trước RCU/WCU (+ Auto Scaling) | Trả theo request thực tế |
| Phù hợp | Traffic **ổn định, đoán trước được** | Traffic **thất thường, spike, mới launch chưa biết** |
| Chi phí | Rẻ hơn khi dùng đều | Đắt hơn theo đơn vị request, nhưng không lo throttle vì thiếu capacity |
| Rủi ro | Đặt thiếu → throttling; đặt thừa → lãng phí | Khó dự toán ngân sách hơn |
| Keyword đề | predictable, steady, cost-optimize | unpredictable, spiky, sudden spike, unknown |

**Quy tắc chọn:** Đoán được traffic → Provisioned để rẻ. Không đoán được / spike → On-Demand để an toàn.

---

## 12. ECS EC2 Launch Type vs Fargate

| Tiêu chí | ECS on EC2 | Fargate |
|---|---|---|
| Quản lý server | Tự quản EC2 (patch, scale cluster) | **Không quản server** |
| Tính tiền | Theo EC2 (kể cả lúc task ít) | Theo vCPU/RAM của task khi chạy |
| Kiểm soát | Cao: chọn instance, GPU, OS, daemon đặc biệt | Thấp: chỉ khai báo task |
| Phù hợp | Workload ổn định, dài hạn, cần phần cứng đặc thù, tối ưu chi phí ở scale lớn | Workload thất thường, đội nhỏ, muốn nhanh gọn |
| Bẫy | Cluster rỗng vẫn tốn tiền EC2 | Không truy cập được host bên dưới |

**Quy tắc chọn:** "No servers to manage" → **Fargate**. "Need GPU / special instance / full control" → **EC2 launch type**.

---

## 13. Disaster Recovery — 4 Chiến Lược

| Chiến lược | Cách làm | RTO tương đối | RPO tương đối | Chi phí | Keyword nhận diện |
|---|---|---|---|---|---|
| Backup and Restore | Backup dữ liệu, sự cố thì restore + dựng lại | Giờ (lâu nhất) | Theo tần suất backup (giờ) | Thấp nhất | cheapest, backup only |
| Pilot Light | Lõi tối thiểu (vd DB replicate) luôn chạy, phần còn lại tắt | Chục phút – giờ | Nhỏ hơn (phút) | Thấp | core services always on, pilot light |
| Warm Standby | Môi trường **thu nhỏ đang chạy sẵn**, sự cố thì scale lên | **Phút** | Giây – phút | Trung bình | scaled-down environment running |
| Multi-Site Active-Active | Cả 2 Region cùng phục vụ traffic | Gần **real-time** (nhỏ nhất) | Gần **0** | Cao nhất | active-active, zero downtime |

**Định nghĩa phải thuộc:**
- **RTO** (Recovery Time Objective) = thời gian tối đa chấp nhận **hệ thống chết** sau sự cố.
- **RPO** (Recovery Point Objective) = lượng **dữ liệu tối đa chấp nhận mất**, tính ngược về thời điểm backup/replica gần nhất.

**Quy tắc chọn:** Ngân sách thấp + chịu downtime lâu → Backup and Restore. Cần phút → Warm Standby. Cần gần như không downtime/mất dữ liệu → Active-Active (và chấp nhận đắt nhất).

---

## 14. Route 53 Routing Policies — So Sánh Nhanh

| Policy | Cách chia | Dùng khi |
|---|---|---|
| Simple | 1 record, không health check logic | Website đơn giản |
| Weighted | Theo % trọng số (vd 90/10) | Blue/green, canary, A/B test, migration dần |
| Latency-based | Route tới Region độ trễ thấp nhất với user | User toàn cầu, tối ưu tốc độ |
| Geolocation | Theo vị trí địa lý của user (châu lục/quốc gia) | Nội dung bản địa hóa, tuân thủ pháp lý theo khu vực |
| Geoproximity | Theo khoảng cách + bias điều chỉnh | Dịch chuyển traffic dần giữa các Region (khái niệm nâng cao) |
| Failover | Primary → Secondary khi health check fail | Active-passive, DR đơn giản qua DNS |
| Multi-value Answer | Trả nhiều IP + health check từng cái | Tăng availability đơn giản kiểu nhiều record khỏe |

**Quy tắc chọn:**
- **% traffic** → Weighted. **Nhanh nhất cho user** → Latency. **Theo quốc gia** → Geolocation. **Chết thì chuyển** → Failover.

**Latency vs Geolocation — bẫy kinh điển:** Latency chọn theo **tốc độ mạng thực tế**, Geolocation chọn theo **vị trí pháp lý/nội dung** — user ở gần chưa chắc phải phục vụ nội dung của nước đó.

---

## 15. Secrets Manager vs Parameter Store

| Tiêu chí | Secrets Manager | SSM Parameter Store |
|---|---|---|
| Mục đích chính | **Secrets**: DB password, API key | Cấu hình + cả secret dạng SecureString |
| Tự động rotate | **Có, tích hợp sẵn** (đặc biệt RDS/Aurora/Redshift/DocumentDB) | Không có rotation tích hợp sẵn |
| Chi phí | Trả phí theo secret + API call | Standard tier miễn phí (giới hạn cơ bản); Advanced trả phí |
| Mã hóa | KMS | SecureString dùng KMS |
| Versioning / hierarchy | Có | Có hierarchy dạng path |
| Keyword đề | **rotate automatically**, database credentials | configuration, plain parameter, free |

**Quy tắc chọn:** Thấy chữ **rotate** → Secrets Manager, không tranh cãi. Chỉ lưu config/tham số thường, muốn rẻ/miễn phí → Parameter Store.

---

## 16. KMS vs CloudHSM

| Tiêu chí | KMS | CloudHSM |
|---|---|---|
| Bản chất | Dịch vụ quản lý khóa, **shared** hạ tầng do AWS quản | Cụm HSM **dedicated** riêng cho bạn |
| Ai quản lý khóa | AWS quản hạ tầng, bạn quản key policy | **Bạn toàn quyền** quản khóa trong HSM |
| Tích hợp dịch vụ AWS | Rất rộng (S3, EBS, RDS, Lambda...) | Hạn chế hơn, thường qua ứng dụng tự tích hợp |
| Chuẩn / compliance | Đáp ứng đa số nhu cầu thông thường | Khi quy định đòi **FIPS 140-2 Level 3 / dedicated HSM** (kiến thức khái niệm hay ra) |
| Vận hành | Gần như không vận hành | Tự lo HA cụm HSM, backup khóa |
| Audit | Qua CloudTrail tự nhiên | Theo cơ chế riêng của HSM/ứng dụng |

**Quy tắc chọn:**
- Mặc định mọi bài toán mã hóa trên AWS → **KMS**.
- Đề nhấn **dedicated, single-tenant HSM, bạn tự kiểm soát hoàn toàn khóa, compliance đặc thù** → **CloudHSM**.

---

## Bảng Chốt Cuối — 12 Cặp Dễ Nhầm Nhất

| Cặp dễ nhầm | Phân biệt 1 câu |
|---|---|
| CloudTrail vs Config | Trail = ai gọi API; Config = resource cấu hình ra sao |
| SG vs NACL | SG stateful + Allow-only; NACL stateless + có Deny |
| SQS vs SNS | SQS giữ tin chờ pull; SNS đẩy tin push |
| Multi-AZ vs Read Replica | Multi-AZ = sống sót; Replica = đọc nhanh hơn |
| ALB vs NLB | ALB đọc HTTP (L7); NLB chuyển TCP/UDP cực nhanh (L4) |
| Gateway vs Interface Endpoint | Gateway chỉ cho S3/DynamoDB và miễn phí; Interface cho phần còn lại, có phí |
| Secrets Manager vs Parameter Store | Cần rotate → Secrets Manager |
| KMS vs CloudHSM | Cần HSM riêng dedicated → CloudHSM, còn lại KMS |
| Durability vs Availability | Durability = không mất dữ liệu; Availability = vào được hệ thống |
| Provisioned vs On-Demand | Đoán được traffic → Provisioned; spike → On-Demand |
| Fargate vs EC2 launch type | Không quản server → Fargate |
| Backup&Restore vs Warm Standby | Chỉ có backup = Backup&Restore; có môi trường thu nhỏ đang chạy = Warm Standby |
