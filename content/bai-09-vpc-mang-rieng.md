# Bài 09 — VPC: Mạng Riêng Trên AWS

## Mục tiêu bài học

- Hiểu VPC là gì và vì sao mọi EC2, RDS, Lambda cần sống trong một VPC.
- Phân biệt được Public Subnet và Private Subnet, biết đọc Route Table.
- Nắm chắc cặp phân biệt kinh điển của đề thi: Security Group vs Network ACL.
- Biết khi nào dùng NAT Gateway, VPC Endpoint, VPC Peering, Transit Gateway.
- Biết dùng VPC Flow Logs và Bastion Host đúng chỗ.

## Lý thuyết chính (tiếng Việt, giữ thuật ngữ English)

### 1. VPC và CIDR Block

**Virtual Private Cloud (VPC)** là mạng riêng ảo của riêng bạn trên AWS. Bạn tự định nghĩa dải IP, chia subnet, đặt rule truy cập — giống như bạn tự kéo cáp mạng trong data center của mình, chỉ khác là nó nằm trên cloud.

Khi tạo VPC, bạn phải chọn một **CIDR Block**, ví dụ `10.0.0.0/16`. Đây là dải IP private cho toàn bộ VPC. Mọi tài nguyên trong VPC sẽ lấy IP từ dải này. Chọn CIDR rồi rất khó đổi, nên hãy chọn rộng vừa đủ ngay từ đầu.

Một VPC nằm trong một **Region** nhưng có thể trải dài qua nhiều **Availability Zone (AZ)**.

### 2. Subnet — Public vs Private

**Subnet** là một đoạn nhỏ của VPC, gắn với một AZ cụ thể.

- **Public Subnet:** có route trong Route Table trỏ ra **Internet Gateway (IGW)**. Tài nguyên trong public subnet (có Public IP) giao tiếp hai chiều được với internet. Ví dụ: ALB, Bastion Host, NAT Gateway.
- **Private Subnet:** KHÔNG có route ra IGW. Tài nguyên trong đây không truy cập trực tiếp được từ internet, và internet cũng không vào trực tiếp được. Ví dụ: EC2 chạy app thật, RDS database.

Lưu ý quan trọng cho đề thi: subnet là public hay private không phải do cái tên, mà do **Route Table** của nó có route `0.0.0.0/0 -> IGW` hay không.

### 3. Route Table

**Route Table** là bảng chỉ đường cho một subnet: gói tin đi tới dải IP nào thì rẽ sang đâu.

Mỗi subnet gắn với đúng một Route Table. Route tới dải IP của chính VPC luôn có sẵn và gọi là **local route** — không xóa được.

Ví dụ đọc bảng:

- `10.0.0.0/16 -> local`: đi trong VPC thì đi thẳng.
- `0.0.0.0/0 -> igw-xxxx`: còn lại, ra internet qua IGW.
- `0.0.0.0/0 -> nat-xxxx`: còn lại, ra internet qua NAT Gateway.

### 4. NAT Gateway

**NAT Gateway** đặt ở **Public Subnet**, cho phép tài nguyên trong **Private Subnet** chủ động ra internet (để tải patch, gọi API bên ngoài) nhưng internet KHÔNG chủ động vào lại được — tức là kết nối **một chiều ra**.

Bẫy chi phí kinh điển: NAT Gateway **tốn phí theo giờ + phí theo GB dữ liệu xử lý**. Nếu đề cho tình huống "private instance tải dữ liệu rất lớn từ S3, hóa đơn NAT tăng vọt" thì đáp án thường là dùng **VPC Endpoint** cho S3 thay vì đi qua NAT.

NAT Gateway là dịch vụ managed, có tính sẵn sàng cao trong một AZ. Muốn HA nhiều AZ thì mỗi AZ đặt một NAT Gateway riêng.

### 5. Security Group

**Security Group (SG)** là tường lửa ảo gắn vào **instance / ENI (Elastic Network Interface)**.

