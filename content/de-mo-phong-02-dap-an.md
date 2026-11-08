# Đáp án Đề mô phỏng SAA-C03 — Bộ 02

Chỉ mở file này sau khi đã làm xong 65 câu trong thời gian 130 phút. Mỗi câu gồm đáp án, giải thích ngắn và keyword để tra cứu khi ôn lại.

**Câu 1 — Đáp án: B**
DAX là cache in-memory được thiết kế riêng cho DynamoDB, cho độ trễ microsecond với các API tương thích DynamoDB. Tăng RCU không tạo cache; ElastiCache phải tự quản lý logic cache và không tích hợp trực tiếp; Streams/OpenSearch không phải cache đọc cho DynamoDB.
Keyword: DynamoDB DAX microsecond cache

**Câu 2 — Đáp án: B**
Reserved concurrency đặt giới hạn tối đa số execution environment chạy đồng thời cho đúng function đó, bảo vệ downstream và không ảnh hưởng function khác. Provisioned concurrency chỉ giữ môi trường khởi tạo sẵn để giảm cold start, không phải cơ chế chặn trên; tăng memory hay VPC/NAT không giới hạn concurrency.
Keyword: Lambda reserved concurrency

**Câu 3 — Đáp án: A**
SQS FIFO đảm bảo ordering trong mỗi message group và deduplication giúp xử lý exactly-once trong cửa sổ deduplication. Standard queue chỉ best-effort ordering và at-least-once nên gây trùng; SNS standard và DLQ không tự tạo ordering/exactly-once.
Keyword: SQS FIFO ordering deduplication exactly-once

**Câu 4 — Đáp án: B**
Aurora Global Database replicate sang Region phụ với độ trễ thường khoảng 1 giây và hỗ trợ failover nhanh ở mức dưới 1 phút, ít vận hành nhất cho RPO/RTO này. Snapshot/Backup theo giờ hoặc theo ngày có RPO quá lớn; read replica cross-Region phải promote thủ công và chậm hơn.
Keyword: Aurora Global Database RPO 1s RTO

**Câu 5 — Đáp án: B**
Redis hỗ trợ sorted sets để xếp hạng leaderboard, pub/sub và persistence — đúng các tính năng nâng cao đề bài yêu cầu. Memcached đơn giản, đa luồng nhưng không có sorted sets/pub-sub/persistence; DAX chỉ là cache cho DynamoDB.
Keyword: ElastiCache Redis sorted sets pub/sub

**Câu 6 — Đáp án: A**
Video là object tải lên một lần, đọc nhiều lần, không cần mount file system — S3 Standard cho durability rất cao và chi phí hợp lý nhất. EBS chỉ gắn với EC2 và không chia sẻ toàn cầu; EFS đắt hơn và thừa tính năng POSIX; instance store mất dữ liệu khi instance dừng.
Keyword: S3 object storage vs EBS vs EFS

**Câu 7 — Đáp án: A**
Secrets Manager có automatic rotation bằng Lambda theo lịch (ví dụ 30 ngày) và ứng dụng luôn lấy secret hiện hành qua API. Parameter Store dạng plain text không an toàn và không tự xoay mật khẩu DB; EBS/S3 versioning không phải cơ chế rotation cho credential.
Keyword: Secrets Manager automatic rotation

**Câu 8 — Đáp án: C**
WAF gắn với ALB và dùng AWS Managed Rules để chặn các exploit phổ biến như SQL injection/XSS, rule được AWS duy trì cập nhật. Shield tập trung vào DDoS; security group chỉ lọc IP/port; GuardDuty/Inspector là dịch vụ phát hiện, không chặn request ở ALB.
Keyword: WAF AWS Managed Rules ALB

**Câu 9 — Đáp án: C**
Gateway VPC endpoint cho S3 và DynamoDB miễn phí, đưa traffic ra khỏi NAT gateway nên cắt chi phí xử lý NAT cho phần traffic chiếm đa số này. NAT instance kém tin cậy/hiệu năng hơn; chuyển sang public subnet làm mất tính riêng tư; flow logs không giảm phí.
Keyword: Gateway VPC Endpoint S3 DynamoDB NAT cost

