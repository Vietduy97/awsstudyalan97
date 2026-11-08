# Đáp án & Giải thích — Đề mô phỏng SAA-C03 Bộ 01

> Chỉ mở file này sau khi đã làm xong 65 câu. Mỗi câu gồm đáp án, giải thích ngắn và keyword cần nhớ.

---

**Câu 1 — Đáp án: A**
SCP áp ở root/OU có hiệu lực trên mọi account thành viên và ngay cả admin trong account cũng không vượt qua được SCP, nên đây là cách chặn triệt để với ít công vận hành nhất. B sai vì IAM policy trong từng account có thể bị admin sửa/xóa. C chỉ phát hiện và sửa sau, không ngăn chặn. D phá vỡ mô hình quản trị và không thực tế.
Keyword: SCP deny > IAM policy, SCP applies to member admins

**Câu 2 — Đáp án: B**
Multi-AZ DB instance dùng replication đồng bộ sang standby ở AZ khác và tự động failover, không mất dữ liệu, endpoint giữ nguyên nên app ít phải sửa. A là read replica (bất đồng bộ, phải promote thủ công, có thể mất dữ liệu). C là restore thủ công, RTO cao. D đổi cả engine, không cần thiết.
Keyword: Multi-AZ = HA + synchronous + auto failover

**Câu 3 — Đáp án: B**
Lifecycle chuyển dần Standard → Standard-IA → Glacier Flexible Retrieval đúng với tần suất truy cập giảm dần và yêu cầu lấy lại trong vài giờ, tối ưu chi phí theo thời gian. A giữ Standard mãi nên đắt. C dùng One Zone-IA kém durable và xóa sau 90 ngày sai yêu cầu compliance. D đưa ngay vào Deep Archive khiến 30 ngày đầu truy cập chậm/đắt.
Keyword: S3 Lifecycle, Glacier Flexible Retrieval = hours

**Câu 4 — Đáp án: B**
Read replica dùng replication bất đồng bộ để offload read, chấp nhận lag vài giây, không ảnh hưởng write ở primary — đúng bản chất bài toán reporting. A sai vì standby Multi-AZ không đọc được. C tăng size chỉ tốn tiền và không tách tải triệt để. D storage autoscaling chỉ lo dung lượng, không lo CPU read.
Keyword: Read Replica = scale read, Multi-AZ ≠ read

**Câu 5 — Đáp án: B**
KMS customer managed key cho phép kiểm soát policy, audit qua CloudTrail và bật automatic rotation hằng năm, đáp ứng cả 3 yêu cầu. A SSE-S3 do AWS quản lý key, không kiểm soát/audit chi tiết được. C client-side + key on-prem vận hành nặng và không tích hợp S3 như yêu cầu. D SSE-C phải gửi key mỗi request, không có rotation/audit tập trung của KMS.
Keyword: SSE-KMS, customer managed key, auto rotation

**Câu 6 — Đáp án: A**
Tăng TTL/cache policy đúng cách giúp object phổ biến, ít thay đổi được giữ lâu ở edge, giảm origin request và latency cho user châu Á. B chuyển Region chỉ giúp một khu vực và gây xáo trộn. C Transfer Acceleration tối ưu upload vào S3, không phải cache phân phối nội dung. D thêm bucket + latency routing vẫn phải về origin mỗi lần.
Keyword: CloudFront TTL / cache policy = reduce origin load

**Câu 7 — Đáp án: C**
Failover routing policy sinh ra đúng cho primary/secondary, kết hợp health check để tự động chuyển DNS sang secondary khi primary unhealthy. A simple routing không có cơ chế failover. B weighted 100/0 không tự chuyển khi primary chết. D latency routing chọn nơi gần nhất, không phải cơ chế primary-standby.
Keyword: Route 53 Failover routing + health check

