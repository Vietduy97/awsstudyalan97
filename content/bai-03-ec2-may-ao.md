# Bài 03 — EC2: Máy ảo trên AWS

## Mục tiêu bài học
- Hiểu Amazon EC2 là gì: máy ảo thuê theo giờ/giây trên AWS
- Biết AMI là gì và cách chọn AMI khi tạo instance
- Nhận diện các họ Instance Type ở mức khái niệm: general, compute, memory, storage optimized
- Nắm 5 mô hình giá: On-Demand, Reserved Instances, Savings Plans, Spot, Dedicated Hosts
- Biết Placement Groups: Cluster, Spread, Partition
- Hiểu Key Pair, Security Group ở mức giới thiệu, User Data và Instance Metadata
- Phân biệt EBS-backed và Instance Store ở mức giới thiệu
- Phân biệt các trạng thái: stop, terminate, hibernate

## Lý thuyết chính

### 1. EC2 là gì?

**Amazon Elastic Compute Cloud (EC2)** là dịch vụ cho thuê máy ảo (Virtual Machine) trên AWS — dịch vụ IaaS kinh điển nhất. Bạn chọn hệ điều hành, CPU, RAM, ổ đĩa, bấm Launch và vài phút sau có một server để SSH/RDP vào, giống hệt một máy tính thật nhưng nằm trong data center của AWS.

EC2 là nền móng của SAA-C03: rất nhiều scenario bắt đầu bằng "một ứng dụng chạy trên EC2..." rồi hỏi cách làm nó highly available, scalable hoặc rẻ hơn.

Khi tạo một EC2 instance, bạn phải quyết định những thứ sau:

### 2. AMI — Amazon Machine Image

**AMI** là bản mẫu (template) để tạo instance, chứa: hệ điều hành (Amazon Linux 2023, Ubuntu, Windows...), phần mềm cài sẵn, cấu hình. Chọn AMI là chọn "khởi đầu" của máy ảo.

Có AMI do AWS cung cấp, do cộng đồng (Community AMI), do Marketplace bán, và AMI bạn tự tạo từ instance của mình (để clone ra nhiều máy giống hệt). Đề thi hay cho tình huống "cần nhiều instance cấu hình giống nhau" — đáp án là tạo **custom AMI** từ instance mẫu rồi launch hàng loạt từ AMI đó.

### 3. Instance Types — các họ máy

Instance Type có dạng `họ.size`, ví dụ `t3.micro`, `m5.large`, `c6g.xlarge`. Số/x2large/xlarge càng lớn thì CPU/RAM càng nhiều và càng đắt. Chỉ cần nhớ **ý nghĩa của họ** ở mức khái niệm:

- **General Purpose (họ M, T):** Cân bằng CPU/RAM, dùng cho web server, app server thông thường. Họ **T** là burstable — rẻ, tích lũy CPU credits, hợp workload lúc ít lúc nhiều. `t2.micro / t3.micro` là instance quen thuộc nhất của người học.
- **Compute Optimized (họ C):** Mạnh về CPU, cho batch processing, tính toán khoa học, game server, encoding video.
- **Memory Optimized (họ R, X):** Mạnh về RAM, cho in-memory database, cache, xử lý dữ liệu lớn trong RAM.
- **Storage Optimized (họ I, D):** Mạnh về ổ đĩa tốc độ cao/dung lượng lớn tại chỗ, cho database cần IOPS cao, data warehouse.
- **Accelerated Computing (họ P, G):** Có GPU, cho machine learning và đồ họa — chỉ cần biết khái niệm ở bậc Associate.

Keyword đề thi: thấy chữ "memory-intensive" thì nghĩ họ R, thấy "compute-intensive / high CPU" thì nghĩ họ C, thấy "balanced" thì nghĩ họ M/T.

### 4. Pricing Models — 5 cách trả tiền EC2

Đây là phần chắc chắn có câu hỏi trong domain Cost-Optimized 20%:

- **On-Demand:** Trả theo giờ/giây, không cam kết, linh hoạt nhất, đắt nhất trong các lựa chọn dài hạn. Hợp cho workload ngắn hạn, không đoán trước, mới thử nghiệm. Đặc điểm: không trả trước, tắt là hết tiền compute.
- **Reserved Instances (RI):** Cam kết dùng **1 năm hoặc 3 năm** với một Instance Type/Region cụ thể (hoặc linh hoạt hơn tùy loại) để được giảm giá lớn so với On-Demand. Hợp cho workload ổn định, chạy 24/7 như database server. Có Standard RI (giảm sâu hơn, ít linh hoạt) và Convertible RI (đổi được instance family, giảm ít hơn).
- **Savings Plans:** Cam kết mức chi tiêu theo giờ (ví dụ $10/giờ) trong 1 hoặc 3 năm, AWS tự áp dụng giảm giá linh hoạt qua nhiều instance family và cả Lambda/Fargate (với Compute Savings Plans). Đây là lựa chọn **linh hoạt hơn RI** và là hướng AWS khuyến nghị hiện nay. Phân biệt cốt lõi hay thi: RI khóa vào instance type/Region cụ thể hơn, Savings Plans khóa vào **mức tiền cam kết** và linh hoạt hơn.
- **Spot Instances:** Đấu giá năng lực EC2 đang dư thừa của AWS với giá giảm rất sâu so với On-Demand, đổi lại **AWS có thể thu hồi instance với cảnh báo 2 phút** khi họ cần lại năng lực. Chỉ hợp cho workload chịu được gián đoạn: batch job, xử lý ảnh/video, CI/CD, big data. **Không bao giờ dùng Spot cho database hay hệ thống không được phép sập giữa chừng.**
- **Dedicated Hosts:** Thuê nguyên một máy chủ vật lý, không chia sẻ với khách hàng khác. Đắt nhất, dùng khi cần tuân thủ license phần mềm tính theo physical core/socket, hoặc yêu cầu compliance đặc biệt. Phân biệt với **Dedicated Instances**: Dedicated Instances cũng chạy trên phần cứng tách riêng cho bạn nhưng bạn không kiểm soát/không thấy được host cụ thể như Dedicated Hosts.

### 5. Placement Groups — cách bố trí instance trong AZ

Placement Group là cách bạn bảo AWS sắp xếp các instance vật lý gần hay xa nhau trong một AZ:

- **Cluster Placement Group:** Đặt các instance **rất gần nhau** trong cùng một AZ để đạt network latency thấp nhất, băng thông cao nhất. Dùng cho HPC (High Performance Computing), ứng dụng cần các node nói chuyện với nhau cực nhanh. Đánh đổi: cùng AZ nên rủi ro cùng lúc cao hơn.
- **Spread Placement Group:** Đặt các instance **trên các phần cứng khác nhau, tách xa nhau** để giảm rủi ro sập cùng lúc. Tối đa 7 instance cho mỗi AZ trong một Spread Group. Dùng cho ứng dụng quan trọng có ít instance, mỗi instance phải độc lập.
- **Partition Placement Group:** Chia instance thành các partition logic, mỗi partition có rack phần cứng riêng, các partition không dùng chung rack. Dùng cho hệ thống phân tán lớn như Hadoop, Cassandra, Kafka — khi một partition lỗi, các partition khác vẫn sống.

Mẹo nhớ: Cluster = gom lại cho nhanh, Spread = rải ra cho an toàn số lượng ít, Partition = chia ô cho hệ thống phân tán lớn.

### 6. Key Pair và Security Group (giới thiệu)

- **Key Pair:** Cặp khóa để đăng nhập instance. AWS giữ public key, bạn tải private key (file `.pem` cho Linux, dùng cho SSH; Windows dùng nó để giải mã password RDP) **một lần duy nhất** khi tạo. Mất private key là mất cách vào instance theo đường chuẩn. Lưu file `.pem` như lưu chìa khóa nhà — tuyệt đối không up lên GitHub.
- **Security Group:** Firewall ảo ở tầng instance, quản lý traffic vào/ra (inbound/outbound). Security Group là **stateful**: đã cho traffic vào thì traffic trả lời tự động được cho ra. Mặc định inbound bị chặn hết, outbound cho phép hết. Chi tiết Security Group vs Network ACL sẽ học sâu ở bài Network — ở bài này chỉ cần nhớ Security Group là "anh bảo vệ cổng" của từng instance.

