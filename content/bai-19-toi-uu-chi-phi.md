# Bài 19 — Tối Ưu Chi Phí

## Mục tiêu bài học

- Nắm tư duy Cost-Optimized theo AWS Well-Architected Framework: đáp ứng đủ yêu cầu với chi phí thấp nhất, không phải cắt chi phí bằng mọi giá.
- Phân biệt đúng 5 công cụ quản lý chi phí: Cost Explorer, AWS Budgets, Cost and Usage Report, Trusted Advisor, Compute Optimizer.
- Thuộc các đòn bẩy tiết kiệm ở 3 tầng: compute (Savings Plans, Spot, On-Demand), storage (S3 Lifecycle, gp3) và network (NAT Gateway, VPC Endpoint, CloudFront), cùng việc dọn tài nguyên mồ côi.

## Lý thuyết chính

### 1. Tư duy cost theo Well-Architected

Domain Cost-Optimized (20% đề thi) không hỏi "cái nào rẻ nhất tuyệt đối" mà hỏi: **"most cost-effective" cho đúng workload trong scenario**. Ba nguyên tắc xuyên suốt:

- **Đo trước, tối ưu sau:** không biết tiền đi đâu thì không tối ưu được — dùng công cụ phân tích chi phí trước khi ra quyết định.
- **Cam kết đổi lấy giảm giá:** workload chạy ổn định, đoán trước được → cam kết sử dụng (Savings Plans) để được giá thấp. Workload ngắn hạn/bất định → On-Demand.
- **Khớp tài nguyên với nhu cầu (right-sizing) và xóa lãng phí:** instance quá khổ, volume mồ côi, dữ liệu lạnh để ở tier nóng đều là tiền rò rỉ.

### 2. Năm công cụ quản lý chi phí — phân biệt theo câu hỏi đề

| Công cụ | Trả lời câu hỏi | Đặc điểm ghi nhớ |
|---|---|---|
| **AWS Cost Explorer** | "Tiền đang tiêu vào đâu, xu hướng thế nào?" | Phân tích/trực quan hóa chi phí theo dịch vụ, tài khoản, tag; có dự báo (forecast) |
| **AWS Budgets** | "Khi nào tôi cần được cảnh báo?" | Đặt ngân sách, **cảnh báo (alert)** khi chi phí thực tế/dự báo vượt ngưỡng, có thể gắn hành động |
| **Cost and Usage Report (CUR)** | "Cho tôi dữ liệu chi phí chi tiết nhất" | Báo cáo **chi tiết nhất (most detailed)**, xuất ra S3, phân tích bằng Athena/QuickSight |
| **AWS Trusted Advisor** | "AWS khuyến nghị tôi sửa gì?" | Đưa khuyến nghị theo nhiều trụ cột: cost optimization, performance, security, fault tolerance — ví dụ EC2 idle, volume mồ côi |
| **AWS Compute Optimizer** | "Instance nào đang quá khổ/quá nhỏ?" | Phân tích metrics thực tế và **khuyến nghị rightsize** cho EC2, ASG, Lambda, EBS... |

> Bẫy phân biệt kinh điển: "alert when spending exceeds threshold" → **Budgets**. "most detailed billing data" → **CUR**. "visualize and analyze costs" → **Cost Explorer**. "recommendation to rightsize instances" → **Compute Optimizer**.

### 3. Đòn bẩy compute

**Savings Plans (SP)** — cam kết mức sử dụng (USD/giờ) trong 1 hoặc 3 năm để được giảm giá so với On-Demand. Ba loại cần thuộc:

- **Compute Savings Plans:** **linh hoạt nhất (most flexible)** — áp dụng cho EC2 (mọi family, mọi Region), Fargate và Lambda; đổi instance family/Region vẫn được hưởng.
- **EC2 Instance Savings Plans:** cam kết theo **instance family + Region** cụ thể → linh hoạt thấp hơn nhưng **giảm sâu hơn** Compute SP.
- **SageMaker Savings Plans:** dành cho Amazon SageMaker.

Nguyên tắc chọn: workload ổn định nhưng có thể đổi cấu hình/Region → Compute SP. Workload cố định family + Region dài hạn → EC2 Instance SP để giảm tối đa.

**Spot Instances** — dùng năng lực EC2 dư thừa với giá giảm sâu, đổi lại **có thể bị AWS thu hồi (interruption)** khi AWS cần lại capacity. Chỉ phù hợp workload **chịu được gián đoạn**: batch processing, CI/CD, xử lý ảnh/video, job chạy lại được, workload stateless có checkpoint. **Tuyệt đối không** dùng Spot cho database production, ứng dụng không được phép dừng giữa chừng.

