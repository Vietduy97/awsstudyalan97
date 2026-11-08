# Bài 13 — ELB & Auto Scaling Group: High Availability và Co giãn

## Mục tiêu bài học

Sau bài này, bạn sẽ có thể:

- Phân biệt chính xác ALB, NLB, GWLB, CLB theo OSI Layer, use case và tính năng, chọn đúng Load Balancer trong mọi scenario đề thi.
- Giải thích Health Check, Cross-Zone Load Balancing, Sticky Sessions, Deregistration Delay và áp dụng vào kiến trúc thực tế.
- Thiết kế Auto Scaling Group (ASG) với Launch Template, Min/Desired/Max Capacity trải nhiều Availability Zone (AZ).
- Chọn đúng Scaling Policy: Target Tracking, Step Scaling, Simple Scaling, Scheduled Scaling cho từng tình huống tải.
- Nhận diện mẫu kiến trúc kinh điển của SAA-C03: **ALB + ASG + Multi-AZ** cho Resilient Architectures (26%) và High-Performing Architectures (24%).

## Lý thuyết chính

### 1. Elastic Load Balancing (ELB) — Họ nhà Load Balancer

Load Balancer là điểm vào (entry point) duy nhất, phân phối traffic đều tới nhiều target phía sau, tự loại bỏ target unhealthy. Đây là nền tảng của High Availability: một AZ/target chết, traffic vẫn sống.

| Loại | OSI Layer | Protocol | Đặc điểm chính | Dùng khi nào |
|------|-----------|----------|----------------|--------------|
| **ALB — Application Load Balancer** | Layer 7 | HTTP, HTTPS, WebSocket | Routing thông minh theo nội dung request | Web app, microservices, container |
| **NLB — Network Load Balancer** | Layer 4 | TCP, UDP, TLS | Hiệu năng cực cao, độ trễ cực thấp | Gaming, IoT, VoIP, TCP/UDP, cần static IP |
| **GWLB — Gateway Load Balancer** | Layer 3 | IP packet | Đưa traffic qua virtual appliance của bên thứ ba | Firewall, IDS/IPS, deep packet inspection tập trung |
| **CLB — Classic Load Balancer** | Layer 4/7 | HTTP/TCP cũ | Thế hệ cũ, ít tính năng | Chỉ gặp trong câu hỏi về hệ thống legacy, migration |

#### ALB — Application Load Balancer (Layer 7)

ALB hiểu HTTP nên nó ra quyết định routing dựa trên nội dung request:

- **Path-based Routing:** `/images/*` → Target Group chứa server xử lý ảnh, `/api/*` → Target Group API.
- **Host-based Routing:** `api.example.com` → một Target Group, `m.example.com` → Target Group khác, cùng dùng chung một ALB.
- **Query String / Header / HTTP Method / Source IP routing** cũng ở mức khái niệm.
- **Target Group:** nhóm logic các target (EC2, IP, Lambda, ECS/EKS task, ALB khác). Một ALB có nhiều Target Group, mỗi Listener Rule trỏ tới một Target Group.
- **Listener:** cổng ALB lắng nghe, ví dụ HTTPS:443, kèm certificate từ ACM.
- Hỗ trợ **WebSocket, HTTP/2**, redirect HTTP → HTTPS, fixed response, authentication qua Cognito / OIDC.

> **Tình huống thực tế:** Một sàn thương mại điện tử có web, API mobile, và service xử lý ảnh chạy trên các ECS service khác nhau nhưng dùng chung domain. Chỉ cần 1 ALB, dùng Host-based + Path-based Routing để tách traffic, tốn ít chi phí hơn nhiều so với dựng 3 Load Balancer riêng.

#### NLB — Network Load Balancer (Layer 4)

NLB không đọc HTTP, chỉ đọc TCP/UDP packet nên:

- Xử lý **hàng triệu request/giây**, độ trễ cực thấp (ultra-low latency).
- Mỗi AZ có **một static IP**, có thể gắn **Elastic IP** cho NLB — rất quan trọng khi đối tác yêu cầu whitelist IP cố định.
- Bảo toàn source IP của client tốt hơn cho backend.
- Hỗ trợ TLS termination ở mức Layer 4.

