# Đề mô phỏng SAA-C03 — Bộ 03 — Đáp án & Giải thích

**Câu 1 — Đáp án: B**
Kiến trúc 3-tier chuẩn HA: ALB và ASG trải nhiều AZ giúp tầng ứng dụng tự scale và chịu lỗi AZ. RDS Multi-AZ có standby đồng bộ, failover tự động nên không mất dữ liệu khi bảo trì hoặc sự cố AZ. Đặt instance ở private subnet cũng đúng thực hành bảo mật.
Keyword: 3-tier, Multi-AZ, ALB + ASG + RDS Multi-AZ

**Câu 2 — Đáp án: C**
Change set cho phép xem trước resource nào sẽ add/modify/replace trước khi thực thi thay đổi trên stack thật. Đây là cơ chế review và phê duyệt chuẩn cho cập nhật production. Drift detection là để so sánh trạng thái thực tế, không phải xem trước thay đổi template.
Keyword: CloudFormation change set, preview changes

**Câu 3 — Đáp án: C**
Khi đổi engine (Oracle sang PostgreSQL), SCT chịu trách nhiệm chuyển đổi schema, code và object không tương thích. DMS chịu trách nhiệm nạp dữ liệu và ongoing replication/CDC để giảm downtime khi cutover. DataSync và Snowball không chuyển database theo cơ chế này.
Keyword: DMS + SCT, heterogeneous migration, CDC

**Câu 4 — Đáp án: B**
Global Accelerator cấp 2 IP tĩnh dạng anycast và định tuyến traffic qua mạng toàn cầu AWS tới endpoint khỏe gần nhất. Nó hỗ trợ cả TCP và UDP nên phù hợp game thời gian thực. CloudFront là CDN cache nội dung HTTP, không dành cho UDP tùy biến.
Keyword: Global Accelerator, static anycast IP, TCP/UDP

**Câu 5 — Đáp án: B**
Lifecycle chuyển tầng theo tuổi dữ liệu giúp tối ưu chi phí: nóng ở Standard, nguội dần sang Standard-IA, lưu trữ lâu dài sang Glacier Deep Archive rẻ nhất. Log phải giữ 7 năm nên không được xóa sau 90 ngày. Giữ tất cả ở Standard sẽ rất tốn kém.
Keyword: S3 Lifecycle, Standard-IA, Glacier Deep Archive

**Câu 6 — Đáp án: C**
CloudTrail ghi lại mọi API call: ai làm, làm gì, khi nào, từ IP nào — đúng câu hỏi "who did what". CloudWatch là metrics/logs hiệu năng, Config là lịch sử cấu hình resource. Muốn truy vết hành động xóa bucket phải xem CloudTrail.
Keyword: CloudTrail, who did what, API activity

**Câu 7 — Đáp án: A, C**
Interface endpoint dùng PrivateLink giúp traffic tới SQS đi hoàn toàn trong mạng AWS, không qua internet. PrivateLink cũng là cách truy cập dịch vụ SaaS của đối tác được expose qua NLB một cách riêng tư. Các đáp án dùng subnet public/internet gateway đi ngược yêu cầu bảo mật.
Keyword: PrivateLink, interface endpoint, no internet

**Câu 8 — Đáp án: B**
Direct Connect là kết nối riêng, chuyên dụng từ data center tới AWS với băng thông ổn định và latency nhất quán. VPN chạy qua internet nên băng thông và độ trễ biến động. Workload tài chính lâu dài, nhạy cảm cần tính ổn định của Direct Connect.
Keyword: Direct Connect, dedicated private, consistent bandwidth

**Câu 9 — Đáp án: C**
Weighted routing chia traffic theo trọng số cấu hình, ví dụ 10/90, rất phù hợp canary release và tăng dần tỷ lệ. Latency routing dựa trên độ trễ, geolocation dựa trên vị trí, failover chỉ chuyển khi primary lỗi.
Keyword: Route 53 weighted routing, canary

**Câu 10 — Đáp án: B**
Cognito user pool cung cấp sẵn đăng ký, đăng nhập và quản lý người dùng cuối, tích hợp trực tiếp làm authorizer cho API Gateway. IAM auth phù hợp principal AWS nội bộ, không phù hợp hàng nghìn retail user. API key một mình không phải cơ chế xác thực danh tính.
Keyword: API Gateway, Cognito user pool authorizer