**Câu 10 — Đáp án: D**
Workload ổn định chạy liên tục 3 năm nên dùng cam kết dài hạn như Savings Plans/Reserved Instances để giảm giá; workload batch chịu gián đoạn được thì Spot rẻ nhất. Spot cho database production không được gián đoạn là sai hoàn toàn; On-Demand cho cả hai không tối ưu chi phí.
Keyword: Savings Plans Reserved vs Spot

**Câu 11 — Đáp án: A**
EventBridge dùng event bus và rules khớp event pattern theo nội dung (số tiền, Region...) để route mà producer không cần biết consumer. SQS là queue point-to-point, Kinesis là stream theo shard, Step Functions là orchestration workflow — đều không phải content-based event routing.
Keyword: EventBridge event pattern routing

**Câu 12 — Đáp án: B, D**
Fanout chuẩn: publish một lần lên SNS topic (D), mỗi service đăng ký một SQS queue riêng (B) để buffer và xử lý độc lập theo tốc độ riêng, không mất event khi service tạm dừng. Một queue chung khiến các service tranh nhau message; gọi Lambda tuần tự tạo coupling; scan DynamoDB không phải messaging.
Keyword: SNS SQS fanout decoupling

**Câu 13 — Đáp án: B**
ECS với Fargate chạy container mà không cần provision/quản lý server hay cluster node — least operational overhead, vẫn gắn ALB được. EC2 tự quản lý và EKS self-managed nodes tốn vận hành hơn; Elastic Beanstalk vẫn phải quản capacity nhiều hơn Fargate.
Keyword: ECS Fargate serverless containers

**Câu 14 — Đáp án: C**
Step Functions là orchestrator có state, retry/backoff, parallel branches và lịch sử thực thi trực quan, kiểm toán được — đúng bản chất workflow nhiều bước dài ngày. SQS chỉ là queue, EventBridge rules không quản state workflow, Lambda gọi nhau trực tiếp khó theo dõi và dễ lỗi dây chuyền.
Keyword: Step Functions orchestration retry

**Câu 15 — Đáp án: D**
Kinesis Data Streams phục vụ ingest tốc độ cao, nhiều consumer đọc độc lập theo position riêng và replay được trong thời gian retention (kéo dài tới 365 ngày). Firehose là delivery gần real-time vào đích, không cho nhiều consumer đọc/replay tùy ý; SQS và MSK một partition không đáp ứng throughput/mô hình này.
Keyword: Kinesis Data Streams replay multiple consumers

**Câu 16 — Đáp án: A**
Athena truy vấn SQL serverless trực tiếp trên S3, còn Glue Data Catalog lưu metadata bảng dùng chung cho Athena/EMR/Redshift Spectrum. Các cặp còn lại hoặc phải provision cluster, hoặc dùng sai dịch vụ làm catalog.
Keyword: Athena Glue Data Catalog serverless SQL

**Câu 17 — Đáp án: C**
On-demand tự trả theo request, không cần dự báo hay quản lý capacity, phù hợp traffic khó đoán với đỉnh đột ngột xen thời gian rỗng. Provisioned (dù có Auto Scaling) vẫn phải đặt mức nền và phản ứng chậm hơn với spike lớn; reserved capacity không dành cho mô hình này.
Keyword: DynamoDB on-demand vs provisioned

**Câu 18 — Đáp án: B**
Lambda giới hạn thời gian chạy tối đa 15 phút nên job 45 phút không thể ở lại Lambda; chuyển sang container trên Fargate chạy task dài hạn là hướng chuẩn. Tăng memory chỉ tăng CPU/mạng chứ không nâng timeout; chia nhỏ bằng SQS phức tạp và không cần thiết khi workload đã đóng gói container.
Keyword: Lambda 15 minute limit Fargate long-running

**Câu 19 — Đáp án: B**
Visibility timeout phải dài hơn thời gian xử lý để message không xuất hiện lại cho worker khác giữa chừng; DLQ với maxReceiveCount cách ly message lỗi lặp lại để điều tra. Rút ngắn timeout làm trùng lặp nặng hơn; xóa message trước khi xử lý gây mất dữ liệu.
Keyword: SQS visibility timeout DLQ maxReceiveCount