**On-Demand** — giá niêm yết, không cam kết, bật/tắt tùy ý. Phù hợp: workload **ngắn hạn**, dev/test, ứng dụng mới chưa đoán được nhu cầu, spike bất định. Đề nói "short-term, unpredictable, cannot be interrupted" → On-Demand (không phải Spot, chưa đủ ổn định để mua SP).

Các đòn bẩy phụ: rightsize instance theo Compute Optimizer, tắt tài nguyên dev ngoài giờ làm việc, chọn Graviton khi phù hợp.

### 4. Đòn bẩy storage

- **S3 Lifecycle Policies:** tự động chuyển object sang tier rẻ hơn theo tuổi dữ liệu hoặc xóa khi hết hạn. Chuỗi quen thuộc: S3 Standard → Standard-IA → Glacier Instant/Flexible → Glacier Deep Archive → Expire.
- **S3 Intelligent-Tiering:** dành cho dữ liệu **không đoán được pattern truy cập** — S3 tự theo dõi và chuyển object giữa các tier theo hành vi truy cập thực tế. Đề nói "unknown or changing access patterns" → Intelligent-Tiering.
- **EBS gp3 thay gp2:** gp3 là thế hệ mới hơn, **rẻ hơn gp2 và hiệu năng tốt hơn**, cho phép cấu hình IOPS/throughput độc lập với dung lượng. Đề hỏi nâng cấp volume "cost-effective" → chuyển gp2 → gp3 gần như luôn đúng.
- **Dọn tài nguyên mồ côi (orphaned resources):** EBS volume **không gắn** vào instance nào, **snapshot cũ** không còn cần, **Elastic IP thừa** không gắn (EIP không dùng bị tính phí). Trusted Advisor giúp phát hiện các mục này.

### 5. Đòn bẩy network — phần hay bị quên nhất

- **NAT Gateway tính phí theo giờ + theo GB dữ liệu đi qua.** Instance trong private subnet gọi ra internet / gọi tới S3 qua NAT Gateway đều tốn tiền xử lý dữ liệu.
- **VPC Gateway Endpoint cho S3 và DynamoDB là MIỄN PHÍ:** traffic từ VPC tới S3/DynamoDB đi qua Gateway Endpoint sẽ **không qua NAT Gateway**, vừa rẻ hơn vừa private hơn. Đây là đáp án kinh điển cho scenario "chi phí NAT Gateway tăng vọt vì EC2 trong private subnet tải dữ liệu từ S3".
  - Lưu ý: Gateway Endpoint chỉ có cho **S3 và DynamoDB**. Các dịch vụ AWS khác dùng Interface Endpoint (PrivateLink) — có tính phí.
- **Data transfer ra internet đắt:** truyền dữ liệu ra ngoài AWS (egress) tốn phí đáng kể. **CloudFront giúp giảm chi phí** vì nội dung được cache ở edge location, giảm lượng dữ liệu gốc phải truyền từ Region và giảm tải cho origin.
- Nguyên tắc phụ: giữ traffic trong cùng AZ/Region khi có thể, tránh truyền cross-Region không cần thiết.

### 6. Cost Allocation Tags

- Gắn tag (ví dụ `Project`, `Team`, `Environment`) lên tài nguyên, kích hoạt trong Billing để **theo dõi và phân bổ chi phí theo team/dự án/môi trường**.
- Đề hỏi "track costs by project/department" hoặc "chargeback/showback" → đáp án là Cost Allocation Tags + Cost Explorer/CUR để báo cáo.
- Lưu ý thực tế: tag chỉ có tác dụng theo dõi sau khi được **activate** trong Billing console, và chỉ áp dụng cho chi phí phát sinh sau đó.

## Ví dụ đời thường

Tối ưu chi phí AWS giống quản lý chi tiêu một nhà hàng:

- **Cost Explorer** là sổ thu chi có biểu đồ — nhìn là biết tiền hao nhất ở bếp, mặt bằng hay nhân sự.
- **AWS Budgets** là chuông báo: "tháng này tiêu quá 80% ngân sách thì nhắn tin cho chủ quán".
- **CUR** là hóa đơn chi tiết từng dòng — mua bao nhiêu hành, ngày nào, giá nào — để kế toán soi tận gốc.
- **Savings Plans** như ký hợp đồng mua gạo cả năm với giá sỉ: rẻ hơn hẳn mua lẻ mỗi ngày (On-Demand), nhưng phải chắc chắn là quán dùng hết.
- **Spot** như mua thực phẩm cuối ngày ở chợ đầu mối giảm giá sâu — ngon rẻ, nhưng có thể bị người khác mua mất bất cứ lúc nào, nên chỉ hợp cho món chế biến được ngay, không hợp để hứa với khách đặt tiệc.
- **NAT Gateway** như thuê shipper ngoài theo chuyến + theo cân nặng; còn **Gateway Endpoint tới S3** như lối đi nội bộ miễn phí xuống kho của chính bạn — tội gì cứ gọi shipper.
- **Volume mồ côi** như tủ lạnh vẫn cắm điện trong kho dù quán đã bỏ món đó từ lâu — không ai dùng mà tiền điện vẫn chạy.

