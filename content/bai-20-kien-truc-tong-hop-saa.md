# Bài 20 — Kiến Trúc Tổng Hợp SAA

## Mục tiêu bài học

- Ánh xạ được 4 domain của đề SAA-C03 với các pillars của AWS Well-Architected Framework để ôn tập có hệ thống trong tuần cuối.
- Thuộc hai bản kiến trúc mẫu: 3-tier truyền thống và serverless — bộ khung trả lời phần lớn câu hỏi scenario.
- Nắm playbook ra quyết định theo keyword, chiến thuật làm bài 130 phút / 65 câu, và checklist tuần cuối + ngày thi.

## Lý thuyết chính

### 1. Thông tin đề thi — thuộc lòng

- **Mã đề:** SAA-C03 — AWS Certified Solutions Architect – Associate.
- **Số câu:** 65 câu, trong đó **50 câu tính điểm + 15 câu không tính điểm** (thử nghiệm của AWS, **không phân biệt được** câu nào là câu nào — nên phải làm nghiêm túc cả 65 câu).
- **Thời gian:** **130 phút** → trung bình khoảng **2 phút/câu**.
- **Điểm đạt:** **720/1000**.
- **Lệ phí:** **$150**.
- **Ngôn ngữ:** **KHÔNG có bản tiếng Việt** — thi hoàn toàn bằng **tiếng Anh**. Đây là lý do toàn bộ quá trình học phải drill keyword tiếng Anh song song với lý thuyết tiếng Việt.

### 2. Ánh xạ 4 domain ↔ Well-Architected pillars

| Domain đề thi | Trọng số | Pillars liên quan nhất | Nội dung trọng tâm |
|---|---|---|---|
| **Design Secure Architectures** | **30%** | Security | IAM least privilege, KMS encryption, VPC/private subnet, Security Group, WAF, Secrets Manager |
| **Design Resilient Architectures** | **26%** | Reliability | Multi-AZ, Multi-Region, ASG, ELB, DR (RPO/RTO), decoupling bằng SQS |
| **Design High-Performing Architectures** | **24%** | Performance Efficiency | Cache (ElastiCache, CloudFront), read replica, chọn đúng compute/storage, DynamoDB |
| **Design Cost-Optimized Architectures** | **20%** | Cost Optimization | Savings Plans, Spot, S3 Lifecycle, rightsize, xóa tài nguyên mồ côi |

Hai pillars còn lại của Well-Architected — **Operational Excellence** và **Sustainability** — không có domain riêng nhưng vẫn xuất hiện lồng ghép (CloudWatch, CloudFormation/IaC...).

Cách dùng bảng này khi ôn: domain **Secure 30% là lớn nhất** — đừng để mất điểm ở IAM, encryption, network security. Nhưng cả 4 domain đều phải qua mức tối thiểu an toàn; đề không cho phép "bỏ hẳn" một domain.

### 3. Kiến trúc mẫu 1 — 3-tier chuẩn (bản EC2/ECS)

Đây là "bộ khung quốc dân" của đề SAA. Thuộc luồng đi của một request:

```
User → Route 53 (DNS) → CloudFront (CDN, cache + HTTPS)
     → Application Load Balancer (public subnet, nhiều AZ)
     → Auto Scaling Group EC2 / ECS Service (private subnet, nhiều AZ)
     → RDS Multi-AZ (private subnet) + ElastiCache (cache)
     → S3 (static assets / backups)
```

Vai trò từng tầng và từ khóa gắn với nó:

- **Route 53:** DNS, routing policies (Latency-based, Failover, Weighted...).
- **CloudFront:** cache nội dung tĩnh ở edge, giảm latency + giảm tải origin, hỗ trợ HTTPS/WAF.
- **ALB:** cân bằng tải tầng application (HTTP/HTTPS), path/host-based routing, target group + health check. Đặt ở **public subnet**.
- **ASG EC2 / ECS Service:** tầng ứng dụng ở **private subnet**, tự scale theo tải, trải nhiều AZ.
- **RDS Multi-AZ:** database quan hệ với standby ở AZ khác, **failover tự động** (đây là HA, không phải tăng khả năng đọc — muốn scale read thì Read Replica).
- **ElastiCache (Redis/Memcached):** cache dữ liệu đọc nhiều để **giảm tải database** và giảm latency. Thấy "read-heavy, giảm tải RDS" → ElastiCache hoặc DAX (cho DynamoDB).