**Câu 20 — Đáp án: C**
Aurora Serverless v2 tự scale capacity theo ACU trong khoảng min–max đã cấu hình, phù hợp usage biến động mạnh và không phải quản lý instance. RDS storage Auto Scaling chỉ mở rộng storage, không scale compute; Aurora Provisioned instance nhỏ nhất vẫn chạy (và tính phí) 24/7.
Keyword: Aurora Serverless v2 ACU scaling

**Câu 21 — Đáp án: A**
Lazy loading (cache-aside) chỉ nạp dữ liệu vào cache khi có request thực tế và miss — đơn giản nhất, chịu được dữ liệu hơi cũ trong vài phút như đề bài. Write-through ghi đồng thời cache+DB mỗi lần write (mạnh về tươi nhưng phức tạp hơn); write-behind ghi cache trước, DB sau; refresh-ahead không phải lựa chọn đơn giản nhất ở đây.
Keyword: ElastiCache lazy loading cache-aside vs write-through

**Câu 22 — Đáp án: C**
Lifecycle chuyển dần Standard → Standard-IA sau 30 ngày → Glacier Flexible Retrieval sau 120 ngày rồi expire sau 7 năm khớp đúng tần suất truy cập giảm dần và yêu cầu lấy lại trong vài giờ. Giữ Standard 7 năm tốn nhất; One Zone-IA kém durable hơn cho compliance và xóa sau 120 ngày vi phạm retention 7 năm.
Keyword: S3 Lifecycle Standard-IA Glacier Flexible Retrieval

**Câu 23 — Đáp án: D**
Global Tables cho phép đọc/ghi chủ động ở nhiều Region (multi-Region active-active) với replication tự động và độ trễ thấp tại Region local. Streams + Lambda là giải pháp tự chế một chiều, tốn vận hành; PITR và export to S3 chỉ phục vụ backup/export, không phải active-active.
Keyword: DynamoDB Global Tables active-active

**Câu 24 — Đáp án: A**
DynamoDB Streams ghi lại mọi thay đổi insert/update theo thứ tự và Lambda là consumer event-driven chuẩn, không cần polling. DAX là cache đọc, không phát sự kiện thay đổi; EventBridge scan định kỳ là polling trá hình; bắt producer gửi trùng vào SQS tạo coupling và dễ sót.
Keyword: DynamoDB Streams Lambda trigger

**Câu 25 — Đáp án: B**
Bật caching ở stage của API Gateway với TTL phù hợp sẽ trả response đã cache cho request lặp lại, giảm lần gọi Lambda và giảm độ trễ. Request validation chỉ kiểm tra input; usage plan để giới hạn quota/throttle; WebSocket API phục vụ giao tiếp hai chiều, không phải caching.
Keyword: API Gateway caching TTL

**Câu 26 — Đáp án: D**
Điều kiện dynamodb:LeadingKeys trong IAM policy giới hạn user chỉ truy cập item có partition key bằng định danh của chính họ — row-level access control thực thi ở tầng IAM. Mỗi user một bảng không scale; encryption và Streams không kiểm soát ai được đọc item nào.
Keyword: DynamoDB LeadingKeys fine-grained access

**Câu 27 — Đáp án: B**
SSE-KMS với customer managed key cho phép kiểm soát key policy, audit mọi lần dùng key qua CloudTrail và disable key để chặn truy cập ngay. SSE-S3 dùng key do S3 quản lý nên không kiểm soát/audit ở mức key của mình; versioning/MFA Delete và nén không phải mã hóa do mình kiểm soát.
Keyword: SSE-KMS customer managed key

**Câu 28 — Đáp án: D**
S3 và DynamoDB hỗ trợ gateway endpoint — miễn phí, traffic đi trong mạng AWS qua route table, không cần NAT/internet. Interface endpoint (PrivateLink) tính phí theo giờ/GB và không cần thiết cho hai dịch vụ này; NAT gateway tốn phí và kém riêng tư hơn cho use case này.
Keyword: Gateway endpoint free S3 DynamoDB