**Câu 8 — Đáp án: C**
Job chịu được gián đoạn và resume được là hồ sơ kinh điển của Spot, giảm giá sâu nhất so với On-Demand. A/B Reserved/Savings Plans phù hợp workload liên tục, cam kết dài, không tối ưu cho job 3 giờ/ngày chịu ngắt. D Dedicated Host đắt nhất, dùng cho licensing/compliance đặc thù.
Keyword: Interruptible = Spot Instances

**Câu 9 — Đáp án: C**
Presigned URL cấp quyền tải đúng 1 object, đúng thời hạn 15 phút, không cần AWS account — least privilege hoàn hảo. A public bucket lộ toàn bộ bucket. B tạo IAM user là cấp quyền thừa và phải quản lý credential. D copy ra website công khai làm mất kiểm soát truy cập.
Keyword: Presigned URL = temporary, object-level access

**Câu 10 — Đáp án: A**
Session dạng key-value, cần latency dưới mili-giây và tự hết hạn sau 30 phút khớp hoàn toàn ElastiCache Redis + TTL. B DAX là cache cho DynamoDB, không phải thay RDS session store kiểu này. C EFS là file system, không phải in-memory cache. D read replica vẫn là database disk-based, latency cao hơn và không có TTL theo key.
Keyword: ElastiCache Redis, TTL, sub-millisecond

**Câu 11 — Đáp án: B**
ASG trải nhiều AZ + ALB + target tracking vừa đảm bảo chết 1 AZ vẫn còn instance ở AZ khác, vừa tự co giãn theo tải với ít vận hành. A dùng 2 Region là quá mức và simple record không kiểm tra health. C single instance là single point of failure. D cố định 1 instance trong 1 AZ không có HA.
Keyword: ASG multi-AZ + ALB = HA

**Câu 12 — Đáp án: B**
Security group là stateful, gắn ở ENI/instance, return traffic tự động được cho phép — đúng định nghĩa cần nhớ. A/C sai vì NACL là stateless, áp ở subnet, không phải instance. D đảo ngược tính chất: security group không phải stateless.
Keyword: SG = stateful, instance level; NACL = stateless, subnet level

**Câu 13 — Đáp án: C**
Intelligent-Tiering tự động chuyển object giữa các tier dựa trên hành vi truy cập thực tế, hợp khi pattern không dự đoán được và tránh phí retrieval bất ngờ. A Deep Archive retrieval chậm nhiều giờ, rủi ro cho 5% còn truy cập. B One Zone-IA kém bền vững và không tự thích ứng. D Standard-IA tính phí retrieval và vẫn phải đoán pattern.
Keyword: Unknown access pattern = S3 Intelligent-Tiering

**Câu 14 — Đáp án: B**
DAX là cache in-memory tương thích DynamoDB, đưa latency xuống microsecond cho read lặp lại nhiều lần — đúng yêu cầu. A Streams phục vụ xử lý thay đổi/event, không cache read. C tăng RCU chỉ tăng throughput, không giảm latency xuống microsecond. D thêm GSI giúp pattern truy cập khác, không giải quyết hot item lặp lại.
Keyword: DAX = microsecond DynamoDB cache

**Câu 15 — Đáp án: B**
IAM role + instance profile cấp credential tạm thời, tự xoay vòng, không lưu long-term key trên máy — best practice chuẩn. A/C/D đều lưu key tĩnh hoặc root credential, rò rỉ là mất toàn quyền và bị cấm trong đề thi lẫn thực tế.
Keyword: EC2 access = IAM role / instance profile, no access keys

**Câu 16 — Đáp án: D**
RPO 24h / RTO 8h là lỏng nhất, nên backup & restore rẻ nhất vẫn đáp ứng: chỉ sao lưu sang DR Region, khi có sự cố mới dựng lại hạ tầng. A multi-site và B warm standby tốn kém vượt nhu cầu. C pilot light cũng đắt hơn vì phải duy trì replication liên tục cho core data.
Keyword: Loosest RPO/RTO + lowest cost = Backup & Restore