### 4. Kiến trúc mẫu 2 — Serverless

```
User → Route 53 → CloudFront → API Gateway → Lambda → DynamoDB
                                    ↘ S3 (static hosting / file storage)
```

- **API Gateway:** cửa ngõ API — xác thực (Cognito/API key/IAM), throttling, request validation.
- **Lambda:** xử lý logic theo request/event, tự scale, trả tiền theo lần chạy — least operational overhead.
- **DynamoDB:** NoSQL serverless, scale gần như không giới hạn, on-demand capacity cho workload khó đoán.
- Bản serverless thắng ở: **operational overhead thấp nhất, chi phí theo mức dùng thật, scale tự động**. Đánh đổi: giới hạn Lambda (15 phút), cold start, ít kiểm soát hạ tầng hơn EC2.

Khi scenario nói team nhỏ, traffic khó đoán, muốn tối thiểu vận hành → nghiêng về bản serverless. Khi scenario nói workload ổn định lớn, phần mềm legacy, yêu cầu kiểm soát OS → nghiêng về bản 3-tier EC2/ECS.

### 5. Playbook ra quyết định theo keyword — bảng vàng ngày thi

Đọc câu hỏi, bắt keyword, đối chiếu bảng này trước khi đọc kỹ 4 đáp án:

| Keyword trong đề | Hướng đáp án ưu tiên |
|---|---|
| **"least operational overhead"** | Managed / serverless: Fargate, Lambda, RDS (thay vì tự cài DB trên EC2), DynamoDB, App Runner |
| **"most cost-effective"** | Spot (workload chịu gián đoạn), Savings Plans (ổn định), S3 Lifecycle / Intelligent-Tiering, gp3, Gateway Endpoint, rightsize |
| **"highest availability" / "fault tolerant"** | Multi-AZ tối thiểu; yêu cầu cao hơn → Multi-Region, ASG nhiều AZ, ALB, Route 53 Failover |
| **"secure" / "least privilege"** | IAM Policy/Role theo least privilege, KMS encryption at rest, TLS in transit, private subnets, Secrets Manager (không hardcode credentials), Security Group hạn chế nhất |
| "scalable / spikes / unpredictable traffic" | ASG, Lambda, DynamoDB on-demand, SQS để đệm tải |
| "decouple / loose coupling" | SQS (queue), SNS (pub/sub), EventBridge |
| "real-time / streaming" | Kinesis Data Streams / MSK |
| "reduce latency globally" | CloudFront, Global Accelerator, Route 53 Latency-based routing |
| "hybrid / on-premises connection" | VPN (nhanh, rẻ) vs Direct Connect (ổn định, riêng, lâu triển khai) |

**Nguyên tắc dùng playbook:** keyword cho bạn *hướng*, nhưng phải kiểm tra lại điều kiện phụ trong scenario (ví dụ: "cost-effective" nhưng workload "cannot be interrupted" thì loại Spot ngay).

## Ví dụ đời thường

Vào phòng thi giống như vào bếp thi nấu ăn với đồng hồ đếm ngược:

- **Hai bản kiến trúc mẫu** là hai "thực đơn tủ" bạn đã nấu thuộc lòng — khách (scenario) gọi món biến tấu nào, bạn cũng bắt đầu từ khung có sẵn thay vì nghĩ từ số 0.
- **Playbook keyword** giống nhìn phiếu order: chữ "không cay" (least privilege — hạn chế tối đa), "tiết kiệm nhất" (cost-effective), "nhanh nhất" (highest availability/latency) quyết định cách nêm nếm trước khi bạn đọc hết ghi chú dài của khách.
- **Chiến thuật 2 phút/câu** giống chia thời gian cho từng món: món nào khó (câu dài, lắt léo) thì đánh dấu, làm món dễ trước, cuối giờ quay lại — không đầu bếp nào đứng chết 15 phút ở một món trong khi 10 phiếu order khác đang chờ.

## Phân biệt dễ nhầm