**Câu 29 — Đáp án: D**
Shield Advanced bổ sung đội DDoS Response Team 24/7, cost protection và chẩn đoán nâng cao cho các cuộc tấn công phức tạp — Shield Standard (miễn phí, mặc định) không có các quyền lợi này. WAF chặn exploit lớp ứng dụng, GuardDuty phát hiện đe dọa, Network Firewall lọc traffic VPC — không thay thế Shield Advanced.
Keyword: Shield Standard vs Shield Advanced DRT

**Câu 30 — Đáp án: B, E**
(B) Secrets Manager có sẵn automatic rotation bằng Lambda — tính năng phân biệt cốt lõi. (E) Parameter Store SecureString cũng lưu secret được mã hóa KMS nhưng không có rotation tự động native. (A) sai vì Secrets Manager luôn mã hóa; (C) sai vì SecureString mã hóa bằng KMS được; (D) sai vì không dịch vụ nào lưu secret trong S3.
Keyword: Secrets Manager rotation vs Parameter Store SecureString

**Câu 31 — Đáp án: A**
ACM cấp chứng chỉ public, tự gia hạn và gắn trực tiếp vào HTTPS listener của ALB; DNS ngoài AWS vẫn validate được qua DNS/EMAIL validation. Self-signed không được trình duyệt tin cậy và không tự gia hạn; Secrets Manager/WAF không phải nơi gắn chứng chỉ cho ALB.
Keyword: ACM certificate ALB HTTPS

**Câu 32 — Đáp án: D**
Block Public Access ghi đè mọi bucket policy/ACL cố tình hay vô ý cấp public, ở cả cấp bucket và account — đúng lớp bảo vệ đề bài yêu cầu. Versioning/Object Lock chống xóa/sửa, logging chỉ ghi nhật ký, WAF không áp dụng cho S3 theo cách này.
Keyword: S3 Block Public Access

**Câu 33 — Đáp án: A**
CloudTrail ghi lại API call và lưu log vào S3; Athena truy vấn SQL serverless trực tiếp trên các file log đó để tìm user/thao tác 60 ngày trước. CloudWatch metrics không chứa danh tính người gọi API; GuardDuty là findings bảo mật; Cost and Usage Reports phục vụ chi phí, không phải audit API.
Keyword: CloudTrail Athena audit query

**Câu 34 — Đáp án: B**
Bật "EBS encryption by default" ở cấp Region khiến mọi volume mới (kể cả tạo từ snapshot) đều được mã hóa mặc định, nhà phát triển không tạo được volume trần. Config rule chỉ phát hiện/xử lý sau; Inspector quét lỗ hổng; MFA cho user không liên quan mã hóa volume.
Keyword: EBS encryption by default

**Câu 35 — Đáp án: B**
Đưa mật khẩu vào Secrets Manager và cấp cho Lambda execution role quyền GetSecretValue là cách chuẩn: lưu trữ tập trung, mã hóa, xoay được, lấy tại runtime. Để mật khẩu trong code/gói deploy, S3 object hay DynamoDB không mã hóa đều giữ nguyên các vi phạm mà bài review đã chỉ ra.
Keyword: Lambda Secrets Manager execution role

**Câu 36 — Đáp án: D**
WAF gắn ALB với Managed Rules nhóm SQL database và Core rule set sẽ chặn SQLi/XSS ở biên trước khi request tới ứng dụng. Network ACL không hiểu nội dung HTTP; signed URL kiểm soát truy cập nội dung CloudFront chứ không lọc payload tấn công; tăng size EC2 không chặn được gì.
Keyword: WAF Managed Rules SQLi XSS

**Câu 37 — Đáp án: A, C**
(A) Inspector tự động đánh giá lỗ hổng phần mềm trên EC2 và container image. (C) GuardDuty phân tích log (CloudTrail, VPC Flow, DNS...) để phát hiện hoạt động độc hại và credential bị xâm phạm. GuardDuty không vá lỗi, Inspector không phải firewall — hai ý (B) và (D) hoán đổi sai vai trò; (E) sai vì IAM vẫn bắt buộc.
Keyword: GuardDuty threat detection Inspector vulnerability