**Câu 11 — Đáp án: B**
Transit Gateway là hub trung tâm kết nối hàng loạt VPC và on-premises, route tập trung, mở rộng tốt. VPC peering là kết nối 1-1, không transitive, số lượng bùng nổ theo mô hình mesh. 40 VPC là dấu hiệu kinh điển phải dùng Transit Gateway.
Keyword: Transit Gateway, hub-and-spoke, peering limits

**Câu 12 — Đáp án: C**
Warm standby duy trì một bản sao đầy đủ chức năng nhưng scale nhỏ ở Region DR, sẵn sàng scale up khi failover. Nó nhanh hơn pilot light/backup-restore nhưng rẻ hơn multi-site active-active. RTO tính bằng phút tới giờ tùy mức scale-up.
Keyword: DR warm standby, scaled-down full copy

**Câu 13 — Đáp án: B**
Drift detection so sánh cấu hình thực tế của resource trong stack với cấu hình kỳ vọng trong template. Thay đổi thủ công ngoài CloudFormation sẽ bị phát hiện là drifted. Change set dùng cho thay đổi sắp áp dụng, không phải kiểm tra thay đổi đã xảy ra ngoài quy trình.
Keyword: CloudFormation drift detection

**Câu 14 — Đáp án: A**
DataSync được thiết kế để di chuyển và đồng bộ dữ liệu file/object quy mô lớn một cách tự động, có lịch trình, kiểm tra toàn vẹn và giữ metadata. Nó phù hợp bài toán sync NFS liên tục sang S3. Snowball là vận chuyển offline, không phải đồng bộ theo lịch qua mạng.
Keyword: DataSync, large-scale file sync, NFS to S3

**Câu 15 — Đáp án: B**
Compute Optimizer phân tích lịch sử utilization thực tế (CPU, memory, network...) để đề xuất rightsize EC2/ASG/Lambda. CPU trung bình 8% trong thời gian dài là tín hiệu oversized rõ ràng. Cost Explorer cho chi phí, không đưa khuyến nghị sizing chuyên sâu như Compute Optimizer.
Keyword: Compute Optimizer, rightsizing

**Câu 16 — Đáp án: C**
SQS dùng interface endpoint (PrivateLink) vì SQS không có gateway endpoint như S3/DynamoDB. Interface endpoint tạo ENI với IP private trong subnet, traffic không cần NAT hay internet. Đây là bẫy hay gặp: chọn nhầm gateway endpoint cho SQS.
Keyword: Interface endpoint, SQS, PrivateLink

**Câu 17 — Đáp án: C**
Trong Glacier Flexible Retrieval, Expedited là tầng truy xuất nhanh nhất, thường trong vài phút, với chi phí cao nhất. Standard mất vài giờ, Bulk rẻ nhất nhưng chậm nhất và dành cho khối lượng lớn. Nhu cầu khẩn cấp, ít object thì chọn Expedited.
Keyword: Glacier retrieval, Expedited

**Câu 18 — Đáp án: A, B**
Stack policy định nghĩa rule allow/deny cho thao tác update trên từng resource, bảo vệ resource stateful như RDS khỏi bị replace/delete ngoài ý muốn. Termination protection ngăn xóa stack. Hai cơ chế bổ sung cho nhau để chống thao tác nhầm trên production.
Keyword: Stack policy, termination protection

**Câu 19 — Đáp án: B**
Site-to-Site VPN thiết lập trong vài giờ, chạy qua internet, chi phí thấp, chấp nhận băng thông biến động. Direct Connect cần đặt circuit và thời gian triển khai dài hơn nhiều. Nhu cầu "nhanh, rẻ, tạm chấp nhận biến động" luôn trỏ về VPN.
Keyword: Site-to-Site VPN, quick and low cost

**Câu 20 — Đáp án: B**
Route 53 Resolver outbound endpoint + forwarding rule cho phép VPC phân giải tên miền on-premises. Inbound endpoint cho phép server on-premises truy vấn private hosted zone trong AWS. Cặp inbound/outbound tạo phân giải DNS hai chiều cho hybrid.
Keyword: Route 53 Resolver, inbound/outbound endpoint, hybrid DNS