**Câu 17 — Đáp án: B**
Workload ổn định, cố định family/Region trong 3 năm thì Standard RI 3 năm all upfront cho mức giảm giá cao nhất. A Compute Savings Plans linh hoạt hơn nhưng discount thấp hơn và chỉ 1 năm. C Convertible đổi được family nhưng discount thấp hơn Standard. D On-Demand không có cam kết nên không giảm sâu.
Keyword: Fixed config + 3yr = Standard RI, max discount

**Câu 18 — Đáp án: A**
Block Public Access là lớp chặn cứng ở cả bucket và account, ghi đè cả policy/ACL cấu hình sai — đúng yêu cầu "không bao giờ public". B Versioning chỉ giúp khôi phục phiên bản. C deny GetObject cho everyone sẽ chặn cả người dùng hợp lệ. D MFA Delete chống xóa nhầm, không chống public access.
Keyword: S3 Block Public Access overrides policy/ACL

**Câu 19 — Đáp án: C**
Cluster placement group đặt các instance gần nhau trong cùng 1 AZ trên cùng hạ tầng mạng để latency thấp nhất, throughput cao nhất cho HPC tightly coupled. A spread dàn ra để chống lỗi phần cứng, latency cao hơn. B partition cho workload phân tán lớn như Hadoop. D khác Region làm latency tệ nhất.
Keyword: HPC tightly coupled = Cluster placement group

**Câu 20 — Đáp án: B**
Muốn sống sót khi mất 1 AZ thì cả ALB và ASG/instance phải trải nhiều AZ ngay từ thiết kế. A chỉ ở 1 AZ thì AZ đó chết là sập. C Classic LB + 1 instance là điểm lỗi đơn. D một EBS volume không thể là nơi chứa dữ liệu dùng chung cho HA đa AZ như vậy (và EBS gắn theo AZ).
Keyword: HA = deploy across multiple AZs

**Câu 21 — Đáp án: B**
Secrets Manager có tính năng automatic rotation tích hợp (qua Lambda), giữ version cũ và xoay vòng không downtime — sinh ra cho database credentials. A Parameter Store SecureString không có rotation tự động tích hợp sẵn cho DB credential như Secrets Manager. C env variable tĩnh, không rotation. D file trên S3 phải tự xây cơ chế rotation.
Keyword: Auto rotation = Secrets Manager

**Câu 22 — Đáp án: B**
Có replication liên tục cho core (data/network/DNS) nhưng compute chưa chạy, khi sự cố mới bật và scale lên — đó là định nghĩa pilot light. A backup & restore không có replication liên tục của core đang sẵn sàng. C warm standby phải có môi trường đầy đủ chức năng chạy sẵn ở mức nhỏ. D active-active phải đang phục vụ traffic thật.
Keyword: Pilot light = core replicated, compute off

**Câu 23 — Đáp án: B**
Yêu cầu giữ đúng thứ tự + exactly-once theo từng customer chính là FIFO queue + MessageGroupId + deduplication. A standard queue là at-least-once, best-effort ordering, sẽ trùng và sai thứ tự. C SNS là pub/sub, không đảm bảo thứ tự/duy nhất kiểu queue. D Kinesis là stream, cơ chế xử lý khác và không phải exactly-once queue theo group như yêu cầu.
Keyword: Order + deduplication = SQS FIFO

**Câu 24 — Đáp án: B**
OAC là cơ chế hiện tại thay OAI: CloudFront ký request tới S3 và bucket policy chỉ cho phép đúng distribution đó, bucket vẫn private, user không bypass được. A public bucket phá yêu cầu private. C dựa trên dải IP CloudFront là không tin cậy/không phải best practice. D website endpoint không dùng được với OAC/private origin đúng cách.
Keyword: CloudFront OAC, bucket private

**Câu 25 — Đáp án: C**
Môi trường DR đầy đủ chức năng nhưng thu nhỏ, chạy liên tục và scale lên nhanh để đạt RTO phút/RPO giây là warm standby. A backup & restore RTO tính bằng giờ. B pilot light chưa có môi trường đầy đủ chạy sẵn. D snapshot ngày một lần cho RPO tới 24h, sai hẳn.
Keyword: Warm standby = scaled-down full environment running

