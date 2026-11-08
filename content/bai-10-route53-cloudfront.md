# Bài 10 — Route 53 & CloudFront: DNS và CDN

## Mục tiêu bài học

- Hiểu Route 53 làm hai việc: đăng ký domain và DNS resolution.
- Phân biệt các record type, đặc biệt là Alias — đặc sản của Route 53.
- Chọn đúng Routing Policy theo từng tình huống đề bài đưa ra.
- Hiểu CloudFront phân phối nội dung ra sao, khóa S3 bằng OAC thế nào.
- Phân biệt Signed URL vs Signed Cookies, và CloudFront vs Global Accelerator.

## Lý thuyết chính (tiếng Việt, giữ thuật ngữ English)

### 1. Route 53 là gì?

**Amazon Route 53** là dịch vụ **DNS** có tính sẵn sàng cao của AWS, đồng thời là nơi **đăng ký domain** (Domain Registrar). DNS là danh bạ của internet: dịch tên thân thiện như `shop.example.com` thành địa chỉ IP để máy tính kết nối.

Ở mức khái niệm, Route 53 được biết tới với **SLA 100%** về độ sẵn sàng của DNS — đề thi rất thích chi tiết này. Route 53 là dịch vụ **global**, không thuộc về một Region cụ thể.

### 2. Record Types cần nhớ

- **A:** trỏ hostname -> địa chỉ **IPv4**.
- **AAAA:** trỏ hostname -> địa chỉ **IPv6**.
- **CNAME:** trỏ hostname -> một **hostname khác**. Lưu ý: CNAME KHÔNG dùng được cho **zone apex** (domain gốc kiểu `example.com` không có `www`).
- **Alias:** record đặc biệt của riêng Route 53. Trỏ hostname -> tài nguyên AWS như **Application Load Balancer, CloudFront distribution, S3 website**. Khác CNAME ở chỗ: Alias dùng được cho cả **zone apex**, và truy vấn tới đích AWS thường không tốn thêm phí.

Các loại khác (MX cho mail, TXT để xác thực) chỉ cần biết mặt, đề SAA ít xoáy sâu.

### 3. Health Checks

Route 53 có **Health Check**: định kỳ kiểm tra endpoint (IP/hostname) còn sống hay không. Health Check là nền tảng của Routing Policy kiểu Failover: endpoint chính chết thì DNS tự trả về địa chỉ của endpoint dự phòng. Health Check cũng có thể gắn với CloudWatch Alarm.

### 4. Routing Policies

Đây là phần đề thi hỏi nhiều nhất của Route 53. Mỗi policy trả lời một kiểu câu hỏi khác nhau:

- **Simple:** một record, một hoặc nhiều giá trị, không có health check. Dùng khi chỉ có một đích duy nhất.
- **Weighted:** chia traffic theo **tỉ trọng** bạn đặt, ví dụ 80% sang version mới, 20% sang version cũ. Nhận diện: đề nhắc tới phần trăm traffic, A/B testing, canary.
- **Latency-based:** trả về endpoint có **độ trễ thấp nhất** cho người dùng, dựa trên Region AWS. Nhận diện: "giảm latency cho user toàn cầu".
- **Failover:** mô hình **active-passive**. Chính chạy, phụ đứng chờ. Kết hợp **Health Check**: chính chết thì tự chuyển sang phụ. Nhận diện: disaster recovery, primary / secondary.
- **Geolocation:** định tuyến theo **vị trí địa lý của người dùng** (châu lục / quốc gia). Dùng để phục vụ nội dung theo ngôn ngữ, tuân thủ quy định địa phương. Đừng nhầm với Latency-based.
- **Geoproximity:** định tuyến theo vị trí địa lý của cả user và tài nguyên, có thể nới/thu phạm vi bằng bias. Ở mức khái niệm cho SAA-C03.
- **Multivalue Answer:** trả về **nhiều giá trị** (nhiều IP) kèm health check cho từng giá trị — giống Simple nhưng thông minh hơn, endpoint chết sẽ bị loại khỏi đáp án.

### 5. CloudFront là gì?

**Amazon CloudFront** là dịch vụ **CDN (Content Delivery Network)**. CloudFront sao chép nội dung tới các **Edge Location** nằm rải khắp thế giới, gần người dùng. User ở Việt Nam tải file từ edge gần Việt Nam thay vì bay sang server gốc ở Mỹ — nhanh hơn nhiều và giảm tải cho origin.

- **Origin:** nguồn gốc nội dung — có thể là **S3 bucket, Application Load Balancer, EC2**, hoặc một HTTP server on-premises.
- **Distribution:** cấu hình CloudFront trỏ tới một origin.
- Nội dung được **cache** tại edge trong một khoảng thời gian (TTL). Hết TTL, edge mới về origin lấy bản mới.

### 6. OAC — Khóa S3 chỉ cho CloudFront vào