## Phân biệt dễ nhầm

- **Cost Explorer vs CUR:** Explorer để **nhìn và phân tích nhanh** trên console; CUR là **dữ liệu thô chi tiết nhất** xuất ra S3 để tự phân tích sâu. "Most detailed" → CUR.
- **Budgets vs Cost Explorer:** Explorer phân tích quá khứ/xu hướng; Budgets là **ngưỡng + cảnh báo + hành động**. Có chữ "alert/notify when exceeds" → Budgets.
- **Trusted Advisor vs Compute Optimizer:** Trusted Advisor bao quát nhiều trụ cột (cost, security, performance...). Compute Optimizer chuyên sâu vào **rightsize tài nguyên compute** dựa trên metrics. Hỏi rightsize EC2 cụ thể → Compute Optimizer.
- **Compute SP vs EC2 Instance SP:** Compute SP linh hoạt nhất (đổi family, Region, áp dụng cả Fargate/Lambda). EC2 Instance SP khóa family + Region nhưng giảm sâu hơn. Đề nhấn "flexibility" → Compute SP; nhấn "greatest discount, workload will not change" → EC2 Instance SP.
- **Spot vs On-Demand:** Cùng là trả theo giờ không cam kết dài, nhưng Spot **bị thu hồi được**. Workload "cannot tolerate interruption" → loại Spot ngay.
- **Gateway Endpoint vs Interface Endpoint:** Gateway Endpoint miễn phí, chỉ cho S3 và DynamoDB. Interface Endpoint (PrivateLink) cho các dịch vụ khác và **có tính phí**.

## Bẫy đề thi

- **Bẫy 1:** Scenario EC2 private subnet tốn phí NAT Gateway vì download dữ liệu S3 liên tục — đáp án cám dỗ là "mua NAT Gateway lớn hơn" hoặc "chuyển instance ra public subnet" (phá vỡ bảo mật). Đáp án đúng: **VPC Gateway Endpoint cho S3 (miễn phí)**.
- **Bẫy 2:** Đề cho workload "fault-tolerant batch job, can be interrupted and resumed" mà không chọn Spot — bỏ lỡ đáp án rẻ nhất. Ngược lại, workload database/stateful quan trọng mà chọn Spot là sai chết người.
- **Bẫy 3:** Hỏi "most detailed cost and usage data" lại chọn Cost Explorer vì quen mắt — phải chọn **CUR**.
- **Bẫy 4:** Workload mới, nhu cầu chưa rõ, chạy vài tuần thử nghiệm — lại đi mua Savings Plans 3 năm. Chưa ổn định thì On-Demand trước.
- **Bẫy 5:** Quên các khoản rò rỉ âm thầm: EBS volume unattached, snapshot cũ, Elastic IP không gắn. Câu hỏi "identify unused resources to reduce cost" thường nhắm vào nhóm này và Trusted Advisor.

## Tóm tắt 5 dòng

- Công cụ: Cost Explorer phân tích, Budgets cảnh báo theo ngưỡng, CUR chi tiết nhất, Trusted Advisor khuyến nghị, Compute Optimizer rightsize.
- Compute: Compute SP linh hoạt nhất, EC2 Instance SP giảm sâu nhất theo family+Region; Spot cho workload chịu được gián đoạn, On-Demand cho ngắn hạn/bất định.
- Storage: S3 Lifecycle chuyển tier theo tuổi, Intelligent-Tiering cho pattern khó đoán, EBS gp3 rẻ và tốt hơn gp2.
- Network: NAT Gateway tốn phí theo giờ + GB — dùng Gateway Endpoint miễn phí cho S3/DynamoDB để cắt traffic qua NAT; CloudFront giảm chi phí egress.
- Luôn bật Cost Allocation Tags theo team/dự án và dọn tài nguyên mồ côi: volume không gắn, snapshot cũ, Elastic IP thừa.

## Quiz