**Câu 38 — Đáp án: B**
ECS task role cấp credential tạm thời đúng phạm vi cho chính các container trong task, do AWS tự cấp và xoay. Instance role dùng chung cho mọi task trên host và dễ thừa quyền; access key của IAM user đóng gói trong image là chống chỉ định; bucket policy mở cho mọi principal phá vỡ least privilege.
Keyword: ECS task role vs instance role

**Câu 39 — Đáp án: D**
Bật SSE trên queue bằng customer managed KMS key và kiểm soát qua key policy + IAM policy mới đáp ứng mã hóa at rest do mình kiểm soát và chỉ role chỉ định mới giải mã được. HTTPS chỉ mã hóa in transit; deduplication/FIFO là tính năng ordering, không phải mã hóa.
Keyword: SQS SSE-KMS key policy

**Câu 40 — Đáp án: B**
IAM database authentication cho phép đăng nhập Aurora bằng token sinh từ thông tin xác thực IAM thay cho mật khẩu tĩnh. Global Database là replication cross-Region, backtrack là tua thời gian trong cluster, auto pause thuộc Serverless v1 — không liên quan xác thực.
Keyword: Aurora IAM database authentication

**Câu 41 — Đáp án: C**
In-transit encryption (TLS) mã hóa dữ liệu trên đường truyền và Redis AUTH yêu cầu token khi kết nối — đúng cặp yêu cầu compliance. AOF/cluster mode là tính năng durability/scale; SASL thuộc Memcached; lazy loading/TTL là chiến lược cache, không phải bảo mật.
Keyword: ElastiCache Redis TLS AUTH encryption

**Câu 42 — Đáp án: C**
Athena workgroups tách nhóm người dùng theo cấu hình riêng: vị trí/kiểu mã hóa của kết quả và giới hạn bytes scanned để kiểm soát chi phí. Crawler chỉ khám phá schema cho Glue Catalog; Object Lock trên bucket kết quả không tạo giới hạn truy vấn theo nhóm.
Keyword: Athena workgroups cost control

**Câu 43 — Đáp án: D**
Mỗi Lambda một execution role riêng với quyền tối thiểu cho đúng việc của nó là least privilege chuẩn. Dùng một role admin chung, nhúng access key vào state machine, hay bỏ IAM roles đều phá vỡ nguyên tắc này.
Keyword: Least privilege Lambda execution role

**Câu 44 — Đáp án: B**
Cấu hình SQS làm event source cho Lambda: message thành công tự bị xóa, message lỗi được nhận lại có giới hạn theo redrive policy rồi chuyển vào DLQ để cách ly. Tự poll bằng lịch và xóa toàn bộ gây mất dữ liệu; tăng memory không xử lý được retry/DLQ; đổi sang SNS làm mất tính buffer của queue.
Keyword: Lambda SQS event source DLQ redrive

**Câu 45 — Đáp án: A**
Aurora Multi-AZ DB cluster deployment có writer và các reader ở nhiều AZ với replication đồng bộ ở tầng storage, failover tự động không mất dữ liệu khi một AZ lỗi. Read replica thường là bất đồng bộ và promote thủ công có thể mất dữ liệu; Global Database dành cho cross-Region; restore snapshot chậm và mất dữ liệu mới.
Keyword: Aurora Multi-AZ cluster failover synchronous

**Câu 46 — Đáp án: C**
EFS Regional là file system POSIX dùng chung, mount đồng thời từ nhiều AZ — đúng yêu cầu shared file system đa AZ. EBS là block storage gắn theo AZ (không chia sẻ đa AZ theo cách này); S3 là object storage không có ngữ nghĩa POSIX; instance store là tạm thời và không dùng chung.
Keyword: EFS shared POSIX multi-AZ

**Câu 47 — Đáp án: A, B**
CRR yêu cầu versioning bật ở cả bucket nguồn và đích (A) và S3 cần quyền replicate thông qua IAM role do S3 assume (B). CRR hoạt động bình thường cùng Block Public Access, bucket đích nằm ở Region khác chứ không phải cùng AZ, và không bắt buộc One Zone-IA.
Keyword: S3 Cross-Region Replication versioning IAM role