**Câu 21 — Đáp án: B**
CloudFront là CDN cache nội dung tĩnh (ảnh, CSS, JS) tại edge location gần người dùng, giảm latency và giảm tải origin. Global Accelerator không cache nội dung, nó tối ưu đường truyền TCP/UDP tới endpoint. Nội dung tĩnh toàn cầu thì chọn CloudFront.
Keyword: CloudFront, CDN caching, static content

**Câu 22 — Đáp án: A**
AWS Config ghi lại lịch sử cấu hình resource và dùng managed rule để đánh giá compliance liên tục, ví dụ bucket thiếu encryption. Config trả lời câu hỏi "cấu hình thay đổi như thế nào theo thời gian". CloudTrail ghi API call, CloudWatch đo metrics — không thay thế Config.
Keyword: AWS Config, compliance rule, configuration history

**Câu 23 — Đáp án: B**
S3 File Gateway của Storage Gateway cung cấp giao diện file (NFS/SMB) ngay tại on-premises, cache dữ liệu nóng tại chỗ và lưu bền vững lên S3. Ứng dụng local vẫn dùng giao thức file quen thuộc. DataSync chỉ đồng bộ, không cung cấp giao diện file thường trực.
Keyword: Storage Gateway, File Gateway, S3 backend

**Câu 24 — Đáp án: B**
Snowball là dịch vụ vận chuyển vật lý cho dữ liệu lớn khi mạng quá chậm hoặc không đáng tin. 80 TB chuyển online sẽ mất nhiều tháng, trong khi ship thiết bị chỉ mất vài ngày. Đây là tiêu chí kinh điển để phân biệt Snowball với DataSync/VPN.
Keyword: Snowball, offline transfer, limited bandwidth

**Câu 25 — Đáp án: A**
RAM cho phép chia sẻ tài nguyên AWS xuyên account trong Organization, điển hình là share VPC subnet từ networking account cho application account. Nhờ vậy quản trị mạng tập trung mà team ứng dụng vẫn launch resource được. Peering không tạo cơ chế share subnet.
Keyword: AWS RAM, shared subnets

**Câu 26 — Đáp án: C**
Latency-based routing dùng số đo độ trễ thực tế giữa người dùng và các Region để chọn Region nhanh nhất. Weighted chia theo tỷ lệ cố định, geolocation dựa trên vị trí địa lý theo luật/chính sách. Từ khóa "lowest latency" luôn trỏ về latency-based.
Keyword: Route 53 latency-based routing

**Câu 27 — Đáp án: B**
Lambda authorizer chạy code tùy biến để validate token độc quyền, tra cứu quyền theo tenant và trả về IAM policy cho API Gateway cache. Cognito authorizer chỉ dùng khi danh tính nằm trong Cognito user pool. IdP bên ngoài + logic tùy biến là dấu hiệu của Lambda authorizer.
Keyword: API Gateway Lambda authorizer, custom auth

**Câu 28 — Đáp án: D**
Multi-site active-active cho RTO/RPO thấp nhất vì cả hai Region đều đang phục vụ traffic thật và dữ liệu được replicate liên tục. Khi một Region lỗi, Region còn lại nhận toàn bộ traffic gần như ngay lập tức. Đổi lại, đây là chiến lược DR tốn kém và phức tạp nhất.
Keyword: DR multi-site active-active, lowest RTO/RPO

**Câu 29 — Đáp án: A, B**
Global Accelerator cấp đúng 2 IP anycast tĩnh làm điểm vào cố định và định tuyến qua backbone AWS tới endpoint khỏe gần nhất dựa trên health check. Nó không cache nội dung như CloudFront và không liên quan migration database hay file gateway. Phân biệt GA với CloudFront là điểm thi rất hay gặp.
Keyword: Global Accelerator, anycast IP, AWS backbone