### 7. User Data và Instance Metadata

- **User Data:** Đoạn script bạn đưa vào khi launch, instance sẽ **tự chạy một lần lúc khởi động lần đầu**. Dùng để tự cài web server, cập nhật OS, tải code — nền tảng của tự động hóa. Ví dụ kinh điển trong đề thi: User Data chứa script cài Apache và tạo trang web mẫu.
- **Instance Metadata:** Thông tin về chính instance đó, truy cập từ bên trong instance qua địa chỉ đặc biệt `169.254.169.254`. Ứng dụng chạy trong instance dùng nó để biết public IP, IAM Role tạm thời của mình, AZ đang ở... Đề thi hay hỏi cách instance lấy credentials của Role — chính là qua Instance Metadata (IMDS).

### 8. EBS-backed vs Instance Store (giới thiệu)

- **EBS-backed Instance:** Ổ đĩa gốc là **Amazon EBS** — ổ đĩa mạng bền vững, tách rời khỏi instance. Stop instance thì dữ liệu vẫn còn. Đây là lựa chọn mặc định và phổ biến nhất.
- **Instance Store:** Ổ đĩa vật lý gắn chết vào host chứa instance — tốc độ rất cao nhưng là **ephemeral storage**: instance stop/terminate hoặc host lỗi là **mất sạch dữ liệu**. Chỉ dùng làm cache, buffer, dữ liệu tạm tái tạo lại được.

Chi tiết về EBS volume types, snapshot, encryption sẽ học kỹ ở bài Storage (Bài 06). Ở bài này chỉ cần ghim: **EBS = bền, Instance Store = tạm và mất khi stop.**

### 9. Các trạng thái của instance

- **Stop:** Tắt máy. Hết tiền compute, **EBS vẫn tính tiền**, dữ liệu EBS còn nguyên, dữ liệu Instance Store mất. Instance có thể start lại, thường sẽ sang host vật lý khác và đổi public IP (trừ khi có Elastic IP).
- **Start:** Bật lại instance đã stop.
- **Reboot:** Khởi động lại OS, giống bấm nút restart — instance vẫn ở nguyên host, không mất dữ liệu Instance Store.
- **Hibernate:** "Ngủ đông" — nội dung RAM được lưu xuống EBS, lần start sau instance khôi phục đúng trạng thái đang chạy dở (các ứng dụng đang mở vẫn nguyên). Cần instance hỗ trợ và EBS root được mã hóa, RAM có giới hạn. Khác với Stop ở chỗ Stop là tắt hẳn, bật lại như mở máy mới.
- **Terminate:** Xóa sổ instance. Không khôi phục được. Root EBS mặc định xóa theo, cần kiểm tra các tài nguyên kèm theo như đã học ở Bài 02.

## Ví dụ đời thường

**EC2 giống như thuê xe máy / ô tô ở Việt Nam theo nhu cầu.**