> **Tình huống thực tế:** Công ty game cần Load Balancer cho game server dùng TCP, hoặc hệ thống ngân hàng yêu cầu IP tĩnh để firewall đối tác whitelist. Đề thi cứ nhắc "static IP / Elastic IP / extreme performance / TCP/UDP / millions of requests per second" → đáp án là NLB.

#### GWLB — Gateway Load Balancer (Layer 3)

GWLB hoạt động ở Layer 3, dùng giao thức GENEVE để **chuyển toàn bộ traffic qua một fleet appliance bảo mật của bên thứ ba** (firewall, IDS/IPS, DPI) trước khi tới ứng dụng.

> **Tình huống thực tế:** Doanh nghiệp muốn mọi traffic vào VPC phải qua firewall tập trung của Palo Alto / Fortinet để kiểm tra, mà không muốn sửa routing phức tạp ở từng VPC. Đề thi nhắc "third-party virtual appliance, centralized inspection, firewall" → GWLB.

#### CLB — Classic Load Balancer

Thế hệ đầu tiên, không có Target Group, không có Path-based Routing. Trong đề thi hiện nay, CLB chỉ là đáp án nhiễu hoặc ngữ cảnh migration sang ALB/NLB. **Không chọn CLB cho kiến trúc mới.**

### 2. Các tính năng ELB phải nhớ cho đề thi

**Health Check:**
Load Balancer định kỳ ping target (ví dụ ALB gọi `GET /health` trên port traffic). Target trả 200 mới được nhận traffic, fail liên tục sẽ bị đánh dấu unhealthy và bị loại khỏi vòng quay. ASG cũng dùng ELB Health Check để tự thay EC2 unhealthy bằng instance mới.

**Cross-Zone Load Balancing:**
- Khi bật: traffic được phân phối đều tới **mọi target ở mọi AZ** mà Load Balancer bao phủ, dù số instance mỗi AZ không bằng nhau.
- Khi tắt: mỗi node Load Balancer chỉ chia đều cho AZ của nó, dễ gây mất cân bằng nếu AZ A có 2 instance, AZ B có 10 instance.
- ALB: mặc định bật, không tính phí thêm. NLB/GWLB: mặc định tắt, bật lên có thể phát sinh phí inter-AZ data transfer.

**Sticky Sessions (Session Affinity):**
- Chỉ ALB (và CLB cũ) hỗ trợ ở mức Load Balancer, dựa trên cookie (duration-based cookie do ALB tạo, hoặc application-based cookie).
- Giúp cùng một user luôn quay về cùng một target — cần khi app lưu session trong bộ nhớ local của server.
- Nhược điểm: gây mất cân bằng tải. Kiến trúc tốt hơn là externalize session ra ElastiCache / DynamoDB rồi tắt sticky. Đề thi thường bẫy: sticky không phải giải pháp HA chuẩn.

**Deregistration Delay (Connection Draining):**
- Khi một target bị deregister (bị ASG terminate, deploy mới), Load Balancer cho nó **hoàn thành nốt các request đang xử lý** thay vì cắt ngang.
- Giá trị **mặc định 300 giây**, cấu hình được từ 0–3600 giây.
- Đề thi hỏi "in-flight requests bị mất khi instance bị terminate / deploy" → tăng / kiểm tra Deregistration Delay.

**Các tính năng phụ hay hỏi:**
- **SSL/TLS Termination:** Load Balancer giải mã HTTPS, backend nhận HTTP trong VPC, giảm tải CPU cho EC2.
- **SNI (Server Name Indication):** ALB/NLB hỗ trợ nhiều certificate trên cùng một Listener cho nhiều domain.
- **Access Logs / Connection Logs** gửi về S3, **CloudWatch Metrics** để giám sát.

### 3. Auto Scaling Group (ASG)

ASG tự động duy trì số lượng EC2 đúng mong muốn và thay thế instance hỏng.

**Thành phần cốt lõi:**