Bài toán kinh điển: bạn muốn user chỉ xem được file qua CloudFront, không ai lấy được link S3 trực tiếp để tải lậu.

Đáp án: dùng **Origin Access Control (OAC)**. Bạn cấu hình S3 bucket thành private, và bucket policy chỉ cho phép đúng CloudFront distribution của bạn truy cập. OAC là cơ chế hiện tại thay cho cơ chế cũ OAI (Origin Access Identity).

### 7. Signed URL vs Signed Cookies

Khi nội dung là trả phí / riêng tư, cache công khai là không đủ:

- **Signed URL:** một URL có chữ ký và thời hạn, cấp quyền truy cập tới **một file duy nhất**. Hợp để bán từng file: một khóa học, một ebook.
- **Signed Cookies:** cookie có chữ ký đính vào trình duyệt, cấp quyền truy cập tới **nhiều file** cùng lúc. Hợp khi user đã đăng nhập và cần xem cả một thư viện video.

### 8. Cache Invalidation

Khi bạn cập nhật file ở origin nhưng edge vẫn giữ bản cache cũ, bạn cần **Cache Invalidation** để xóa cache trước hạn. Ở mức khái niệm: invalidation **có tốn phí sau khi dùng hết hạn mức miễn phí** — và vì tốn phí + không nên lạm dụng, cách làm tốt hơn thường là đặt tên file có version (ví dụ `style-v2.css`) thay vì invalidate liên tục.

### 9. Chứng chỉ HTTPS cho CloudFront — Bẫy Region

Muốn dùng custom domain + HTTPS trên CloudFront, bạn cấp chứng chỉ bằng **AWS Certificate Manager (ACM)**. Bẫy kinh điển: chứng chỉ dùng cho CloudFront **bắt buộc phải ở Region us-east-1**, dù origin của bạn nằm ở bất kỳ Region nào khác.

## Ví dụ đời thường

Route 53 giống tổng đài danh bạ 1080 ngày xưa: bạn đọc tên "quán phở Hòa" thì tổng đài trả số điện thoại. Còn Routing Policy là cách tổng đài chọn số nào để trả:

- Có một quán duy nhất -> đọc luôn số đó (Simple).
- Hai chi nhánh, muốn thử nghiệm chi nhánh mới với 20% khách -> Weighted.
- Khách ở Hà Nội thì giới thiệu chi nhánh gần nhất, ít phải chờ -> Latency-based.
- Chi nhánh chính mất điện thì tự động giới thiệu chi nhánh dự phòng -> Failover.
- Khách gọi từ nước nào thì giới thiệu thực đơn của nước đó -> Geolocation.

CloudFront giống chuỗi kho hàng của một sàn thương mại điện tử: thay vì mọi đơn đều ship từ tổng kho ở Mỹ mất cả tuần, sàn đặt sẵn hàng ở kho Hà Nội, kho Singapore. Khách gần kho nào thì nhận từ kho đó. S3 là tổng kho (Origin), các kho vùng là Edge Location, OAC là quy định "chỉ nhân viên giao hàng của hãng mới được vào tổng kho lấy hàng, khách không tự vào được".

## Phân biệt dễ nhầm

### CNAME vs Alias

| Tiêu chí | CNAME | Alias |
|---|---|---|
| Trỏ tới | Hostname khác | Tài nguyên AWS (ALB, CloudFront, S3...) |
| Dùng ở zone apex (`example.com`) | Không | Có |
| Của ai | Chuẩn DNS chung | Đặc sản riêng Route 53 |

### Geolocation vs Latency-based

- Latency-based: chọn nơi **nhanh nhất** cho user.
- Geolocation: chọn nơi **đúng vùng địa lý** của user, dù nơi đó chưa chắc nhanh nhất. Đề nhắc "tuân thủ luật địa phương / nội dung theo quốc gia" là Geolocation.

### Signed URL vs Signed Cookies

- 1 file -> Signed URL.
- Nhiều file -> Signed Cookies.

### CloudFront vs Global Accelerator

| Tiêu chí | CloudFront | Global Accelerator |
|---|---|---|
| Bản chất | CDN có cache nội dung | Tăng tốc đường truyền, không cache |
| Hợp nhất cho | HTTP/HTTPS: web, ảnh, video | Non-HTTP, gaming, TCP/UDP |
| Địa chỉ | DNS name của distribution | 2 static Anycast IP |
| Đường đi | Từ Edge Location về origin | Qua mạng riêng AWS |

**AWS Global Accelerator (GA)** đưa traffic vào mạng riêng của AWS càng sớm càng tốt và cấp **2 static IP (Anycast)** — cùng một IP nhưng định tuyến tới điểm vào gần nhất. Đề nhắc "game cần kết nối UDP ổn định, IP cố định" là GA. Đề nhắc "phân phối ảnh/video/web tĩnh cho user toàn cầu" là CloudFront.

## Bẫy đề thi