**Câu 26 — Đáp án: C**
Compute Savings Plans áp cho EC2 + Lambda + Fargate, cam kết theo $/giờ, linh hoạt family/size/Region nhất trong nhóm Savings Plans. A Standard RI khóa family/Region hơn. B EC2 Instance Savings Plans chỉ cho EC2 và một family/Region. D Spot không có cam kết ổn định cho baseline.
Keyword: Compute Savings Plans = most flexible, EC2+Lambda+Fargate

**Câu 27 — Đáp án: B**
Envelope encryption: data key mã hóa dữ liệu, KMS key mã hóa data key, chỉ bản encrypted data key được lưu cùng dữ liệu; plaintext data key chỉ tồn tại trong bộ nhớ khi dùng. A sai vì lưu plaintext key sẽ vô hiệu mã hóa. C KMS key không rời HSM để mã hóa từng block. D key vẫn được quản lý trong AWS KMS.
Keyword: Envelope encryption = encrypted data key stored with data

**Câu 28 — Đáp án: C**
EFS là NFS shared file system, mount đồng thời từ nhiều instance/nhiều AZ và tự replicate trong Region. A EBS chủ yếu gắn 1 AZ/instance (Multi-Attach rất giới hạn, cùng AZ). B instance store là tạm, mất khi instance dừng/chết. D S3 là object storage, không phải file system NFS thực thụ.
Keyword: Shared NFS multi-AZ = EFS

**Câu 29 — Đáp án: B**
Automated backups + retention 7 ngày cho phép point-in-time recovery tới bất kỳ giây nào trong 7 ngày và chống mất dữ liệu khi xóa nhầm tốt nhất với ít vận hành. A read replica không phải backup và lỗi xóa sẽ replicate sang. C export tháng một lần không đạt PITR 7 ngày. D Multi-AZ chống lỗi hạ tầng, không chống xóa nhầm và không thay backup.
Keyword: Automated backup + PITR, Multi-AZ ≠ backup

**Câu 30 — Đáp án: B**
SCP gắn ở OU áp cho mọi account trong OU và chặn cả khi IAM policy cho phép — đúng cơ chế "trần quyền" của Organizations. A phải sửa từng policy, dễ sót và bị admin sửa lại. C VPC endpoint policy chỉ kiểm soát traffic qua endpoint, không kiểm soát RunInstances. D budget chỉ cảnh báo chi phí, không chặn hành động.
Keyword: SCP at OU = guardrail for all accounts

**Câu 31 — Đáp án: B**
Intelligent-Tiering tự học pattern từng object, giữ durability đa AZ và không bắt đội phải đoán object nào sẽ được đọc lại, cân bằng tốt nhất cho log khó đoán. A One Zone-IA rẻ hơn nhưng rủi ro mất AZ và không tự thích ứng. C Deep Archive retrieval chậm, không hợp yêu cầu latency tiêu chuẩn. D giữ Standard là đắt không cần thiết.
Keyword: Intelligent-Tiering = unknown pattern + multi-AZ durability

**Câu 32 — Đáp án: B**
Global Accelerator dùng mạng AWS toàn cầu + anycast static IP, cải thiện latency/độ ổn định TCP cho ứng dụng đa châu lục và đáp ứng nhu cầu IP tĩnh cho allowlist. A CloudFront mạnh cho cache nội dung HTTP, không phải giải pháp IP tĩnh anycast cho app tổng quát. C geolocation chỉ chọn endpoint theo vị trí. D Transfer Acceleration chỉ cho upload S3.
Keyword: Global Accelerator = static anycast IP, global performance

**Câu 33 — Đáp án: A**
Health check (hoặc evaluate target health với ALB) là điều kiện để Route 53 ngừng trả về endpoint unhealthy. B weighted chỉ chia tỉ lệ traffic, không tự loại endpoint chết. C geoproximity định tuyến theo khoảng cách. D DNSSEC chống giả mạo DNS, không liên quan health.
Keyword: Route 53 health check = stop returning unhealthy endpoint