- **Stateful:** nếu bạn cho phép traffic vào, traffic trả lời đi ra sẽ tự động được phép, và ngược lại. Bạn không cần viết rule cho chiều trả lời.
- Chỉ có rule **Allow**, KHÔNG có rule Deny. Không ghi gì = mặc định chặn.
- Đánh giá **tất cả** các rule cùng lúc để quyết định.
- Rule có thể tham chiếu tới một Security Group khác — rất hay dùng: cho SG của app tham chiếu SG của ALB, thay vì mở IP lung tung.

### 6. Network ACL (NACL)

**Network Access Control List (NACL)** là tường lửa gắn vào **Subnet**.

- **Stateless:** traffic vào và traffic trả lời đi ra là hai chuyện riêng. Bạn phải mở rule cho cả hai chiều, kể cả các cổng trả lời tạm thời (ephemeral ports).
- Có cả rule **Allow** và **Deny**.
- Rule được đánh số — **Rule Number**. Rule có số **thấp hơn được xét trước** và thắng trước. Vừa khớp rule nào là dừng, không xét tiếp.
- Một subnet chỉ gắn với một NACL, nhưng một NACL có thể gắn cho nhiều subnet.

### 7. VPC Endpoints

Mặc định, từ VPC đi tới các dịch vụ AWS như S3, DynamoDB vẫn có thể phải vòng ra internet. **VPC Endpoint** tạo đường riêng trong mạng AWS, không ra internet công cộng.

- **Gateway Endpoint:** chỉ hỗ trợ **S3 và DynamoDB**, **miễn phí**, thực chất là thêm một route vào Route Table.
- **Interface Endpoint (AWS PrivateLink):** hỗ trợ hầu hết các dịch vụ AWS khác, tạo một ENI có Private IP trong subnet của bạn. **Có phí** theo giờ + theo GB.

Đề hỏi "private subnet truy cập S3 mà không qua internet, rẻ nhất" -> Gateway Endpoint.

### 8. Kết nối các VPC: Peering vs Transit Gateway

- **VPC Peering:** kết nối 1-1 giữa hai VPC. **Không có tính transitive** — A peer với B, B peer với C thì A vẫn KHÔNG đi tới C qua B được. CIDR của hai VPC peer không được trùng nhau.
- **Transit Gateway:** là một **hub** trung tâm. Nhiều VPC và cả mạng on-premises cùng nối vào hub này. **Có transitive** — mọi spoke nói chuyện được với nhau qua hub. Đề cho "hàng chục VPC cần kết nối với nhau" thì chọn Transit Gateway.

### 9. VPC Flow Logs

**VPC Flow Logs** ghi lại thông tin về traffic IP đi vào/ra các network interface trong VPC: IP nguồn/đích, port, protocol, ACCEPT hay REJECT. Gửi log về CloudWatch Logs hoặc S3 để điều tra sự cố mạng và bảo mật. Flow Logs không ghi nội dung gói tin, chỉ ghi metadata.

### 10. Bastion Host

**Bastion Host** (hay Jump Box) là một EC2 nhỏ đặt ở Public Subnet, là cửa duy nhất để quản trị viên SSH/RDP vào, rồi từ đó mới nhảy tiếp vào các instance trong Private Subnet. Không bao giờ mở SSH trực tiếp cho private instance ra internet.

## Ví dụ đời thường

Hãy tưởng tượng VPC là một khu chung cư có cổng bảo vệ là của riêng bạn.