**Câu 48 — Đáp án: C**
EventBridge hỗ trợ DLQ cho target để hứng event giao thất bại và tính năng archive/replay để phát lại event đã lưu sau khi target sửa xong. Scheduler/input transformer không xử lý delivery failure; FIFO deduplication và Catch của Step Functions thuộc dịch vụ khác.
Keyword: EventBridge DLQ archive replay

**Câu 49 — Đáp án: C**
ECS service duy trì desired count, thay task unhealthy dựa trên health check của ALB và kết hợp Application Auto Scaling theo CPU để scale — bộ ba chuẩn cho service luôn khỏe và đàn hồi. Task đơn lẻ/scheduled task không có cơ chế duy trì số lượng hay tự thay task lỗi.
Keyword: ECS service desired count Auto Scaling

**Câu 50 — Đáp án: D**
PITR sao lưu liên tục và cho restore về bất kỳ thời điểm nào trong tối đa 35 ngày — đúng kịch bản khôi phục sau xóa/ghi nhầm. Streams chỉ giữ thay đổi 24 giờ và là nguồn sự kiện, không phải backup; on-demand và DAX liên quan capacity/cache.
Keyword: DynamoDB point-in-time recovery 35 days

**Câu 51 — Đáp án: A**
Provisioned concurrency giữ sẵn môi trường đã khởi tạo nên request đến là chạy ngay, loại bỏ cold start cho workload dùng liên tục. Reserved concurrency chỉ đặt hạn mức tối đa/tối thiểu được đảm bảo, không khởi tạo sẵn môi trường; tăng timeout không liên quan độ trễ khởi động.
Keyword: Lambda provisioned concurrency cold start

**Câu 52 — Đáp án: D**
Bật cluster mode với nhiều shard sẽ phân mảnh dữ liệu để vượt giới hạn bộ nhớ/throughput của một node, vẫn giữ cấu trúc dữ liệu Redis trong từng shard. Tắt cluster mode rồi chỉ tăng node thì sớm chạm trần single node; Memcached và DAX không đáp ứng yêu cầu Redis này.
Keyword: ElastiCache Redis cluster mode sharding

**Câu 53 — Đáp án: A**
Hot shard sinh ra do partition key phân bố lệch: cần đa dạng hóa partition key để tải trải đều, đồng thời tăng shard hoặc chuyển sang on-demand mode khi tổng throughput tăng. Mã hóa, retention và Firehose không giải quyết nút cổ chai theo từng shard.
Keyword: Kinesis hot shard partition key

**Câu 54 — Đáp án: C**
io2/io2 Block Express cho IOPS rất cao, ổn định và độ trễ thấp cho database giao dịch; gp3 là SSD đa dụng cân bằng giá/hiệu năng cho workload thông thường. st1/sc1 là HDD cho throughput/cold data, không hợp database cần IOPS; instance store không bền vững cho dữ liệu quan trọng.
Keyword: EBS io2 vs gp3

**Câu 55 — Đáp án: D**
Aurora read replicas chia sẻ cùng storage layer nên lag rất thấp, và reader endpoint tự cân bằng, tự bổ sung replica mới — tách tải đọc khỏi writer đúng yêu cầu. Chạy report trên writer vẫn ảnh hưởng production; export S3 theo giờ dữ liệu cũ và chậm; tăng size writer không tách được tải.
Keyword: Aurora read replica reader endpoint

**Câu 56 — Đáp án: C**
Multipart upload chia file lớn thành các phần tải song song, thử lại từng phần — chuẩn cho file >100 MB; Transfer Acceleration tăng tốc đường dài qua CloudFront edge locations. Tải một request duy nhất dễ lỗi và không resume được; EBS/Glacier không phải kênh upload cho người dùng toàn cầu.
Keyword: S3 multipart upload Transfer Acceleration

**Câu 57 — Đáp án: A, D**
(D) Spot/Fargate Spot cho chi phí thấp nhất cho ECS task. (A) Vì Spot có thể bị thu hồi, ứng dụng bắt buộc phải checkpoint và chịu gián đoạn tốt — đề bài đã nêu rõ hai điều kiện này. Spot cho primary database không replication là chống chỉ định; giữ state chỉ trong bộ nhớ local và cố trả giá cao ở một AZ đều phá vỡ thiết kế chịu lỗi/giá rẻ.
Keyword: Spot Fargate Spot checkpoint fault tolerant