**Câu 34 — Đáp án: B**
S3 và DynamoDB là 2 dịch vụ duy nhất hỗ trợ Gateway Endpoint — miễn phí, đi qua route table, không qua internet/NAT. A Interface Endpoint tính phí theo giờ + GB và không cần thiết cho 2 dịch vụ này. C NAT tốn phí và vẫn đi đường vòng. D internet gateway phá yêu cầu private.
Keyword: Gateway Endpoint FREE for S3 + DynamoDB only

**Câu 35 — Đáp án: A**
Graviton (ARM) thường cho price-performance tốt hơn x86 đáng kể, và bài đã nêu app tương thích ARM + đã test thành công nên rủi ro thấp. B Dedicated Host tăng chi phí. C tăng size x86 chỉ tốn thêm tiền. D mua RI 3 năm khi chưa test là khóa chi phí sai hướng.
Keyword: Graviton = better price-performance

**Câu 36 — Đáp án: B**
Instance store NVMe gắn trực tiếp vật lý cho latency thấp nhất và IOPS rất cao, đổi lại dữ liệu mất khi instance chết — đề đã chấp nhận vì có replication ở tầng app. A EFS là network file system, latency cao hơn. C gp3 bền nhưng qua network, không thấp bằng local NVMe. D S3 là object storage, không phải block storage.
Keyword: Lowest latency block = instance store (ephemeral)

**Câu 37 — Đáp án: B**
Object Lock compliance mode khóa object đúng nghĩa WORM: không ai, kể cả root, xóa/ghi đè được trước khi hết retention. A MFA Delete vẫn xóa được nếu có MFA + quyền. C bucket policy có thể bị sửa bởi người có quyền quản trị policy. D Vault Lock là cho Glacier vault, không thay Object Lock cho S3 object retention kiểu này.
Keyword: WORM / immutable = S3 Object Lock compliance mode

**Câu 38 — Đáp án: A, B**
Aurora Global Database cho replication liên Region với lag thường <1 giây, failover có quản lý dưới 1 phút, và secondary cluster có reader endpoint để đọc trong lúc bình thường — khớp cả RPO/RTO lẫn yêu cầu đọc. C restore snapshot cho RTO hàng giờ. D DMS copy ngày một lần cho RPO 24h. E Multi-AZ chỉ trong cùng Region, không phải DR liên Region.
Keyword: Aurora Global Database = cross-Region, <1s lag

**Câu 39 — Đáp án: B**
Compute Optimizer phân tích lịch sử utilization (CloudWatch) và đưa khuyến nghị rightsize cụ thể theo resource. A Trusted Advisor chỉ có một số check cơ bản, không thay Compute Optimizer cho rightsizing chuyên sâu. C billing alarm chỉ báo tiền. D Cost Explorer forecast dự báo chi phí tổng, không khuyến nghị đổi size từng instance.
Keyword: Rightsizing recommendations = Compute Optimizer

**Câu 40 — Đáp án: A**
IAM Access Analyzer có thể generate policy từ hoạt động CloudTrail thực tế và phân tích unused access, giúp thu hẹp quyền đúng least privilege. B Macie tìm dữ liệu nhạy cảm (PII) trong S3. C Trusted Advisor chỉ check bề mặt. D Inspector quét lỗ hổng trên EC2/container/lambda.
Keyword: Access Analyzer = generate least-privilege policy from CloudTrail

**Câu 41 — Đáp án: B**
Clickstream tốc độ cao, cần giữ thứ tự theo partition key, replay trong 24h và nhiều consumer độc lập là đúng thiết kế của Kinesis Data Streams. A SQS không giữ stream để replay cho nhiều consumer như vậy và throughput/ordering khác bản chất. C SNS là push pub/sub, không lưu stream để replay. D EventBridge cho event routing, không phải high-throughput streaming.
Keyword: Streaming + replay + multiple consumers = Kinesis Data Streams