- **Managed vs Serverless:** RDS là managed (AWS lo patching/backup) nhưng không gọi là serverless theo nghĩa trả tiền theo mức dùng như Aurora Serverless/DynamoDB. Đề hỏi "least operational overhead" thì cả hai nhóm đều là ứng viên; đề hỏi đúng chữ "serverless" hãy ưu tiên Lambda/Fargate/DynamoDB/Aurora Serverless.
- **Multi-AZ vs Multi-Region:** Multi-AZ = khả dụng cao trong 1 Region, là lựa chọn mặc định cho "high availability". Multi-Region chỉ khi đề yêu cầu DR cấp Region hoặc RTO gần 0 / latency toàn cầu. Đừng vung Multi-Region cho mọi câu "availability".
- **Caching ở đâu:** Nội dung tĩnh/dùng chung toàn cầu → CloudFront. Dữ liệu query lặp lại từ database → ElastiCache. Bảng DynamoDB cần cache microsecond → DAX. Amazon CloudFront, ElastiCache và DAX không thay thế nhau.
- **SQS vs SNS:** Cần **hàng đợi để đệm và xử lý lần lượt** (decouple + buffer) → SQS. Cần **phát một sự kiện tới nhiều nơi cùng lúc** (fan-out/pub-sub) → SNS. Fan-out chuẩn: SNS → nhiều SQS queue.
- **Security Group vs NACL:** Security Group là stateful, ở tầng instance/ENI — đáp án mặc định cho kiểm soát truy cập. NACL là stateless, ở tầng subnet, dùng khi đề nhấn mạnh deny rule hoặc tầng subnet.

## Bẫy đề thi

- **Bẫy đáp án "mạnh nhất":** Nhiều đáp án sai được viết rất hoành tráng (Multi-Region Active-Active, instance lớn nhất) nhưng vượt yêu cầu và đội chi phí. Đề SAA chấm đáp án **đủ yêu cầu + tối ưu theo tiêu chí được hỏi**, không chấm độ hoành tráng.
- **Bẫy tự quản thay vì managed:** Đáp án "tự cài database trên EC2", "tự viết script backup" thường sai khi đã có dịch vụ managed tương ứng (RDS, AWS Backup) — trừ khi scenario có yêu cầu đặc biệt ép phải tự quản.
- **Bẫy đọc scenario trước, câu hỏi sau:** Đọc hết đoạn scenario dài rồi mới biết đề hỏi gì khiến bạn phải đọc lại — mất gấp đôi thời gian. Luôn đọc **câu hỏi (thường là câu cuối) trước**, gạch keyword, rồi mới đọc scenario để săn chi tiết liên quan.
- **Bẫy 15 câu không tính điểm:** Không có cách nào nhận biết chúng, và chúng trông y như câu thật. Đừng cố đoán, đừng hoảng nếu gặp vài câu lạ — cứ làm hết sức bình đẳng cả 65 câu.
- **Bẫy đổi đáp án khi review:** Khi quay lại câu đã flag, chỉ đổi đáp án khi tìm thấy **lý do cụ thể** trong scenario mà lần đầu đọc sót. Đổi vì "cảm giác" ở phút cuối thường làm mất điểm.

## Tóm tắt 5 dòng

- Đề SAA-C03: 65 câu (50 tính điểm + 15 không tính điểm, không phân biệt được), 130 phút, đạt 720/1000, $150, thi bằng tiếng Anh.
- Trọng số domain: Secure 30% > Resilient 26% > High-Performing 24% > Cost-Optimized 20% — ánh xạ lần lượt tới Security, Reliability, Performance Efficiency, Cost Optimization pillars.
- Thuộc 2 khung kiến trúc: 3-tier (Route 53 → CloudFront → ALB → ASG/ECS → RDS Multi-AZ + ElastiCache) và serverless (CloudFront → API Gateway → Lambda → DynamoDB).
- Playbook keyword: least operational overhead → managed/serverless; most cost-effective → Spot/SP/Lifecycle; highest availability → Multi-AZ/Multi-Region; secure → least privilege + KMS + private subnet.
- Chiến thuật: ~2 phút/câu, đọc câu hỏi trước, loại 2 đáp án sai trước, flag-and-return với câu khó, không bỏ trống câu nào.