- **CIDR Block** là toàn bộ địa chỉ của khu: từ số nhà 10.0.0.1 tới 10.0.255.255.
- **Public Subnet** là dãy nhà mặt tiền, mở cửa ra đường lớn (Internet Gateway) — ai đi qua cũng nhìn thấy: đó là sảnh lễ tân, quán cà phê (ALB, Bastion).
- **Private Subnet** là dãy nhà phía trong, không có cửa ra đường. Người ngoài không tự vào được. Cư dân bên trong (EC2, RDS chứa dữ liệu quý) sống yên tĩnh ở đây.
- **NAT Gateway** giống anh bảo vệ chạy việc vặt: người ở trong nhờ anh ra ngoài mua đồ (tải bản vá) thì được, nhưng người lạ ngoài đường không nhờ anh dẫn vào nhà được.
- **Security Group** là khóa thông minh gắn trên từng căn hộ, nhớ ai đã được cho vào thì tự mở cửa cho họ ra — đó là stateful.
- **NACL** là chốt kiểm soát ở cổng từng dãy nhà: kiểm tra cả lượt vào lẫn lượt ra, có danh sách cấm rõ ràng, ai mang số thứ tự (Rule Number) nhỏ hơn thì được xét trước.
- **VPC Endpoint** là đường hầm nội bộ từ khu chung cư đi thẳng tới siêu thị S3 mà không cần ra đường lớn.
- **Bastion Host** là phòng bảo vệ: bạn phải trình giấy ở đây trước, rồi mới được dẫn vào trong.

## Phân biệt dễ nhầm

### Security Group vs Network ACL — Cặp phân biệt quan trọng nhất bài này

| Tiêu chí | Security Group | Network ACL |
|---|---|---|
| Gắn vào | Instance / ENI | Subnet |
| Stateful / Stateless | Stateful | Stateless |
| Loại rule | Chỉ Allow | Allow + Deny |
| Thứ tự xét rule | Xét tất cả rule | Theo Rule Number, số thấp thắng trước |
| Phạm vi ảnh hưởng | Chỉ tài nguyên được gắn | Mọi tài nguyên trong subnet |

Nhớ mẹo: **SG = Stateful, gắn Instance. NACL = Stateless, gắn Subnet.** Thấy chữ "Deny một dải IP cụ thể" trong đề -> chỉ NACL làm được, SG không có Deny.

### Gateway Endpoint vs Interface Endpoint

- Gateway Endpoint: chỉ S3 + DynamoDB, miễn phí, là route trong Route Table.
- Interface Endpoint: nhiều dịch vụ, qua PrivateLink, có ENI + Private IP, có phí.

### VPC Peering vs Transit Gateway

- Peering: 1-1, không transitive, nhiều VPC sẽ thành mớ bòng bong.
- Transit Gateway: mô hình hub-and-spoke, có transitive, quản lý tập trung.

### Public Subnet vs Private Subnet

Khác nhau ở Route Table: có route ra IGW là public, không có là private. Đặt tên "private" mà gắn route ra IGW thì nó vẫn là public.

## Bẫy đề thi

1. **"Block một IP xấu cụ thể"** — Đừng chọn Security Group. SG không có Deny. Phải dùng NACL với rule Deny.
2. **Quên ephemeral ports với NACL** — Vì NACL stateless, mở port 443 vào mà quên mở port trả lời đi ra là traffic vẫn chết. SG thì không gặp lỗi này vì stateful.
3. **NAT Gateway tốn tiền** — Đề kể chi phí NAT tăng bất thường khi tải nhiều từ S3/DynamoDB: đáp án là Gateway VPC Endpoint (miễn phí).
4. **Peering không transitive** — A-B, B-C không suy ra A-C. Cần A nói chuyện với C thì peer trực tiếp A-C hoặc dùng Transit Gateway.
5. **NAT Gateway phải đặt ở Public Subnet** — Đặt NAT vào private subnet là sai kiến trúc kinh điển trong các phương án nhiễu.
6. **Gateway Endpoint chỉ có 2 dịch vụ** — Thấy SQS, SNS, KMS mà chọn Gateway Endpoint là sai, phải là Interface Endpoint.

## Tóm tắt 5 dòng