- **Launch Template (khuyên dùng) / Launch Configuration (cũ):** bản mẫu EC2 — AMI, Instance Type, Key Pair, Security Group, IAM Role, User Data. Launch Template hỗ trợ versioning, nhiều instance type, Spot + On-Demand trộn (Mixed Instances Policy).
- **Min Size:** số instance tối thiểu luôn chạy — đảm bảo HA.
- **Desired Capacity:** số instance mong muốn hiện tại, ASG cố giữ đúng số này.
- **Max Size:** trần tối đa — chặn scale vô hạn để kiểm soát chi phí.
- **Subnet / AZ:** ASG phải trải **nhiều AZ** (chọn nhiều subnet ở các AZ khác nhau) → mất một AZ, ASG tự bù instance ở AZ còn lại.
- **Health Check Type:** EC2 (chỉ kiểm tra instance sống/chết) hoặc ELB (kiểm tra cả ứng dụng qua Load Balancer — chặt hơn, nên dùng khi gắn với ALB/NLB).
- **Termination Policy & Lifecycle Hooks** ở mức khái niệm: hook cho phép chạy script trước khi instance InService hoặc trước khi Terminated.

#### Scaling Policies — Chọn đúng loại

| Policy | Cách hoạt động | Khi nào dùng |
|--------|---------------|--------------|
| **Target Tracking Scaling** | Giữ một metric ở đúng giá trị mục tiêu, như giữ CPU trung bình = 50%, ALB RequestCountPerTarget = 1000 | **Mặc định nên khuyên dùng**, đơn giản như thermostat. Hầu hết scenario đề thi |
| **Step Scaling** | Tăng/giảm theo bậc tùy mức độ vượt ngưỡng, VD: CPU > 70% thêm 1, CPU > 90% thêm 3 | Traffic tăng đột biến, cần phản ứng mạnh yếu khác nhau theo mức alarm CloudWatch |
| **Simple Scaling** | Vượt ngưỡng thì cộng/trừ một lượng cố định, chờ Cooldown rồi mới scale tiếp | Hệ thống cũ, nhu cầu đơn giản. Dễ bị bẫy vì phản ứng chậm |
| **Scheduled Scaling** | Đặt lịch trước: 8h sáng tăng Desired lên 20, 22h giảm xuống 4 | Tải có chu kỳ đoán trước được: giờ hành chính, ngày sale cố định, batch job ban đêm |
| **Predictive Scaling** | Machine Learning dự báo tải từ lịch sử (nhắc ở mức khái niệm) | Tải có pattern lặp lại phức tạp |

**Cooldown Period:**
Sau một hoạt động scale-out/scale-in, ASG chờ một khoảng thời gian (mặc định 300 giây) trước khi scale tiếp, để metric kịp ổn định và tránh scale lên/xuống liên tục (flapping). Target Tracking và Step Scaling xử lý cooldown linh hoạt hơn Simple Scaling. Ở mức SAA, chỉ cần hiểu khái niệm và hệ quả: cooldown quá dài → phản ứng chậm khi traffic spike.

**ASG + Spot Instances:**
ASG có thể trộn On-Demand (cho baseline, đảm bảo HA) và Spot (cho phần tăng thêm, tiết kiệm chi phí) trong Mixed Instances Policy. Hợp với workload chịu được gián đoạn.

### 4. Mẫu kiến trúc kinh điển của đề thi

```
Users → Route 53 → ALB (Multi-AZ, public subnet)
                        ↓
                 Target Group
                        ↓
            ASG (private subnet, trải 3 AZ)
              Min=3  Desired=6  Max=20
                        ↓
              RDS Multi-AZ / ElastiCache
```

Vì sao mẫu này xuất hiện ở hầu hết câu hỏi Resilient / High-Performing?

1. **ALB** loại bỏ single point of failure ở tầng entry, tự bỏ target unhealthy.
2. **ASG Multi-AZ** tự thay instance hỏng, tự scale theo tải, mất 1 AZ vẫn sống.
3. **Target Tracking** giữ CPU/latency ổn định mà không cần vận hành thủ công.
4. Tách public subnet (chỉ ALB) và private subnet (EC2) tăng bảo mật.