**Câu 42 — Đáp án: A**
S3 Cross-Region Replication tự động replicate object mới (và version) sang bucket ở Region khác, bắt buộc versioning ở cả hai bucket. B Lifecycle chỉ chuyển storage class trong cùng bucket, không đổi Region. C DataSync thủ công tháng một lần không tự động/liên tục. D Batch Copy là tác vụ on-demand, không phải replication liên tục.
Keyword: CRR requires versioning on source + destination

**Câu 43 — Đáp án: B**
ACM cấp và tự động gia hạn chứng chỉ TLS dùng trực tiếp trên ALB/CloudFront, loại bỏ vận hành thủ công. A self-signed không được trình duyệt tin cậy và phải tự quản lý. C S3 không phải nơi quản lý cert cho ALB. D KMS quản lý encryption key, không cấp TLS certificate cho ALB.
Keyword: ACM = free TLS cert + auto renewal for ALB/CloudFront

**Câu 44 — Đáp án: B**
Athena query trực tiếp trên S3 theo kiểu serverless trả tiền theo dữ liệu quét; dùng Parquet + partitioning giảm mạnh dữ liệu quét và chi phí cho query ad hoc chỉ lấy ít cột/dòng. A Redshift phải duy trì cluster và nạp dữ liệu mỗi đêm, đắt cho ad hoc. C EC2/EBS tự vận hành tốn kém. D import 10 TB vào RDS là sai công cụ.
Keyword: Athena + Parquet + partition = pay per scan

**Câu 45 — Đáp án: B**
Redis hỗ trợ sorted set, leaderboard, geospatial, persistence và Multi-AZ failover — Memcached không có các data structure và persistence đó. A Memcached chỉ cache đơn giản, đa luồng, không persistence/failover kiểu này. C DAX chỉ cache cho DynamoDB. D read replica là database quan hệ, không phải in-memory store cho leaderboard.
Keyword: Sorted sets / leaderboard = ElastiCache for Redis

**Câu 46 — Đáp án: B**
ECS service trải nhiều AZ + ALB + Application Auto Scaling trên Fargate cho HA theo AZ và scale không cần quản lý EC2. A 1 AZ / desired 1 là điểm lỗi đơn. C 1 EC2 instance cũng vậy. D Dedicated Host đi ngược mục tiêu không quản lý hạ tầng.
Keyword: Fargate multi-AZ + ALB = serverless HA containers

**Câu 47 — Đáp án: A, B**
WAF lọc ở Layer 7 (SQLi, XSS) khi gắn vào ALB/CloudFront, còn Shield (Standard mặc định / Advanced nâng cao) lo DDoS ở tầng mạng/transport — hai lớp bổ sung nhau. C security group không đọc được HTTP body. D Block Public Access là của S3, không lọc exploit. E health check chỉ kiểm tra sức khỏe endpoint.
Keyword: WAF = L7 exploits, Shield = DDoS

**Câu 48 — Đáp án: C**
Traffic khó đoán, spike thưa và bất ngờ thì on-demand tính theo request, không cần dự báo capacity và không throttling do thiếu RCU/WCU, rẻ hơn việc provision cho peak rồi để idle. A/B provision cho peak gây lãng phí lớn phần lớn thời gian. D đổi sang RDS là thay đổi kiến trúc không cần thiết.
Keyword: Unpredictable spikes = DynamoDB on-demand

**Câu 49 — Đáp án: A**
RDS Proxy pool và tái sử dụng connection, giảm lỗi too many connections và cải thiện failover (giảm thời gian chuyển đổi) mà app gần như không phải sửa nhiều. B ElastiCache là cache dữ liệu, không pool DB connection. C ALB không proxy được giao thức database RDS như Proxy. D Route 53 không quản lý connection.
Keyword: RDS Proxy = connection pooling