## Phụ lục — Chiến thuật làm bài & Checklist cuối

### Chiến thuật trong phòng thi (130 phút / 65 câu ≈ 2 phút/câu)

1. **Đọc câu hỏi trước:** Với câu scenario dài, đọc câu cuối (câu hỏi thật) + gạch keyword ("least operational overhead", "most cost-effective"...) trước, sau đó mới đọc scenario để tìm chi tiết quyết định.
2. **Loại 2 đáp án sai trước:** Hầu hết câu hỏi có 2 đáp án sai rõ ràng (sai dịch vụ, sai phạm vi AZ/Region, vi phạm điều kiện phụ). Loại xong, bạn chỉ còn cân 50/50 giữa 2 đáp án đúng hướng — lúc này mới đọc lại scenario tìm chi tiết phân thắng bại.
3. **Flag-and-return:** Câu nào quá 2 phút chưa ra → chọn tạm đáp án tốt nhất, **flag** lại, đi tiếp. Quay lại xử lý khi đã xong lượt một. Không bao giờ để trống — đề không trừ điểm câu sai.
4. **Quản lý nhịp:** Mục tiêu tham chiếu: câu 20 quanh phút 40, câu 40 quanh phút 80, kết thúc lượt một còn ít nhất 10–15 phút để review các câu đã flag.
5. **Chỉ đổi đáp án khi có lý do cụ thể** tìm thấy trong scenario, không đổi theo cảm giác.

### Checklist tuần cuối

- [ ] Ôn theo domain yếu nhất trước (dựa trên điểm các đề practice gần nhất), không ôn dàn đều.
- [ ] Làm ít nhất 2 đề practice full 65 câu bấm giờ 130 phút, review **cả câu đúng lẫn câu sai** — đọc giải thích vì sao đáp án kia sai.
- [ ] Học thuộc: bảng ánh xạ domain ↔ pillar, playbook keyword ở trên, bảng 4 chiến lược DR (Bài 18), bảng 5 công cụ chi phí (Bài 19).
- [ ] Rà lại các cặp phân biệt dễ nhầm của cả khóa: RPO/RTO, Multi-AZ/Read Replica, SQS/SNS, Gateway/Interface Endpoint, Compute SP/EC2 Instance SP.
- [ ] Hai ngày cuối: giảm cường độ, chỉ đọc tóm tắt 5 dòng của mỗi bài + lướt lại các câu quiz đã sai.
- [ ] Đêm trước ngày thi: ngủ đủ giấc — điểm số mất vì mệt mỏi lớn hơn điểm kiếm thêm được từ một đêm cày cuốc.

### Checklist ngày thi

- [ ] Mang giấy tờ tùy thân đúng quy định của trung tâm thi / chuẩn bị phòng yên tĩnh nếu thi online (OnVUE).
- [ ] Đến sớm (hoặc đăng nhập sớm) 30 phút để làm thủ tục check-in.
- [ ] Nhớ: đề **bằng tiếng Anh hoàn toàn, không có bản tiếng Việt** — giữ nhịp đọc keyword, đừng dịch từng chữ.
- [ ] Trong phòng thi: hít thở, làm theo nhịp 2 phút/câu, flag câu khó, không hoảng vì 15 câu thử nghiệm không tính điểm lẫn trong đề.
- [ ] Kết quả hiển thị ngay sau khi nộp bài (đạt/không đạt); báo cáo điểm chi tiết theo domain gửi sau — dùng nó để biết domain nào cần bổ sung nếu phải thi lại.

## Quiz

**Question 1.** A company runs a web application on EC2 instances behind an Application Load Balancer, with an Amazon RDS MySQL database. Read traffic is growing rapidly and database CPU is consistently high because the same product catalog queries are executed repeatedly. Which solution will MOST effectively reduce the load on the database with the least change to the architecture?

A. Migrate the database to Amazon DynamoDB.
B. Add an Amazon ElastiCache cluster in front of the RDS database to cache frequent query results.
C. Convert the RDS instance to a larger instance class.
D. Enable Multi-AZ on the RDS database to share read traffic with the standby.