1. **Zone apex + ALB** — Cần trỏ `example.com` (không có www) tới ALB: CNAME không làm được, phải dùng **Alias**.
2. **ACM certificate cho CloudFront phải ở us-east-1** — Đề cho bạn tạo cert ở ap-southeast-1 rồi không gắn được vào CloudFront, đáp án là tạo lại cert ở us-east-1.
3. **User tải trực tiếp từ S3, bỏ qua CloudFront** — Giải quyết bằng OAC + bucket private, không phải bằng cách đổi tên file cho khó đoán.
4. **Nhiều file trả phí** — Chọn Signed Cookies thay vì ngồi tạo Signed URL cho từng file.
5. **Weighted vs Failover** — Thấy tỉ lệ phần trăm là Weighted, thấy primary chết chuyển secondary là Failover. Hai policy này hay bị trộn.
6. **Global Accelerator cho nội dung cache** — GA không cache. Cần cache để giảm tải origin thì phải là CloudFront.

## Tóm tắt 5 dòng

Route 53 là DNS + đăng ký domain với SLA 100% ở mức khái niệm; Alias là record riêng của Route 53, trỏ được tới ALB/CloudFront/S3 và dùng được cho zone apex.
Routing Policies: Weighted chia theo tỉ trọng, Latency-based chọn nơi trễ thấp nhất, Failover active-passive kèm Health Check, Geolocation theo vị trí user.
CloudFront là CDN đưa nội dung ra Edge Location gần user, origin phổ biến là S3, ALB, EC2.
Dùng OAC để khóa S3 private chỉ cho CloudFront vào; Signed URL cho 1 file, Signed Cookies cho nhiều file; cert ACM cho CloudFront phải ở us-east-1.
Global Accelerator không cache, cấp 2 static Anycast IP, hợp cho non-HTTP/gaming/TCP-UDP; CloudFront hợp cho HTTP content cần cache.

## Quiz — 5 câu hỏi tiếng Anh kiểu đề thi (A/B/C/D)

**Question 1:** A company needs to point the zone apex domain `example.com` (without `www`) to an Application Load Balancer. Which Route 53 record type should be used?

A. A record pointing to the load balancer IP address
B. CNAME record
C. Alias record
D. AAAA record

**Question 2:** A company wants to gradually shift traffic to a new version of its application: 20% of users should reach the new version and 80% the old version. Which Route 53 routing policy meets this requirement?

A. Failover routing
B. Latency-based routing
C. Geolocation routing
D. Weighted routing

**Question 3:** Users must access paid video files only through CloudFront. Direct access to the underlying S3 bucket must be blocked. What should the architect configure?

A. Make the S3 bucket public and enable versioning
B. Use Origin Access Control (OAC) and keep the bucket private
C. Create Signed URLs for the bucket website endpoint
D. Enable S3 Transfer Acceleration

**Question 4:** A gaming company needs to improve connection stability for its global UDP-based game traffic and requires static IP addresses for its endpoints. Which service is the BEST choice?

A. Amazon CloudFront
B. AWS Global Accelerator
C. Route 53 Latency-based routing
D. Amazon API Gateway

**Question 5:** A development team created an ACM certificate in ap-southeast-1 but cannot associate it with their CloudFront distribution. What is the cause?

A. CloudFront does not support HTTPS
B. The certificate must be requested in us-east-1 for CloudFront
C. The distribution must be recreated in ap-southeast-1
D. ACM certificates expire after one day

## Đáp án quiz

**Câu 1 — Đáp án C.**
Giải thích tiếng Việt: Zone apex không dùng được CNAME, còn địa chỉ của ALB là hostname chứ không phải IP cố định nên A/AAAA cũng không hợp. **Alias** là record riêng của Route 53 sinh ra đúng cho việc này: trỏ apex tới ALB.

**Câu 2 — Đáp án D.**
Giải thích tiếng Việt: Thấy tỉ lệ phần trăm chia traffic (20/80) là dấu hiệu nhận diện của **Weighted routing**. Failover là chính/phụ khi có sự cố, không chia theo tỉ trọng.

**Câu 3 — Đáp án B.**
Giải thích tiếng Việt: **OAC** kết hợp bucket private là cách chuẩn để khóa S3, chỉ cho đúng CloudFront distribution truy cập. Bucket public thì ai cũng vào thẳng được, trái với yêu cầu đề bài.

**Câu 4 — Đáp án B.**
Giải thích tiếng Việt: Traffic **UDP / non-HTTP** cho gaming + cần **static IP** là bài toán của **Global Accelerator**: 2 static Anycast IP và đường truyền qua mạng riêng AWS. CloudFront là CDN cho HTTP content có cache, không phù hợp cho UDP gaming.

**Câu 5 — Đáp án B.**
Giải thích tiếng Việt: Bẫy Region kinh điển — chứng chỉ ACM dùng cho CloudFront **bắt buộc ở us-east-1**, bất kể origin ở Region nào. Phải xin lại cert ở us-east-1 rồi mới gắn vào distribution được.