> **Tình huống thực tế:** Trang tin tức bình thường chạy 4 EC2. Khi có tin nóng, traffic tăng 10 lần trong 15 phút. ASG với Target Tracking (CPU 50% + RequestCountPerTarget) tự scale lên 18 instance, tin qua đi tự scale-in xuống 4. Không ai phải dậy nửa đêm bật server, chi phí chỉ tăng đúng lúc cần.

## Ví dụ đời thường

Hãy hình dung một **quán trà sữa đông khách**:

- **Load Balancer** là anh quản lý đứng ở cửa. Khách tới, anh chỉ sang quầy nào đang vắng nhất. Quầy nào nhân viên ốm (fail Health Check) thì anh không chỉ khách vào nữa.
- **Cross-Zone Load Balancing** giống việc quản lý được quyền điều khách sang **mọi quầy trong mọi chi nhánh gần nhau**, thay vì mỗi chi nhánh tự xoay sở với lượng khách của mình.
- **Sticky Sessions** là khách quen luôn đòi đúng một bạn pha chế cũ vì bạn ấy nhớ khẩu vị đã ghi trên giấy để tại quầy — tiện nhưng nếu bạn ấy nghỉ thì khách bị kẹt. Tiệm chuyên nghiệp sẽ ghi khẩu vị vào sổ chung (ElastiCache) để quầy nào pha cũng được.
- **Deregistration Delay** là khi một quầy sắp đóng, quản lý không đuổi khách đang chờ lấy đồ, mà cho quầy làm xong hết ly đang dở rồi mới đóng.
- **ASG** là quy định ca trực: tối thiểu luôn có 3 quầy mở (Min), bình thường mở 6 quầy (Desired), đông nhất không mở quá 20 quầy (Max). Đông khách (CPU cao) thì gọi thêm nhân viên, vắng thì cho về bớt.
- **Target Tracking** như máy điều hòa đặt 25°C: nóng lên tự chạy mạnh, mát rồi tự yếu đi — bạn không cần bấm nút liên tục.

## Phân biệt dễ nhầm

**1. ALB vs NLB**
- ALB = Layer 7, hiểu HTTP, routing theo path/host. NLB = Layer 4, chỉ TCP/UDP, nhanh cực độ, có static IP / Elastic IP.
- Từ khóa phân biệt: "path-based routing" → ALB. "static IP, whitelist, TCP/UDP, gaming, extreme performance" → NLB.

**2. ALB vs GWLB**
- ALB phân phối tải tới app của bạn. GWLB không phục vụ app trực tiếp, nó **chuyển traffic qua appliance bảo mật bên thứ ba** để kiểm tra tập trung.

**3. Target Tracking vs Step Scaling vs Simple Scaling**
- Target Tracking: giữ metric ở **một giá trị mục tiêu** (giữ CPU 50%). Tự tính số instance cần thêm/bớt.
- Step Scaling: phản ứng **theo bậc** tùy mức alarm (vượt ít thêm ít, vượt nhiều thêm nhiều).
- Simple Scaling: vượt ngưỡng cộng **một lượng cố định** rồi chờ cooldown. Chậm và kém linh hoạt nhất trong ba loại.

**4. Sticky Sessions vs External Session Store**
- Sticky giữ user ở một server — giải pháp nhanh nhưng chống lại việc scale-in và HA.
- Lưu session ra ElastiCache/DynamoDB mới là kiến trúc stateless chuẩn mà đề thi ưu tiên. Nếu scenario nói "users bị mất session khi instance bị terminate", đáp án đúng thường là **tách session ra ngoài**, không phải bật sticky.

**5. ELB Health Check vs EC2 Status Check trong ASG**
- ASG để Health Check Type = EC2: chỉ biết instance còn sống ở mức phần cứng/hypervisor.
- Để = ELB: biết cả **ứng dụng bên trong có khỏe không** (endpoint /health trả 200). Muốn tự thay instance khi app treo dù EC2 vẫn chạy → chọn ELB Health Check.