**Question 2.** A solutions architect must design a solution for a new API with unpredictable traffic. The company wants the least operational overhead, does not want to manage servers, and wants to pay only for the requests processed. Which architecture best meets these requirements?

A. Amazon EC2 instances in an Auto Scaling group behind an Application Load Balancer, with a self-managed MySQL database on EC2.
B. Amazon CloudFront, Amazon API Gateway, AWS Lambda, and Amazon DynamoDB on-demand.
C. Amazon ECS with the EC2 launch type and Amazon RDS Multi-AZ.
D. A single large EC2 instance running the API and the database together.

**Question 3.** A company's application is deployed in a single Availability Zone and experiences outages whenever that Availability Zone has an issue. The company requires the highest availability for its relational database within the same AWS Region, with automatic failover. Which solution meets these requirements?

A. Take hourly RDS snapshots and copy them to another Region.
B. Deploy the RDS database with Multi-AZ and run the application tier across multiple Availability Zones.
C. Create RDS Read Replicas in other Regions.
D. Store the database on an EBS volume with snapshots in Amazon S3.

**Question 4.** A company needs to store application secrets such as database passwords, rotate them automatically on a schedule, and ensure application code never contains hardcoded credentials. Which solution is MOST appropriate and secure?

A. Store the passwords in an encrypted Amazon S3 bucket and embed the bucket name in the code.
B. Store the passwords in AWS Secrets Manager with automatic rotation, and grant the application an IAM role with least-privilege access.
C. Store the passwords in environment variables in the EC2 user data script.
D. Store the passwords in a private Git repository accessible to the application.

**Question 5.** A batch workload runs on EC2 instances every night. The workload is fault-tolerant, can be interrupted, and can resume from checkpoints. The company wants the MOST cost-effective compute option for this workload. Which option should the solutions architect choose?

A. On-Demand Instances
B. Dedicated Instances
C. Spot Instances
D. EC2 Instance Savings Plans

## Đáp án quiz

**Câu 1 — Đáp án B.** Pattern kinh điển: query lặp lại + database quá tải vì read → thêm **cache ElastiCache** phía trước RDS. C (tăng instance) chỉ xử lý triệu chứng, tốn kém và không giảm số query trùng lặp. D sai kiến thức cốt lõi: RDS Multi-AZ standby **không nhận read traffic** — Multi-AZ là cho failover/HA. A thay đổi kiến trúc quá lớn, không phải "least change".

**Câu 2 — Đáp án B.** Ba keyword cùng chỉ về serverless: "unpredictable traffic" + "least operational overhead" + "pay only for requests" → API Gateway + Lambda + DynamoDB on-demand, CloudFront ở phía trước. A và C đều phải quản lý EC2/cluster. D là kiến trúc tệ nhất: một instance duy nhất chứa cả API lẫn database, không scale, không HA.

**Câu 3 — Đáp án B.** Yêu cầu là **highest availability trong cùng Region + automatic failover** cho RDS → **Multi-AZ** là đáp án chuẩn, đồng thời tầng ứng dụng cũng phải trải nhiều AZ. A là cơ chế DR thủ công, phục hồi chậm, không tự động. C sai vì Read Replica phục vụ scale read và có thể promote thủ công, không phải cơ chế failover tự động trong Region như Multi-AZ. D không phải giải pháp HA cho database.

**Câu 4 — Đáp án B.** Secrets Manager sinh ra đúng cho bài toán này: lưu secret tập trung, **tự động rotate**, tích hợp IAM để cấp quyền theo **least privilege** qua IAM Role — code không chứa credentials. A, C, D đều để lộ secret qua code/script/repo ở các mức khác nhau và không có rotation tự động chuẩn như Secrets Manager. Đây là mẫu câu thuộc domain Secure 30% — domain nặng nhất đề thi.

**Câu 5 — Đáp án C.** "Fault-tolerant + can be interrupted + resume from checkpoints" + "most cost-effective" là chân dung của **Spot Instances**. Savings Plans (D) dành cho workload ổn định liên tục, không phải batch ngắn mỗi đêm. On-Demand (A) đúng về kỹ thuật nhưng không rẻ bằng Spot. Dedicated Instances (B) là lựa chọn đắt, phục vụ yêu cầu isolation/compliance chứ không phải tối ưu chi phí.