VPC là mạng riêng của bạn trên AWS, chia thành Public Subnet (có route ra Internet Gateway) và Private Subnet (không có).
NAT Gateway đặt ở Public Subnet cho Private Subnet ra internet một chiều, nhưng tốn phí theo giờ và theo GB.
Security Group stateful, chỉ Allow, gắn vào instance; NACL stateless, có Allow + Deny, gắn vào subnet, Rule Number thấp thắng trước.
Gateway Endpoint miễn phí chỉ cho S3 và DynamoDB, Interface Endpoint qua PrivateLink có phí cho các dịch vụ khác.
VPC Peering không transitive, Transit Gateway là hub có transitive; Flow Logs ghi metadata traffic, Bastion Host là cửa SSH/RDP duy nhất vào vùng private.

## Quiz — 5 câu hỏi tiếng Anh kiểu đề thi (A/B/C/D)

**Question 1:** A security team must explicitly block all traffic from a specific malicious IP address range to instances in a subnet. Which AWS feature should they use?

A. Security Group with a deny rule
B. Network ACL with a deny rule
C. Route Table with a blackhole route to the internet gateway
D. VPC Flow Logs with an alarm

**Question 2:** Instances in a private subnet download large amounts of data from Amazon S3 every day. The NAT Gateway data processing charges have become very high. What is the MOST cost-effective solution?

A. Move the instances to a public subnet
B. Add a second NAT Gateway in another Availability Zone
C. Create a Gateway VPC Endpoint for Amazon S3
D. Create an Interface VPC Endpoint for Amazon S3

**Question 3:** VPC A is peered with VPC B, and VPC B is peered with VPC C. An application in VPC A needs to communicate with a database in VPC C. What should the architect do?

A. Nothing, VPC peering is transitive by default
B. Update the Security Group in VPC B to allow forwarding
C. Create a direct VPC peering connection between VPC A and VPC C, or use a Transit Gateway
D. Add the CIDR of VPC C to the Network ACL of VPC B

**Question 4:** Which statement about Security Groups is correct?

A. They are stateless and require rules for return traffic
B. They support both allow and deny rules
C. They are stateful, and return traffic is automatically allowed
D. They are evaluated in order of rule number, lowest first

**Question 5:** A company has 30 VPCs that all need to communicate with each other and with an on-premises network through a central hub. Which service is the BEST choice?

A. VPC Peering between every pair of VPCs
B. NAT Gateway
C. AWS Transit Gateway
D. Internet Gateway

## Đáp án quiz

**Câu 1 — Đáp án B.**
Giải thích tiếng Việt: Chỉ Network ACL mới có rule **Deny** rõ ràng. Security Group chỉ có Allow nên phương án A tự nó đã sai về mặt kỹ thuật. Flow Logs chỉ ghi log, không chặn traffic.

**Câu 2 — Đáp án C.**
Giải thích tiếng Việt: S3 thuộc 2 dịch vụ được Gateway Endpoint hỗ trợ và Gateway Endpoint miễn phí. Traffic đi S3 qua endpoint sẽ không còn đi qua NAT Gateway nữa nên cắt được phí xử lý dữ liệu. Interface Endpoint cũng đi được tới S3 nhưng có phí, không tối ưu chi phí bằng Gateway Endpoint.

**Câu 3 — Đáp án C.**
Giải thích tiếng Việt: VPC Peering **không transitive** — A không đi nhờ B để tới C được. Muốn A nói chuyện với C phải peer trực tiếp A-C hoặc đưa cả ba VPC vào Transit Gateway làm hub.

**Câu 4 — Đáp án C.**
Giải thích tiếng Việt: Security Group là **stateful**: cho phép chiều vào thì chiều trả lời tự động được phép. Các mô tả stateless, có Deny, xét theo Rule Number đều là đặc điểm của NACL, đề cố tình trộn sang.

**Câu 5 — Đáp án C.**
Giải thích tiếng Việt: Số lượng VPC lớn + cần kết nối tập trung + cần transitive là dấu hiệu nhận diện của **Transit Gateway** (mô hình hub-and-spoke). Peering từng cặp với 30 VPC sẽ tạo ra hàng trăm kết nối, rất khó quản lý và vẫn không transitive.
