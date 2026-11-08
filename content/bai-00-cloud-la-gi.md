# Bài 00 — Cloud Computing là gì? Giới thiệu AWS

## Mục tiêu bài học
- Hiểu Cloud Computing là gì bằng ngôn ngữ đời thường
- Nắm được lợi ích cốt lõi: pay-as-you-go, elasticity, agility, global reach
- Phân biệt được IaaS / PaaS / SaaS
- Hiểu các mô hình triển khai: Public Cloud, Private Cloud, Hybrid Cloud
- Biết cấu trúc hạ tầng toàn cầu của AWS: Region, Availability Zone, Edge Location
- Nắm Shared Responsibility Model — phần nào AWS lo, phần nào mình lo
- Biết Well-Architected Framework gồm 6 trụ cột
- Nắm thông tin cơ bản về kỳ thi SAA-C03

## Lý thuyết chính

### 1. Cloud Computing là gì?

**Cloud Computing** là việc thuê tài nguyên IT (máy chủ, lưu trữ, database, network) qua Internet, dùng bao nhiêu trả bấy nhiêu, thay vì tự mua máy chủ đặt ở công ty.

Trước đây, muốn có website, bạn phải mua server, thuê chỗ đặt, thuê người bảo trì, mua điện, điều hòa. Với Cloud, bạn chỉ cần vài cú click là có server chạy trong vài phút.

AWS (Amazon Web Services) là nhà cung cấp Cloud lớn nhất thế giới. SAA-C03 là chứng chỉ **AWS Certified Solutions Architect – Associate**, chứng chỉ dành cho người thiết kế hệ thống trên AWS.

Thông tin kỳ thi SAA-C03 cần nhớ ngay từ đầu:
- 65 câu hỏi trắc nghiệm (50 câu tính điểm + 15 câu không tính điểm, bạn không biết câu nào không tính điểm)
- Thời gian: 130 phút
- Điểm đạt: 720/1000
- Lệ phí: $150
- Hiệu lực: 3 năm
- **KHÔNG có đề tiếng Việt** — đề thi chỉ có tiếng Anh và một số ngôn ngữ khác, không có tiếng Việt. Vì vậy học phải nhớ keyword tiếng Anh.
- Trọng số 4 domain: **Secure Applications and Architectures 30%**, **Resilient Architectures 26%**, **High-Performing Architectures 24%**, **Cost-Optimized Architectures 20%**

### 2. Lợi ích cốt lõi của Cloud

- **Pay-as-you-go:** Dùng bao nhiêu trả bấy nhiêu, như tiền điện nước. Không dùng thì tắt đi là không tốn tiền compute.
- **Elasticity:** Tăng/giảm tài nguyên tự động theo nhu cầu. Trưa đông khách thì tăng server, đêm ít khách thì giảm server.
- **Scalability:** Hệ thống lớn lên được khi business lớn lên, không phải đập đi xây lại.
- **Agility:** Thử nghiệm nhanh, sai thì xóa. Ra tính năng mới trong vài giờ thay vì vài tháng.
- **Global in minutes:** Triển khai hệ thống ra nhiều nước trong vài phút.
- **Trade capital expense for variable expense:** Biến chi phí đầu tư ban đầu lớn (CapEx) thành chi phí vận hành theo用量 (OpEx).
- **Stop guessing capacity:** Không cần đoán trước cần bao nhiêu server.
- **Economies of scale:** AWS mua phần cứng số lượng khổng lồ nên giá rẻ hơn bạn tự mua.

Phân biệt nhỏ nhưng hay thi: **Elasticity** là khả năng tự co giãn theo load ở thời điểm hiện tại. **Scalability** là khả năng hệ thống chịu được khi lớn lên về lâu dài.

### 3. Các mô hình dịch vụ: IaaS / PaaS / SaaS

Hãy tưởng tượng từ thấp đến cao, càng lên cao bạn càng ít phải quản lý:

- **IaaS — Infrastructure as a Service:** AWS cho thuê hạ tầng thô: máy ảo, network, storage. Bạn tự cài OS, tự cài phần mềm. Ví dụ: **Amazon EC2**. Bạn quản lý nhiều nhất, linh hoạt nhất.
- **PaaS — Platform as a Service:** AWS lo sẵn platform, bạn chỉ đưa code lên chạy. Ví dụ: **AWS Elastic Beanstalk**. Bạn không cần lo OS, patching.
- **SaaS — Software as a Service:** Dùng phần mềm có sẵn qua Internet, không cài gì. Ví dụ: Gmail, Dropbox, Salesforce. Bạn chỉ là người dùng cuối.

Keyword đề thi: EC2 = IaaS, Elastic Beanstalk = PaaS, Gmail = SaaS.

### 4. Mô hình triển khai

- **Public Cloud:** Dùng hạ tầng của AWS, chia sẻ với khách hàng khác nhưng dữ liệu tách biệt. Ví dụ: chạy toàn bộ trên AWS.
- **Private Cloud / On-premises:** Hạ tầng riêng trong data center của công ty. Kiểm soát cao nhưng tốn kém.
- **Hybrid Cloud:** Kết hợp cả hai — một phần on-premises, một phần trên AWS, kết nối với nhau. Rất phổ biến trong doanh nghiệp lớn và là đáp án hay gặp trong đề thi khi công ty muốn migrate dần.

### 5. Hạ tầng toàn cầu của AWS

Đây là phần chắc chắn có trong đề thi:

- **Region:** Một khu vực địa lý độc lập, ví dụ `us-east-1` (Virginia), `ap-southeast-1` (Singapore). Mỗi Region hoàn toàn độc lập với Region khác. Chọn Region dựa trên: latency (gần người dùng), compliance (luật dữ liệu), cost (giá mỗi Region khác nhau), và service availability (không phải dịch vụ nào cũng có ở mọi Region).
- **Availability Zone (AZ):** Mỗi Region gồm nhiều AZ. Mỗi AZ là một hoặc nhiều data center vật lý riêng biệt, cách nhau đủ xa để không cùng ngập lụt/mất điện, nhưng đủ gần để độ trễ thấp. AZ được ký hiệu như `us-east-1a`, `us-east-1b`. Thiết kế chuẩn là chạy hệ thống trên **ít nhất 2 AZ** để đạt High Availability.
- **Edge Location:** Điểm đặt máy chủ biên, gần người dùng, dùng cho **Amazon CloudFront** (CDN) và **Route 53**. Số lượng Edge Location nhiều hơn số Region rất nhiều. Nhiệm vụ của nó là cache nội dung và giảm latency, không phải nơi chạy EC2 chính.
- **Local Zones, Wavelength, Outposts:** Mở rộng của AWS ra gần người dùng hơn hoặc vào data center của khách hàng — chỉ cần biết khái niệm ở mức Associate.

Nguyên tắc vàng: **Region là độc lập, AZ là độc lập trong Region**. Sập 1 AZ không được làm sập hệ thống của bạn nếu bạn thiết kế đúng.

### 6. Shared Responsibility Model

Đây là mô hình **trách nhiệm chia sẻ** giữa AWS và khách hàng — câu hỏi kinh điển trong mọi đề thi AWS.

- **AWS chịu trách nhiệm về Security OF the Cloud:** Phần cứng, data center, network toàn cầu, Region/AZ, phần mềm ảo hóa. AWS lo bảo mật *của* đám mây.
- **Khách hàng chịu trách nhiệm về Security IN the Cloud:** Dữ liệu của bạn, cấu hình IAM, cấu hình Security Group, mã hóa dữ liệu, patch OS trên EC2, cài antivirus trên EC2. Bạn lo bảo mật *trong* đám mây.

Với dịch vụ càng managed (ví dụ Lambda, S3), AWS lo càng nhiều. Với IaaS như EC2, bạn lo càng nhiều — kể cả việc vá lỗi hệ điều hành.

Nhớ câu thần chú: **AWS lo OF, Customer lo IN.**

### 7. Well-Architected Framework — 6 trụ cột

Khung thiết kế hệ thống tốt trên AWS gồm 6 trụ cột (pillars). Đề thi hay hỏi tên trụ cột:

1. **Operational Excellence** — Vận hành xuất sắc: chạy, giám sát, cải tiến liên tục, Infrastructure as Code.
2. **Security** — Bảo mật: IAM, mã hóa, least privilege, traceability.
3. **Reliability** — Độ tin cậy: tự phục hồi khi lỗi, scale ngang, backup.
4. **Performance Efficiency** — Hiệu quả hiệu năng: chọn đúng loại tài nguyên, dùng serverless khi phù hợp.
5. **Cost Optimization** — Tối ưu chi phí: pay-as-you-go, đo lường, tắt tài nguyên thừa.
6. **Sustainability** — Bền vững: giảm tác động môi trường, dùng tài nguyên hiệu quả.

Khi đề thi mô tả một tình huống, hãy nghĩ: câu này đang hỏi về trụ cột nào?

## Ví dụ đời thường

**Cloud giống như đi thuê nhà / dùng điện nước, không phải mua đất xây nhà.**

- Tự mua server giống như tự mua đất, xây nhà, tự kéo điện nước. Đắt lúc đầu, nhà chật thì phải xây lại, dọn đi cũng khó bán.
- Dùng Cloud giống như thuê căn hộ dịch vụ: cần phòng to thì thuê phòng to, tháng sau ít người thì chuyển phòng nhỏ. Điện nước dùng bao nhiêu trả bấy nhiêu. Hỏng bóng đèn thì chủ nhà sửa — đó là phần AWS lo trong Shared Responsibility Model.
- **Elasticity** giống như quán phở: buổi sáng đông khách thì kê thêm bàn ghế ra vỉa hè, buổi chiều vắng thì cất bàn đi. Không ai mua đứt cả mặt bằng vỉa hè chỉ vì 2 giờ đông khách buổi sáng.
- **Region** giống như chuỗi cửa hàng ở Hà Nội, Đà Nẵng, Sài Gòn — mỗi thành phố là một Region độc lập. **AZ** là các cửa hàng khác nhau trong cùng một thành phố, đặt ở các quận khác nhau để nếu một quận mất điện thì cửa hàng quận khác vẫn bán được.
- **IaaS/PaaS/SaaS:** IaaS là thuê đất trống tự xây quán. PaaS là thuê mặt bằng đã có sẵn bếp, bàn ghế, chỉ mang công thức phở tới nấu. SaaS là đi ăn phở có sẵn, ăn xong trả tiền, không lo gì cả.

## Phân biệt dễ nhầm

| Cặp dễ nhầm | Cách phân biệt |
|---|---|
| Region vs Availability Zone | Region là khu vực địa lý lớn (Singapore). AZ là data center độc lập *bên trong* Region đó |
| Availability Zone vs Edge Location | AZ để chạy workload chính (EC2, RDS). Edge Location để cache nội dung qua CloudFront, số lượng nhiều hơn hẳn |
| Elasticity vs Scalability | Elasticity = co giãn tự động theo load hiện tại. Scalability = khả năng lớn lên lâu dài |
| IaaS vs PaaS | IaaS bạn quản lý OS (EC2). PaaS AWS quản lý OS/platform, bạn chỉ đưa code (Elastic Beanstalk) |
| Security OF vs IN the Cloud | OF = AWS lo hạ tầng. IN = Bạn lo dữ liệu, IAM, cấu hình |
| Public Cloud vs Hybrid | Hybrid nhất định phải có cả on-premises + cloud kết nối với nhau |

## Bẫy đề thi

- Đề nói "một AZ bị mất điện, hệ thống sập" rồi hỏi cách tránh: đáp án luôn hướng tới **deploy across multiple AZs**, không phải mua server to hơn.
- Đề hỏi về Edge Location: đáp án liên quan tới **CloudFront / CDN / giảm latency cho nội dung tĩnh**, đừng chọn EC2.
- Đề hỏi trách nhiệm patch OS trên EC2: đó là **trách nhiệm của khách hàng**, không phải AWS. Nếu là RDS hay Lambda thì AWS lo nhiều hơn.
- Đề đưa tình huống "công ty muốn giữ một phần dữ liệu nhạy cảm tại data center riêng, phần còn lại lên Cloud" — đó là **Hybrid Cloud**.
- Nhiều tài liệu cũ vẫn nói những con số hạ tầng toàn cầu cụ thể đã lỗi thời. Đề thi SAA-C03 không kiểm tra bạn nhớ chính xác số Region hiện tại, mà kiểm tra bạn hiểu khái niệm Region/AZ dùng để làm gì: High Availability, Disaster Recovery, latency, compliance.
- Nhớ trọng số: Secure 30% là cao nhất. Ngay từ bài 00, hãy hiểu là bảo mật sẽ xuyên suốt cả kỳ thi.