- **On-Demand** là thuê xe theo ngày ở tiệm đầu ngõ: cần thì thuê, trả theo ngày, không ràng buộc, giá niêm yết cao nhất nhưng tự do nhất.
- **Reserved Instance** là ký hợp đồng thuê xe dài hạn 1–3 năm cho nhân viên giao hàng chạy cố định mỗi ngày: giá rẻ hơn hẳn vì bạn cam kết thuê lâu — nhưng cam kết rồi thì xe đó phải dùng, không dùng vẫn trả tiền.
- **Savings Plans** giống như cam kết với hãng "tháng nào tôi cũng thuê ít nhất 10 triệu tiền xe" — đổi lại hãng giảm giá cho mọi loại xe bạn thuê, linh hoạt hơn việc khóa chết vào một mẫu xe như RI.
- **Spot Instance** là xe đang trống của hãng được cho thuê giá rẻ bất ngờ, với điều kiện: khi có khách VIP cần xe, hãng lấy lại xe sau khi báo trước 2 phút. Chỉ hợp cho chuyến đi mà bị hủy giữa chừng cũng không sao — như chở vật liệu xây dựng chia nhiều chuyến nhỏ, tuyệt đối không dùng để chở bệnh nhân đi cấp cứu (database).
- **AMI** là bản thiết kế quán phở mẫu: nấu chuẩn một quán rồi photocopy bản thiết kế để mở 20 quán giống hệt nhau khắp thành phố.
- **User Data** là tờ giấy dặn nhân viên ca sáng: "Vừa mở cửa là bật bếp, treo biển, bật nhạc" — instance vừa khởi động là tự làm theo, không cần ai đứng nhắc.

## Phân biệt dễ nhầm

| Cặp dễ nhầm | Cách phân biệt |
|---|---|
| Reserved Instances vs Savings Plans | RI cam kết theo instance type/Region cụ thể. Savings Plans cam kết theo số tiền/giờ, linh hoạt nhiều family/dịch vụ hơn |
| Spot vs On-Demand | Spot rẻ sâu nhưng bị thu hồi với cảnh báo 2 phút. On-Demand giá chuẩn nhưng không ai lấy lại máy của bạn |
| Dedicated Hosts vs Dedicated Instances | Dedicated Hosts thuê nguyên server vật lý và thấy/kiểm soát được host — cần cho license theo socket/core. Dedicated Instances tách phần cứng nhưng không kiểm soát host ở mức đó |
| Stop vs Hibernate | Stop tắt hẳn, bật lại như máy mới. Hibernate lưu cả RAM xuống EBS, bật lại tiếp tục đúng trạng thái đang dở |
| EBS-backed vs Instance Store | EBS bền, sống sót qua stop. Instance Store nhanh nhưng ephemeral — stop/terminate là mất dữ liệu |
| Cluster vs Spread Placement Group | Cluster gom instance gần nhau để latency thấp nhất. Spread rải instance ra phần cứng khác nhau để giảm rủi ro |
| Security Group vs Key Pair | Key Pair để đăng nhập (bạn là ai). Security Group là firewall chặn/cho traffic (ai được nói chuyện với instance) |

## Bẫy đề thi

- Đề cho workload "batch processing có thể chạy lại khi bị gián đoạn, cần rẻ nhất": đáp án là **Spot Instances**. Đề cho workload "database production không được sập": Spot là đáp án **sai**.
- Đề hỏi giảm giá cho workload ổn định chạy 24/7 trong 3 năm: nghĩ tới **Reserved Instances hoặc Savings Plans**. Nếu đề nhấn mạnh "linh hoạt đổi instance family" thì Savings Plans thắng.
- Đề hỏi license phần mềm tính theo physical cores và cần biết chính xác host: đáp án là **Dedicated Hosts**, không phải Dedicated Instances.
- Đề hỏi ứng dụng cần các node giao tiếp với latency thấp nhất có thể: **Cluster Placement Group**. Ứng dụng quan trọng, ít instance, cần tách biệt lỗi: **Spread**. Hadoop/Kafka quy mô lớn: **Partition**.
- User Data chỉ chạy khi **launch lần đầu** (mặc định). Đừng chọn đáp án "dùng User Data để sửa cấu hình mỗi lần reboot".
- Mất private key `.pem` — không có chuyện AWS gửi lại file đó cho bạn. Đây là lỗi người dùng, không phải lỗi AWS.
- Hibernate không phải instance nào cũng dùng được và có yêu cầu về EBS root mã hóa — đừng mặc định mọi instance đều hibernate được.