**Câu 30 — Đáp án: B**
VPC peering không có tính bắc cầu (non-transitive): A–B và B–C không suy ra A–C. Muốn định tuyến bắc cầu tập trung ở quy mô lớn phải dùng Transit Gateway làm hub. Đây là giới hạn kiến trúc của peering, không phải lỗi security group hay NAT.
Keyword: VPC peering non-transitive, Transit Gateway

**Câu 31 — Đáp án: B**
CloudWatch thu thập metrics như CPUUtilization, tạo alarm và kích hoạt scaling policy cho ASG. CloudTrail ghi API activity, Config ghi cấu hình, Trusted Advisor đưa khuyến nghị — cả ba đều không cung cấp metric/alarm thời gian thực. Bài toán metric + alarm luôn thuộc CloudWatch.
Keyword: CloudWatch metrics and alarms, auto scaling

**Câu 32 — Đáp án: B**
S3 có ràng buộc: object phải ở Standard ít nhất 30 ngày mới được chuyển sang Standard-IA, và các lớp IA/Glacier đều có thời gian lưu tối thiểu. Chuyển sau 30 ngày sang IA rồi sau 90 ngày sang Glacier tuân thủ ràng buộc và giảm chi phí đúng nhịp truy cập. Chuyển ngày 1 hoặc sau 10 ngày vi phạm quy tắc 30 ngày.
Keyword: S3 Lifecycle constraints, 30-day rule

**Câu 33 — Đáp án: B**
Stack policy là tài liệu JSON gắn với stack, quy định thao tác nào được allow/deny trên resource cụ thể trong lúc stack update. Nhờ đó có thể deny hành động replace RDS production trong khi vẫn cho phép update resource khác. Nó không làm nhiệm vụ backup, encryption hay drift detection.
Keyword: CloudFormation stack policy, deny update

**Câu 34 — Đáp án: B**
VPN là phương án dự phòng kinh điển cho Direct Connect: rẻ, dựng nhanh, sẵn sàng nhận traffic khi circuit chính lỗi dù chạy qua internet. Kết hợp DX chính + VPN backup cân bằng giữa ổn định và chi phí. Snowball hay Transfer Acceleration không phải kết nối mạng dự phòng.
Keyword: Direct Connect backup, VPN failover

**Câu 35 — Đáp án: C**
IAM authorization yêu cầu request ký bằng SigV4 và kiểm soát truy cập theo IAM principal/policy, rất phù hợp API nội bộ giữa các workload AWS. Không cần luồng đăng ký người dùng cuối như Cognito. Lambda authorizer chỉ cần khi có token/logic tùy biến bên ngoài.
Keyword: API Gateway IAM authorization, SigV4

**Câu 36 — Đáp án: A**
Trusted Advisor cung cấp các check có sẵn về cost optimization như idle load balancer, EC2 underutilized, Elastic IP chưa gắn. Đây là báo cáo managed, xem nhanh không cần tự phân tích metrics. Compute Optimizer sâu hơn cho rightsizing compute, còn Trusted Advisor bao quát nhiều loại lãng phí hạ tầng.
Keyword: Trusted Advisor, cost optimization checks

**Câu 37 — Đáp án: A**
Trong geoproximity routing, bias mở rộng hoặc thu hẹp "vùng ảnh hưởng" của một resource mà không cần di chuyển resource thật. Tăng bias cho record US East sẽ kéo thêm traffic về Region đó. TTL hay health check không thay đổi phân bổ địa lý theo cách này.
Keyword: Route 53 geoproximity, bias

**Câu 38 — Đáp án: B**
Nguyên tắc 3-tier an toàn: chỉ ALB được public để nhận traffic internet, tầng application nằm ở private subnet, database ở private subnet sâu nhất và không có route ra internet. Đặt database ở public subnet là lỗi bảo mật nghiêm trọng thường bị đưa vào đáp án nhiễu. NAT gateway chỉ phục vụ traffic ra có kiểm soát từ private subnet khi cần.
Keyword: Private subnets, secure 3-tier placement

**Câu 39 — Đáp án: B**
DMS full load + CDC giúp migrate database đang chạy thật: nạp toàn bộ dữ liệu ban đầu rồi liên tục áp dụng thay đổi phát sinh. Khi cutover, target đã gần như đồng bộ nên downtime rất ngắn. Full load một lần duy nhất sẽ bỏ lỡ mọi thay đổi sau thời điểm export.
Keyword: DMS CDC, ongoing replication, minimal downtime