**Câu 50 — Đáp án: B**
AWS Backup là dịch vụ tập trung, tạo backup plan/policy áp dụng xuyên account/Region qua Organizations, có báo cáo compliance và không cần agent cho các resource AWS được hỗ trợ. A thủ công từng account không scale. C Lifecycle của S3 không backup được EBS/RDS/DynamoDB. D Run Command tự chế, giòn và tốn vận hành.
Keyword: Centralized backup = AWS Backup + backup policy

**Câu 51 — Đáp án: B**
IAM Identity Center (SSO) liên kết IdP ngoài, cấp permission set tạm thời theo account — nhân viên dùng 1 danh tính công ty cho nhiều account, không tạo IAM user lẻ. A tạo user khắp nơi gây phình quản lý và key tĩnh. C dùng chung tài khoản vi phạm truy vết. D lưu password công ty vào Secrets Manager là sai mục đích và nguy hiểm.
Keyword: SSO multi-account = IAM Identity Center + permission sets

**Câu 52 — Đáp án: B**
Mixed instances policy cho phép đặt baseline On-Demand đảm bảo luôn có capacity, phần vượt baseline dùng Spot giá rẻ và chịu ngắt được — cân bằng cost/độ tin cậy chuẩn đề thi. A toàn Spot rủi ro mất toàn bộ capacity. C Dedicated Host đắt vô ích. D fixed On-Demand không có lợi ích co giãn/Spot.
Keyword: Mixed ASG = On-Demand baseline + Spot above baseline

**Câu 53 — Đáp án: A**
Athena là serverless SQL trực tiếp trên S3, không phải quản lý server hay load dữ liệu trước, hợp nhất cho analyst query ad hoc. B RDS phải nạp dữ liệu và giới hạn scale. C EMR cluster chạy idle 24/7 tốn tiền và vận hành. D tự quản DB trên EC2 là nặng nhất.
Keyword: Serverless SQL on S3 = Athena

**Câu 54 — Đáp án: B**
Blue/green trong Beanstalk tạo môi trường mới, kiểm tra khỏe rồi swap CNAME — downtime tối thiểu và rollback chỉ là swap lại URL. A all-at-once gây downtime và khó rollback. C xóa môi trường cũ trước là mất đường lui. D in-place không health check rủi ro phát hành bản lỗi.
Keyword: Beanstalk blue/green = swap CNAME, fast rollback

**Câu 55 — Đáp án: B**
Interface Endpoint (PrivateLink) tạo ENI có IP private trong subnet cho từng dịch vụ AWS, traffic đi hoàn toàn trong mạng AWS private, không cần IGW/NAT. A/C đưa instance ra internet, phá yêu cầu. D VPC peering sang VPC có internet vẫn là đường ra internet gián tiếp và không phải cách truy cập AWS API private chuẩn.
Keyword: No IGW/NAT + AWS APIs = Interface VPC Endpoint

**Câu 56 — Đáp án: C**
One Zone-IA lưu dữ liệu ở 1 AZ nên rẻ nhất trong nhóm IA, availability 99.5%, chỉ hợp dữ liệu tái tạo được và chấp nhận mất khi AZ hỏng — đề đã nêu rõ 2 điều kiện đó. A Standard đắt và đa AZ không cần thiết. B Standard-IA đa AZ nên đắt hơn One Zone. D Intelligent-Tiering cũng đa AZ và có phí monitoring.
Keyword: Cheapest IA, recreatable = S3 One Zone-IA

**Câu 57 — Đáp án: C**
io2 / io2 Block Express là dòng Provisioned IOPS cao cấp, đạt tới hàng chục nghìn–trăm nghìn IOPS, dung lượng lớn và persistent độc lập với instance. A gp3 mặc định IOPS thấp hơn nhiều và phải tune mới tăng, không phải lựa chọn tốt nhất cho 80k bền vững kiểu này. B/D HDD (st1/sc1) mạnh về throughput/giá, latency và IOPS kém.
Keyword: Highest IOPS EBS = io2