**6. Min / Desired / Max**
- Min là sàn đảm bảo HA, Max là trần chặn chi phí, Desired là số hiện tại ASG đang cố duy trì. Scheduled Scaling thay đổi Min/Desired/Max theo lịch; Target Tracking thay đổi Desired trong khoảng Min–Max.

## Bẫy đề thi

1. **"Cần IP tĩnh để đối tác whitelist" mà chọn ALB.** ALB không có static IP cố định cho từng AZ như NLB. Gặp whitelist / Elastic IP → NLB (hoặc NLB đứng trước ALB trong kiến trúc nâng cao).

2. **Quên Multi-AZ cho ASG.** ASG chỉ đặt trong 1 AZ thì không HA, dù có Min = 10. Đề hay cho scenario "ASG in a single AZ, AZ fails" — lỗi nằm ở thiết kế AZ, không phải ở số lượng instance.

3. **Chọn Simple Scaling cho traffic spike đột ngột.** Simple Scaling cộng cố định + cooldown dài nên phản ứng quá chậm. Traffic biến động mạnh → Target Tracking hoặc Step Scaling.

4. **Nhầm Deregistration Delay với Cooldown.** Deregistration Delay là cho target **hoàn thành request đang dở** khi rời Target Group (mặc định 300s). Cooldown là thời gian ASG **nghỉ giữa hai lần scaling**. Hai con số 300s giống nhau nhưng là hai khái niệm khác nhau.

5. **Bật Sticky Sessions để giải quyết mọi bài toán session.** Sticky làm mất cân bằng tải và kẹt user khi target chết. Đề thi SAA ưu tiên stateless: session ra ElastiCache / DynamoDB.

6. **CLB xuất hiện trong đáp án.** Nếu yêu cầu là path-based routing, target group, WebSocket hiện đại — CLB không làm được. CLB gần như luôn là đáp án nhiễu cho kiến trúc mới.

7. **Cross-Zone tắt gây tải lệch mà tưởng do instance yếu.** Khi số instance các AZ không đều và Cross-Zone bị tắt trên NLB, một vài instance sẽ quá tải dù tổng capacity vẫn đủ.

8. **Health Check path sai.** Cấu hình Health Check vào `/` nhưng trang chủ nặng / trả redirect 301, target bị đánh unhealthy oan và ASG liên tục thay instance. Health Check nên trỏ tới endpoint nhẹ chuyên dụng như `/health` trả đúng mã kỳ vọng.

## Tóm tắt 5 dòng

1. ALB là Layer 7 cho HTTP/HTTPS với path/host routing và Target Group; NLB là Layer 4 TCP/UDP hiệu năng cực cao có static IP/Elastic IP; GWLB là Layer 3 để đưa traffic qua appliance bảo mật bên thứ ba; CLB là thế hệ cũ.
2. Health Check loại target hỏng, Cross-Zone chia đều tải xuyên AZ, Sticky Sessions giữ user ở một target (nên thay bằng session store ngoài), Deregistration Delay mặc định 300s cho request đang dở hoàn thành.
3. ASG dùng Launch Template với Min/Desired/Max, phải trải nhiều AZ mới đạt High Availability và tự thay thế instance unhealthy.
4. Target Tracking là Scaling Policy được khuyên dùng nhất (giữ metric ở mục tiêu), Step cho phản ứng theo bậc, Scheduled cho tải theo lịch, Cooldown tránh scale dồn dập.
5. Mẫu kiến trúc kinh điển của SAA-C03 là ALB + ASG Multi-AZ + Target Tracking: vừa resilient khi AZ/instance hỏng, vừa high-performing và tối ưu chi phí khi traffic biến động.

## Quiz — 5 câu hỏi tiếng Anh kiểu đề thi

**Question 1.** A company runs a web application and a mobile API behind a single domain. Requests to `/images/*` must go to servers optimized for image processing, requests to `api.example.com` must go to a different group of servers, and all traffic uses HTTPS. Which load balancer should the solutions architect choose?