**Câu 40 — Đáp án: A**
Cost Explorer cho phép phân tích và trực quan chi phí theo service, account, tag, Region... kèm lọc và nhóm tùy ý. Đây là công cụ đầu tiên để truy nguyên spike chi phí. CloudWatch đo hiệu năng, CloudTrail ghi API, Config ghi cấu hình — không phân tích hóa đơn.
Keyword: Cost Explorer, cost breakdown by tag/service

**Câu 41 — Đáp án: A, C**
Direct Connect là kết nối vật lý riêng, băng thông nhất quán, cần thời gian triển khai và chi phí cao hơn. VPN chạy qua internet, dựng nhanh trong vài giờ và rẻ, đổi lại hiệu năng biến động. Ghi nhớ cặp đối lập này: DX = riêng/ổn định/chậm triển khai, VPN = internet/nhanh/rẻ.
Keyword: Direct Connect vs VPN

**Câu 42 — Đáp án: C**
AWS Config lưu configuration item theo thời gian và có timeline xem lại trạng thái cấu hình tại một thời điểm quá khứ, kèm lịch sử thay đổi. Đây đúng nhu cầu kiểm toán cấu hình 3 tháng trước. CloudTrail cho biết ai gọi API, CloudWatch cho metrics — không tái hiện được toàn bộ cấu hình resource.
Keyword: AWS Config timeline, configuration history

**Câu 43 — Đáp án: A**
Compute Optimizer đưa khuyến nghị rightsizing dựa trên metrics lịch sử, và khi bật CloudWatch agent để thu memory metrics thì khuyến nghị tính cả RAM chứ không chỉ CPU. Workload memory-intensive rất dễ bị oversized nếu chỉ nhìn CPU. Đây là cách tránh mua instance thừa cả CPU lẫn memory.
Keyword: Compute Optimizer, memory metrics

**Câu 44 — Đáp án: C**
Bulk retrieval là tầng rẻ nhất của Glacier Flexible Retrieval, thiết kế cho khôi phục khối lượng rất lớn khi thời gian không gấp (thường 5–12 giờ hoặc lâu hơn). Expedited đắt và dành cho khẩn cấp, Standard ở mức trung gian. 50 TB + hạn tuần sau + ưu tiên rẻ thì chọn Bulk.
Keyword: Glacier retrieval, Bulk cheapest

**Câu 45 — Đáp án: B**
VPC endpoint service kết hợp PrivateLink cho phép nhà cung cấp expose dịch vụ sau NLB của mình cho khách hàng kết nối bằng interface endpoint với IP private. Không cần peering, không lộ internet và không vướng giới hạn trùng CIDR như peering. Đây là mô hình chuẩn để bán dịch vụ private xuyên VPC/account.
Keyword: PrivateLink endpoint service, NLB

**Câu 46 — Đáp án: A**
Failover routing chỉ hoạt động đúng khi có health check gắn với record primary để Route 53 biết khi nào primary unhealthy. Khi health check fail, Route 53 tự chuyển truy vấn sang secondary. Thiếu health check thì DNS không có tín hiệu để quyết định failover.
Keyword: Route 53 failover, health check

**Câu 47 — Đáp án: B**
Nested stacks (stack con) cho phép đóng gói từng tier thành module tái sử dụng, parent stack tham chiếu và orchestrate chúng. Mỗi tier có thể được chuẩn hóa, version hóa và tái dùng cho nhiều ứng dụng. Template nguyên khối khổng lồ khó bảo trì và không tái sử dụng được.
Keyword: CloudFormation nested stacks, reusable tiers

**Câu 48 — Đáp án: B**
Compute Savings Plans cam kết mức chi tiêu compute theo giờ trong 1 hoặc 3 năm và tự áp dụng linh hoạt qua EC2, Fargate, Lambda, đổi được instance family, size và Region. Reserved Instance truyền thống gắn chặt hơn với cấu hình cụ thể. Workload steady + cần linh hoạt là dấu hiệu của Savings Plans.
Keyword: Compute Savings Plans, flexible commitment