**Câu 58 — Đáp án: B**
Trong cùng Region, cơ chế HA không mất dữ liệu là Multi-AZ với synchronous replication sang standby khác AZ. A read replica là asynchronous nên có thể lag và mất dữ liệu khi failover ép buộc. C snapshot theo giờ cho RPO 1 giờ. D CRR của S3 không liên quan replication của database engine.
Keyword: Synchronous = Multi-AZ, Asynchronous = Read Replica

**Câu 59 — Đáp án: B**
Root là quyền tối cao không giới hạn: phải bật MFA, đặt mật khẩu mạnh, không dùng access key của root và không dùng root cho việc hằng ngày. A tạo admin user dùng chung vẫn là credential chia sẻ nguy hiểm. C/D là việc phụ, không bảo vệ được tài khoản nếu root bị chiếm.
Keyword: Secure root first = MFA + no root access keys

**Câu 60 — Đáp án: B**
Lên lịch tự động stop bằng Instance Scheduler/EventBridge + Lambda/Systems Manager loại bỏ lỗi quên của con người, instance stopped chỉ tốn tiền EBS nên giảm chi phí rõ rệt cho môi trường test. A phụ thuộc trí nhớ, đã chứng minh không hiệu quả. C RI 3 năm khóa tiền cho máy chạy không liên tục. D tăng size không giải quyết idle quên tắt.
Keyword: Auto stop schedule = stop non-prod when idle

**Câu 61 — Đáp án: A, B**
Least privilege (chỉ cấp đúng action/resource qua group/role) và MFA cho human console access là 2 best practice cốt lõi. C chia sẻ access key phá truy vết và rotation. D dùng root hằng ngày bị cấm theo best practice. E cấp AdministratorAccess cho mọi người là trái ngược least privilege.
Keyword: Least privilege + MFA for humans

**Câu 62 — Đáp án: A, B**
HA trong 1 Region = loại bỏ điểm lỗi đơn theo AZ: LB + app trải ≥2 AZ và RDS Multi-AZ synchronous standby ở AZ khác. C một EBS volume ở 1 AZ là single point of failure (EBS gắn theo AZ). D dồn hết vào 1 AZ thì mất AZ là sập. E một NAT gateway duy nhất cũng không phải thiết kế HA đầy đủ, dù NAT không nằm trong 2 đáp án đúng yêu cầu.
Keyword: HA = multi-AZ for compute + Multi-AZ for DB

**Câu 63 — Đáp án: A, B**
CloudFront đưa nội dung tĩnh lại gần user toàn cầu và giảm tải origin, còn read replica tách tải đọc khỏi primary RDS — cả hai trực tiếp cải thiện read performance. C dồn read qua 1 instance nhỏ tạo nút thắt. D tắt cache làm mọi request về origin, chậm hơn. E dồn thêm reporting lên primary làm primary quá tải hơn.
Keyword: Global read perf = CloudFront + Read Replica

**Câu 64 — Đáp án: A, B**
Lifecycle chuyển object cũ sang class rẻ hơn và mua Savings Plans/RI cho baseline ổn định (sau khi phân tích Cost Explorer) là 2 cách giảm tiền kinh điển, ít rủi ro. C xóa backup phá khả năng khôi phục. D chạy DB production duy nhất trên Spot có thể bị thu hồi bất cứ lúc nào. E giữ volume/IP thừa là tiếp tục lãng phí.
Keyword: Cost = lifecycle + commitment for steady baseline

**Câu 65 — Đáp án: A, B**
SSE-KMS với customer managed key + key policy kiểm soát được ai dùng key để mã hóa dữ liệu at rest, và ép TLS qua aws:SecureTransport + bucket policy least privilege bảo vệ dữ liệu in transit/access. C public bucket phá mọi kiểm soát. D tắt Block Public Access làm tăng rủi ro lộ dữ liệu. E để access key trong repo công khai là rò rỉ credential.
Keyword: S3 protection = SSE-KMS + enforce TLS + least privilege