## Tóm tắt 5 dòng
Cloud là thuê tài nguyên IT qua Internet, dùng bao nhiêu trả bấy nhiêu, với lợi ích lớn nhất là elasticity và agility.
IaaS (EC2) bạn quản nhiều nhất, PaaS (Elastic Beanstalk) ở giữa, SaaS bạn chỉ dùng phần mềm có sẵn.
AWS chia thế giới thành Region, mỗi Region có nhiều Availability Zone độc lập — thiết kế tối thiểu 2 AZ để có High Availability.
Shared Responsibility Model: AWS lo Security OF the Cloud, bạn lo Security IN the Cloud — dữ liệu và cấu hình là của bạn.
Well-Architected Framework có 6 trụ cột: Operational Excellence, Security, Reliability, Performance Efficiency, Cost Optimization, Sustainability.

## Quiz

**Câu 1:** A company wants to deploy an application across multiple isolated data centers within a single geographic area to achieve high availability. Which AWS component should they use?

A. Multiple Regions
B. Multiple Availability Zones within a single Region
C. Multiple Edge Locations
D. Multiple AWS accounts

**Câu 2:** According to the Shared Responsibility Model, which of the following is the CUSTOMER's responsibility when using Amazon EC2?

A. Physical security of the data center
B. Patching the guest operating system
C. Maintaining the underlying hardware
D. Managing the virtualization software

**Câu 3:** Which service model describes AWS Elastic Beanstalk, where the customer provides the code and AWS manages the underlying platform?

A. Infrastructure as a Service (IaaS)
B. Platform as a Service (PaaS)
C. Software as a Service (SaaS)
D. Function as a Service (FaaS)

**Câu 4:** A company keeps sensitive data in its own on-premises data center while running its web application on AWS, with connectivity between the two environments. Which deployment model is this?

A. Public Cloud
B. Private Cloud
C. Hybrid Cloud
D. Community Cloud

**Câu 5:** Which of the following is a benefit of Cloud Computing that means a system can automatically increase and decrease resources based on current demand?

A. Elasticity
B. Durability
C. Encryption
D. Federation

## Đáp án quiz

**Câu 1 — B.** Nhiều Availability Zone trong cùng một Region là thiết kế chuẩn cho High Availability. Mỗi AZ độc lập về điện, mạng, vị trí vật lý nên một AZ sập thì AZ khác vẫn chạy. Dùng nhiều Region là cho Disaster Recovery xuyên khu vực, phức tạp hơn mức cần thiết trong câu này. Edge Location là cho CloudFront, không chạy workload chính.

**Câu 2 — B.** Trên EC2 (IaaS), khách hàng chịu trách nhiệm patch Guest OS, cấu hình firewall, quản lý dữ liệu. AWS lo phần A, C, D — đó là Security OF the Cloud: bảo mật vật lý, phần cứng, ảo hóa.

**Câu 3 — B.** Elastic Beanstalk là ví dụ kinh điển của PaaS trong đề thi AWS: bạn đưa code, AWS lo provision server, OS, load balancer. EC2 mới là IaaS. Gmail là SaaS.

**Câu 4 — C.** Hybrid Cloud = kết hợp on-premises (private) + public cloud và có kết nối giữa hai bên. Đây là mô hình migrate phổ biến của doanh nghiệp lớn.

**Câu 5 — A.** Elasticity là định nghĩa sách giáo khoa: tự động tăng/giảm tài nguyên theo nhu cầu thực tế. Đây là keyword phải thuộc lòng, đề thi sẽ dùng đúng từ này trong cả câu hỏi lẫn đáp án.