## Tóm tắt 5 dòng
EC2 là máy ảo thuê trên AWS, tạo từ AMI (bản mẫu OS + phần mềm) với Instance Type thuộc các họ general/compute/memory/storage tùy đặc tính workload.
Về giá: On-Demand linh hoạt không cam kết, Reserved Instances và Savings Plans giảm giá khi cam kết 1–3 năm, Spot rẻ nhất nhưng bị thu hồi sau cảnh báo 2 phút, Dedicated Hosts thuê nguyên máy vật lý cho nhu cầu license/compliance.
Placement Group gồm Cluster (gom gần, latency thấp), Spread (rải ra, tối đa 7 instance/AZ) và Partition (chia ô cho hệ thống phân tán lớn như Hadoop/Kafka).
Key Pair để đăng nhập, Security Group là firewall stateful của instance, User Data là script tự chạy lúc launch, Instance Metadata ở 169.254.169.254 cho instance tự biết thông tin về chính nó.
EBS-backed thì dữ liệu bền qua stop, Instance Store là ephemeral sẽ mất dữ liệu khi stop/terminate, và Hibernate khác Stop ở chỗ nó lưu cả trạng thái RAM để khôi phục nguyên vẹn.

## Quiz

**Câu 1:** A company runs a batch image-processing job that can be interrupted and restarted without data loss. The company wants the LOWEST possible cost for the EC2 compute capacity. Which purchasing option should they choose?

A. On-Demand Instances
B. Reserved Instances
C. Spot Instances
D. Dedicated Hosts

**Câu 2:** A company needs to deploy a small number of critical instances so that no two instances share the same underlying hardware, reducing the risk of simultaneous failure. Which placement group type should they use?

A. Cluster placement group
B. Spread placement group
C. Partition placement group
D. Auto Scaling group

**Câu 3:** An application requires high CPU performance for scientific simulations. Which EC2 instance family is MOST appropriate?

A. Memory optimized (R family)
B. Storage optimized (I family)
C. Compute optimized (C family)
D. General purpose burstable (T family)

**Câu 4:** What happens to data stored on an Instance Store volume when an EC2 instance is stopped?

A. The data is automatically backed up to Amazon S3
B. The data is preserved on the EBS root volume
C. The data is lost because Instance Store is ephemeral storage
D. The data is encrypted and retained for 30 days

**Câu 5:** A company has a stable workload that runs 24/7 and wants a pricing commitment based on a consistent hourly spend that can be applied flexibly across instance families. Which option is MOST suitable?

A. Spot Instances
B. Compute Savings Plans
C. On-Demand Instances
D. Dedicated Hosts

## Đáp án quiz

**Câu 1 — C.** Spot Instances là đáp án kinh điển cho workload chịu được gián đoạn và cần rẻ nhất. Đề đã cố tình cho dữ kiện "can be interrupted and restarted" — đó là dấu hiệu nhận diện Spot. On-Demand đắt hơn, RI là cam kết dài hạn không liên quan, Dedicated Hosts đắt nhất.

**Câu 2 — B.** Spread Placement Group rải từng instance lên phần cứng riêng biệt khác nhau, tối đa 7 instance mỗi AZ trong một group — đúng với yêu cầu "số lượng ít, quan trọng, không chia sẻ phần cứng". Cluster làm ngược lại (gom gần nhau), Partition dành cho hệ thống phân tán lớn.

**Câu 3 — C.** "High CPU performance" là keyword của Compute Optimized — họ C. Họ R là nhiều RAM, họ I là storage, họ T là burstable giá rẻ cho workload thông thường.

**Câu 4 — C.** Instance Store là ephemeral storage: dữ liệu mất khi instance stop, terminate hoặc host gặp sự cố. Muốn dữ liệu bền phải dùng EBS. Đây là câu phân biệt EBS vs Instance Store kinh điển nhất.

**Câu 5 — B.** Savings Plans cam kết theo mức chi tiêu theo giờ và áp dụng linh hoạt qua nhiều instance family. RI cũng giảm giá nhưng khóa chặt hơn vào instance type/Region. Đề nhấn mạnh chữ "flexibly across instance families" là cố ý chỉ về Savings Plans.