**Question 1.** A company needs the MOST detailed cost and usage data available for its AWS accounts so that its finance team can run custom analysis with Amazon Athena. Which AWS offering should the company use?

A. AWS Cost Explorer
B. AWS Budgets
C. AWS Cost and Usage Report
D. AWS Trusted Advisor

**Question 2.** A company's EC2 instances in private subnets download large amounts of data from Amazon S3 every day. The monthly bill shows rapidly growing NAT Gateway data processing charges. Which solution will MOST cost-effectively reduce these charges while keeping the instances in private subnets?

A. Move the EC2 instances to public subnets and assign Elastic IP addresses.
B. Create a VPC gateway endpoint for Amazon S3 and route S3 traffic through it.
C. Replace the NAT Gateway with a larger NAT Gateway instance type.
D. Deploy an Amazon CloudFront distribution in front of the S3 bucket.

**Question 3.** A company runs a steady-state production workload on the same EC2 instance family in the same AWS Region, and this is not expected to change for the next 3 years. The company wants the deepest possible discount compared to On-Demand pricing. Which purchasing option is the MOST appropriate?

A. Spot Instances
B. Compute Savings Plans
C. EC2 Instance Savings Plans
D. On-Demand Instances with nightly shutdowns

**Question 4.** A data processing team runs nightly batch jobs on EC2 instances. The jobs can be interrupted at any time and safely resumed from checkpoints without data loss. Which purchasing option will MOST cost-effectively run these jobs?

A. On-Demand Instances
B. Dedicated Hosts
C. Spot Instances
D. EC2 Instance Savings Plans

**Question 5.** A finance manager wants to receive an alert when the forecasted AWS spend for a project reaches 80% of its monthly budget, and wants costs tracked separately by project and team. Which combination of actions meets these requirements? (Select the best answer.)

A. Use AWS Cost Explorer forecasts and check the console daily.
B. Use AWS Budgets for threshold alerts and activate Cost Allocation Tags to track costs by project and team.
C. Use AWS Trusted Advisor to send budget alerts and rely on account names for cost tracking.
D. Use the Cost and Usage Report with a Lambda function to delete resources at 80% usage.

## Đáp án quiz

**Câu 1 — Đáp án C.** Cost and Usage Report (CUR) là nguồn dữ liệu chi phí **chi tiết nhất**, xuất ra S3 để phân tích bằng Athena/QuickSight — khớp từ khóa "most detailed". Cost Explorer phục vụ phân tích trực quan nhanh, Budgets phục vụ ngân sách/cảnh báo, Trusted Advisor đưa khuyến nghị — không cái nào là dữ liệu thô chi tiết nhất.

**Câu 2 — Đáp án B.** Gateway Endpoint cho S3 **miễn phí** và đưa traffic S3 ra khỏi NAT Gateway, giữ nguyên private subnet — vừa rẻ nhất vừa đúng bảo mật. A phá vỡ yêu cầu private và tăng rủi ro bảo mật. C sai bản chất vì NAT Gateway không có "instance type lớn hơn" để đổi, và vẫn tính phí theo GB. D không giải quyết luồng EC2 → S3 nội bộ trong bài toán này.

**Câu 3 — Đáp án C.** Workload ổn định, **cố định family + Region trong 3 năm** là điều kiện lý tưởng của EC2 Instance Savings Plans — đổi lại cam kết cứng là mức giảm sâu hơn Compute SP. Compute SP (B) linh hoạt hơn nhưng giảm ít hơn, chỉ thắng khi workload cần đổi family/Region/dịch vụ. Spot (A) không phù hợp production ổn định không chịu gián đoạn. D không phải cam kết giảm giá và việc tắt máy đêm không áp dụng cho workload chạy liên tục.

**Câu 4 — Đáp án C.** Batch job có checkpoint, **chịu được gián đoạn và chạy lại an toàn** là chân dung hoàn hảo của Spot Instances — giá rẻ nhất trong các lựa chọn. Đây là pattern đề thi lặp lại nhiều lần: thấy "fault-tolerant / interruptible / checkpoint" → Spot.

**Câu 5 — Đáp án B.** "Alert khi đạt ngưỡng ngân sách" là chức năng của **AWS Budgets** (cảnh báo theo chi phí thực tế và dự báo), còn "theo dõi chi phí theo project/team" là **Cost Allocation Tags** sau khi activate trong Billing. Cost Explorer (A) không tự gửi alert theo ngưỡng ngân sách. Trusted Advisor (C) không phải công cụ đặt ngân sách. D dùng CUR sai mục đích và hành động xóa tài nguyên tự động là nguy hiểm, không phải yêu cầu của đề.