**Câu 49 — Đáp án: B**
S3 Intelligent-Tiering tự động di chuyển object giữa các access tier dựa trên hành vi truy cập thực tế, có phí giám sát nhỏ nhưng loại bỏ công sức viết lifecycle cho pattern khó đoán. Glacier Deep Archive cho mọi object sẽ gây chậm và tốn phí truy xuất với object đang nóng. Đây là lựa chọn tối ưu khi pattern thay đổi liên tục.
Keyword: S3 Intelligent-Tiering, unpredictable access

**Câu 50 — Đáp án: A**
ASG dùng health check (EC2 hoặc ELB) để phát hiện instance impaired, tự terminate và launch instance thay thế giữ nguyên desired capacity. Cơ chế này diễn ra tự động, không cần quản trị viên can thiệp. Các đáp án còn lại hoặc thủ công, hoặc không liên quan tới compute health.
Keyword: Auto Scaling health check replacement

**Câu 51 — Đáp án: B**
VPC endpoint policy là policy gắn trực tiếp trên endpoint, kiểm soát principal, action và resource được phép đi qua endpoint đó. Giới hạn resource về đúng một bucket ARN sẽ chặn truy cập mọi bucket khác qua endpoint này. Đây là lớp kiểm soát bổ sung cho IAM policy và bucket policy.
Keyword: VPC endpoint policy, restrict to one bucket

**Câu 52 — Đáp án: A, C**
EBS volume không gắn và snapshot thừa là lãng phí phổ biến, xóa sau khi kiểm chứng sẽ giảm chi phí storage ngay. Lifecycle chuyển object ít truy cập sang lớp rẻ hơn cũng cắt giảm trực tiếp hóa đơn S3. Giữ Elastic IP idle hoặc mua thêm On-Demand đều làm tăng chi phí.
Keyword: Cost optimization, delete unattached EBS, S3 lifecycle

**Câu 53 — Đáp án: A**
Snowball Edge ngoài lưu trữ dung lượng lớn còn có khả năng compute tại biên (EC2-compatible/Lambda) cho môi trường mất kết nối. Dữ liệu được xử lý sơ bộ tại chỗ rồi ship thiết bị về AWS để nạp dữ liệu. VPN hay Resolver đều cần kết nối mạng đáng tin cậy — điều địa điểm này không có.
Keyword: Snowball Edge, edge compute, offline

**Câu 54 — Đáp án: A**
Direct Connect bản chất là mạch riêng nhưng không tự mã hóa IPsec; cách chuẩn là tạo Site-to-Site VPN chạy trên public virtual interface của DX để cộng thêm mã hóa IPsec. Nhờ vậy vẫn giữ đường truyền riêng của DX mà dữ liệu được mã hóa đầu-cuối. Các đáp án còn lại thuộc tầng ứng dụng/log, không mã hóa đường truyền.
Keyword: VPN over Direct Connect, IPsec encryption

**Câu 55 — Đáp án: A**
Transit Gateway đóng vai trò hub định tuyến trung tâm: mỗi VPC mới chỉ cần tạo attachment và cấu hình route table của TGW là kết nối được tới on-premises qua Direct Connect Gateway đã có. Không cần kéo circuit riêng cho từng VPC. Đây là lợi thế mở rộng cốt lõi của mô hình hub-and-spoke.
Keyword: Transit Gateway hub, Direct Connect Gateway

**Câu 56 — Đáp án: B**
Global Accelerator liên tục health-check endpoint; khi cả endpoint group chính unhealthy, traffic được chuyển sang endpoint group khỏe ở Region gần nhất tiếp theo. IP anycast tĩnh không thay đổi nên client không cần cấu hình lại. GA không cache nội dung và không chuyển đổi giao thức như CloudFront.
Keyword: Global Accelerator failover, health check

**Câu 57 — Đáp án: B**
Private API chỉ truy cập được qua VPC endpoint được chỉ định, và resource policy phải allow endpoint đó đồng thời deny mọi nguồn khác để chặn cả khi URL bị lộ. API key hay Cognito public không tạo tính private ở tầng mạng. Đây là bộ đôi private API + resource policy thường đi cùng nhau trong đề thi.
Keyword: Private API, resource policy, VPC endpoint