**Câu 58 — Đáp án: B**
Giá Lambda tính theo GB-second: tăng memory tăng CPU nên có thể rút ngắn duration đủ để tổng chi phí giảm, và ngược lại với function nhẹ. Vì vậy phải đo/tinh chỉnh từng function để tìm điểm chi phí thấp nhất. Đặt max hay min cho mọi function đều phung phí ở một đầu; timeout không quyết định chi phí mỗi invocation.
Keyword: Lambda memory tuning GB-second cost

**Câu 59 — Đáp án: C**
Long polling với WaitTimeSeconds > 0 (tối đa 20) khiến ReceiveMessage chờ tới khi có message thay vì trả rỗng ngay, cắt mạnh số lần receive rỗng và chi phí API. Short polling (0) chính là nguyên nhân gây receive rỗng liên tục; FIFO và retention không liên quan.
Keyword: SQS long polling WaitTimeSeconds

**Câu 60 — Đáp án: C**
Một NAT gateway cho cả VPC rẻ hơn nhưng là single point of failure: AZ chứa nó lỗi thì các AZ khác mất đường ra internet, và traffic xuyên AZ còn phát sinh phí cross-AZ. NAT gateway tính phí theo giờ + theo GB xử lý nên số lượng ảnh hưởng trực tiếp chi phí; nó cũng không thể vừa rẻ vừa HA hơn phương án mỗi AZ một cái.
Keyword: NAT Gateway cost vs high availability tradeoff

**Câu 61 — Đáp án: C, D**
Compute Savings Plans cam kết mức dùng theo $/giờ và tự áp dụng linh hoạt qua EC2, Fargate, Lambda, thay đổi được family/size/Region (C, D). Cam kết cứng theo family/Region là của EC2 Instance Savings Plans/Reserved Instances; Savings Plans không giữ capacity theo AZ và không bị thu hồi như Spot.
Keyword: Compute Savings Plans flexibility EC2 Fargate Lambda

**Câu 62 — Đáp án: B**
TTL dùng attribute chứa timestamp hết hạn; DynamoDB tự xóa item đã hết hạn ở background mà không tốn write capacity. Streams + Lambda tự xóa vẫn tốn tài nguyên và phải vận hành; PITR là backup; DAX eviction chỉ là việc của cache, không dọn bảng gốc.
Keyword: DynamoDB TTL free expiry deletion

**Câu 63 — Đáp án: B, E**
Athena tính phí theo lượng data scan: Parquet dạng cột chỉ đọc các cột cần thiết (B) và partition theo cột lọc như date giúp bỏ qua toàn bộ partition không liên quan (E) — hai đòn giảm chi phí kinh điển. Nhiều file CSV nhỏ không partition làm scan toàn bộ; tắt Glue Catalog phá vỡ việc quản lý bảng; Athena không cache vĩnh viễn toàn bộ dataset.
Keyword: Athena Parquet partitioning scan cost

**Câu 64 — Đáp án: A**
EFS lifecycle management tự chuyển file ít truy cập sang lớp Infrequent Access rẻ hơn và tự chuyển về khi được truy cập lại, không cần thao tác thủ công. Sao chép tay sang Glacier rồi xóa khỏi EFS phá vỡ yêu cầu file vẫn sẵn sàng trên file system; Max I/O là chế độ hiệu năng, không giảm chi phí lưu trữ.
Keyword: EFS lifecycle Infrequent Access

**Câu 65 — Đáp án: C**
Glacier Flexible Retrieval cho chi phí lưu trữ rất thấp cho dữ liệu archive hiếm khi truy cập và vẫn lấy lại được trong vài giờ (expedited/standard) — khớp đúng retention 5 năm và yêu cầu audit. Standard/Standard-IA đắt hơn nhiều cho archive dài hạn; Intelligent-Tiering không bật archive tier thì không đạt mức giá archive.
Keyword: S3 Glacier Flexible Retrieval archive hours