A. Network Load Balancer with TCP listeners
B. Application Load Balancer with host-based and path-based routing rules
C. Gateway Load Balancer with GENEVE encapsulation
D. Classic Load Balancer with sticky sessions enabled

**Question 2.** A trading partner requires the company to provide fixed IP addresses so the partner can allowlist them in its firewall. The application uses a custom TCP protocol and must handle millions of requests per second with ultra-low latency. Which load balancer meets these requirements?

A. Application Load Balancer
B. Classic Load Balancer
C. Network Load Balancer with Elastic IP addresses
D. Gateway Load Balancer

**Question 3.** An Auto Scaling group maintains a web application across three Availability Zones. Traffic is predictable: it is high during business hours on weekdays and very low at night and on weekends. The company wants to reduce costs without reacting to real-time metrics. Which scaling policy is most appropriate?

A. Target Tracking Scaling on CPU utilization
B. Step Scaling based on CloudWatch alarms
C. Simple Scaling with a long cooldown period
D. Scheduled Scaling that adjusts desired capacity by time

**Question 4.** During deployments, users report that in-progress file uploads are frequently interrupted when old Amazon EC2 instances are removed from service. The instances sit behind an Application Load Balancer. Which setting should the solutions architect increase to reduce these interruptions?

A. Idle timeout of the Application Load Balancer
B. Deregistration delay of the target group
C. Health check interval of the target group
D. Cooldown period of the Auto Scaling group

**Question 5.** A company wants a highly available architecture for a stateless web application. Traffic varies unpredictably throughout the day. The solutions architect must ensure the application survives the loss of one Availability Zone and maintains average CPU utilization near 50% automatically. Which design meets these requirements?

A. EC2 instances in a single AZ behind a Classic Load Balancer with Simple Scaling
B. An Auto Scaling group spanning multiple AZs behind an Application Load Balancer, using Target Tracking Scaling
C. A fixed number of large EC2 instances in multiple AZs with Sticky Sessions enabled on an ALB
D. EC2 instances behind a Network Load Balancer with Scheduled Scaling only

## Đáp án quiz

**Question 1 — Đáp án: B**
Giải thích: Yêu cầu routing theo path (`/images/*`) và theo host (`api.example.com`) là tính năng Layer 7 của ALB. NLB (Layer 4) không đọc được path/host của HTTP, GWLB dùng cho appliance bảo mật, CLB không hỗ trợ routing nâng cao theo Target Group như ALB.

**Question 2 — Đáp án: C**
Giải thích: Từ khóa "fixed IP / allowlist / custom TCP / millions of requests per second / ultra-low latency" là dấu hiệu kinh điển của NLB. NLB cho gắn Elastic IP theo AZ và xử lý Layer 4 ở hiệu năng cực cao. ALB không cung cấp static IP kiểu này.

**Question 3 — Đáp án: D**
Giải thích: Tải đoán trước được theo giờ giấc cố định thì dùng Scheduled Scaling để chủ động đặt Desired/Min/Max theo lịch, tiết kiệm chi phí ban đêm/cuối tuần. Target Tracking và Step Scaling phản ứng theo metric thời gian thực, không đúng với yêu cầu "không dựa vào metric" của đề.

**Question 4 — Đáp án: B**
Giải thích: Deregistration Delay (Connection Draining), mặc định 300 giây, cho phép target hoàn thành các request đang xử lý (như upload dở) trước khi bị gỡ hẳn. Cooldown của ASG liên quan tới khoảng nghỉ giữa các lần scaling, không trực tiếp bảo vệ in-flight request ở Target Group.

**Question 5 — Đáp án: B**
Giải thích: Đây là mẫu kiến trúc kinh điển của SAA: ALB + ASG trải nhiều AZ (sống sót khi mất 1 AZ) + Target Tracking giữ CPU quanh 50% và tự scale theo tải khó đoán. Phương án A sai vì single AZ và CLB; C sai vì số instance cố định, không tự scale; D sai vì Scheduled Scaling chỉ hợp với tải theo lịch, không hợp tải khó đoán.