**Câu 58 — Đáp án: A, B**
Inbound endpoint nhận truy vấn DNS từ on-premises vào Resolver trong VPC, phục vụ phân giải private hosted zone. Outbound endpoint kèm forwarding rule gửi truy vấn từ VPC ra DNS server on-premises cho tên miền nội bộ của công ty. Thiếu một trong hai chiều, hybrid DNS sẽ không hoàn chỉnh.
Keyword: Route 53 Resolver, inbound + outbound

**Câu 59 — Đáp án: A**
CloudWatch Logs tập trung log ứng dụng, metric filter trích xuất pattern lỗi thành metric, và CloudWatch alarm cảnh báo khi vượt ngưỡng. Đây là chuỗi log → filter → alarm kinh điển của CloudWatch. Config và CloudTrail phục vụ cấu hình và audit API, không phân tích application log theo cách này.
Keyword: CloudWatch Logs, metric filter, alarm

**Câu 60 — Đáp án: B**
Đặc trưng warm standby là hạ tầng và dữ liệu đã sẵn sàng ở Region DR: database đang replicate, ứng dụng đang chạy ở quy mô nhỏ. Khi failover chỉ cần promote database, scale up ứng dụng và chuyển DNS bằng Route 53 sang DR. Khác hẳn backup-restore phải dựng lại mọi thứ từ snapshot.
Keyword: Warm standby failover, promote replica, Route 53

**Câu 61 — Đáp án: B**
Glacier được thiết kế cho lưu trữ lạnh: truy xuất chậm, có phí retrieval và thời gian lưu tối thiểu, nên truy cập thường xuyên trong tháng đầu sẽ tốn kém và chậm. Cách đúng là giữ log ở Standard/Standard-IA trong giai đoạn còn phân tích tích cực, rồi mới lifecycle sang Glacier sau khoảng 90 ngày. Đề xuất chuyển ngày 1 bỏ qua hoàn toàn hành vi truy cập thực tế.
Keyword: Glacier trade-off, retrieval cost, lifecycle timing

**Câu 62 — Đáp án: A**
Transit Gateway cho phép dùng nhiều route table riêng để phân đoạn traffic: attachment nào gắn route table nào sẽ chỉ nói chuyện được với các đích được cho phép. Nhờ vậy kiểm soát được ma trận kết nối giữa các phòng ban ở quy mô lớn. Peering mesh không có khả năng kiểm soát tập trung và không bắc cầu.
Keyword: Transit Gateway route tables, segmentation

**Câu 63 — Đáp án: A**
Cost Explorer cung cấp sẵn giao diện trực quan phân tích chi phí theo service, linked account, Region, tag trong tối đa 12 tháng kèm xu hướng và forecast cơ bản. Lãnh đạo xem được ngay nguyên nhân hóa đơn tăng mà không cần xây pipeline báo cáo. CloudWatch dashboard chỉ hiển thị metric kỹ thuật, không phải dữ liệu billing.
Keyword: Cost Explorer, cost by service/account

**Câu 64 — Đáp án: A, B**
Bộ ba cần phân biệt rõ: CloudWatch = metrics/logs/alarm về hiệu năng và vận hành; CloudTrail = audit trail ghi ai gọi API gì, khi nào; Config = lịch sử và compliance của cấu hình resource. Hai phát biểu A và B mô tả đúng CloudWatch và CloudTrail. Các phát biểu còn lại gán nhầm vai trò CDN/database cho Config và CloudTrail.
Keyword: CloudWatch vs CloudTrail vs Config

**Câu 65 — Đáp án: B**
Đáp án B hội đủ best practice ở mọi lớp: HA Multi-AZ ở Region chính, warm standby cho DR, change set để review trước khi update stack, Direct Connect có VPN dự phòng, lifecycle S3 để giảm chi phí lưu trữ và Route 53 failover theo health check. Các đáp án còn lại đều chứa lỗi kinh điển như single-AZ, database public, nhầm vai trò CloudFront/Global Accelerator hoặc giữ toàn bộ dữ liệu ở Standard.
Keyword: Capstone architecture, HA + DR + cost + hybrid
