# Bài 02 — Billing và Free Tier an toàn

## Mục tiêu bài học
- Hiểu cách AWS tính tiền và vì sao người mới dễ bị trừ tiền oan
- Biết dùng AWS Pricing Calculator, Billing Dashboard, Cost Explorer
- Biết thiết lập AWS Budgets và Billing Alarm ngay ngày đầu tiên
- Nắm chính xác Free Tier MỚI áp dụng cho tài khoản tạo từ 15/07/2025
- Nhận diện các bẫy tốn tiền phổ biến: NAT Gateway, Elastic IP, RDS/snapshot quên xóa, tài nguyên ở Region khác
- Nắm checklist an toàn ngày 1 và cách terminate tài nguyên đúng cách
- Hiểu Budget là chuông báo, không phải nắp chặn chi tiêu

## Lý thuyết chính

### 1. Cách AWS tính tiền

AWS tính tiền theo nguyên tắc **pay-as-you-go**: mỗi dịch vụ có một cách tính riêng — EC2 tính theo giờ/giây chạy, S3 tính theo dung lượng lưu trữ + số request, Lambda tính theo số request + thời gian chạy, dữ liệu truyền ra Internet (data transfer out) thường bị tính phí trong khi truyền vào thường miễn phí.

Ba yếu tố luôn xuất hiện trong hóa đơn: **Compute** (thời gian máy chạy), **Storage** (dung lượng lưu), **Data transfer out** (dữ liệu đi ra Internet). Điểm mấu chốt người mới hay quên: **nhiều tài nguyên vẫn tính tiền khi bạn tưởng nó đã "tắt"** — ổ đĩa EBS vẫn tính tiền khi EC2 đã stop, snapshot vẫn tính tiền sau khi đã xóa instance, địa chỉ IP tĩnh không dùng vẫn tính tiền.

Mỗi **Region có giá khác nhau**. Tài nguyên bạn tạo ở Region nào thì nằm ở Region đó — quên một instance ở Region xa là bẫy kinh điển.

### 2. Các công cụ quản lý chi phí

- **AWS Pricing Calculator:** Công cụ ước tính chi phí *trước khi* dùng. Chọn dịch vụ, cấu hình, Region → ra bảng ước tính để dự toán. Đề thi hay hỏi "muốn ước tính chi phí trước khi triển khai thì dùng gì?" — đáp án là Pricing Calculator.
- **Billing Dashboard (Billing and Cost Management Dashboard):** Trang tổng quan hóa đơn của tài khoản: tháng này đã tốn bao nhiêu, dịch vụ nào tốn nhất, xem hóa đơn các tháng trước.
- **AWS Cost Explorer:** Phân tích chi phí *đã phát sinh* theo thời gian, lọc theo dịch vụ, Region, tag, tài khoản. Dùng để trả lời câu hỏi "tháng trước tiền tăng vì dịch vụ nào?" Cost Explorer còn có khả năng forecast (dự báo) chi phí sắp tới.
- **AWS Budgets:** Đặt ngân sách và nhận cảnh báo khi chi phí thực tế hoặc dự báo vượt ngưỡng (ví dụ báo ở 50%, 80%, 100% của $10/tháng). Budgets gửi cảnh báo qua email và Amazon SNS.
- **Billing Alarm (CloudWatch Billing Alarm):** Alarm dựa trên metric hóa đơn trong CloudWatch. Lưu ý thực tế hay thi: Billing metric nằm ở Region **us-east-1 (N. Virginia)** — muốn tạo billing alarm phải chuyển sang Region đó.
- **AWS Cost and Usage Report (CUR):** Báo cáo chi phí chi tiết nhất, xuất ra S3 để phân tích sâu.
- **Trusted Advisor — mục Cost Optimization:** Gợi ý tài nguyên đang lãng phí, ví dụ EBS volume không gắn vào đâu, instance chạy utilization thấp.

### 3. Free Tier MỚI — phần bắt buộc phải học đúng

**Cảnh báo quan trọng:** Rất nhiều tài liệu, video YouTube và blog cũ vẫn dạy gói Free Tier "12 tháng miễn phí 750 giờ EC2 mỗi tháng". **Gói đó đã HẾT cho tài khoản mới.** Nếu bạn làm theo tài liệu cũ, bạn sẽ hiểu sai hoàn toàn cách tài khoản mới được tính tiền.

Đối với **tài khoản tạo từ ngày 15/07/2025**, AWS áp dụng chương trình Free Tier mới:

- **Nhận $100 credit ngay khi tạo tài khoản.**
- **Nhận thêm tối đa $100 credit nữa** khi hoàn thành các hoạt động khám phá (explore activities) mà AWS gợi ý — ví dụ dùng thử các dịch vụ cơ bản. Tổng credit tối đa là **$200 trong vòng 6 tháng**.
- Tài khoản mới bắt đầu ở **Free plan (gói miễn phí):** Trong gói này, **bạn KHÔNG bị trừ tiền** ngay cả khi dùng dịch vụ — hệ thống trừ vào credit, và khi hết credit hoặc hết 6 tháng, tài khoản Free plan sẽ bị đóng/paused chứ không tự động chuyển sang tính tiền thẻ của bạn.
- **Chỉ khi bạn chủ động nâng cấp lên Paid plan** thì AWS mới bắt đầu tính tiền vượt mức vào phương thức thanh toán. Vì vậy: đừng bấm nâng cấp Paid plan khi chưa hiểu rõ mình đang làm gì.
- Ngoài credit, vẫn có **30+ dịch vụ Always Free** — miễn phí dài hạn trong giới hạn nhất định (ví dụ một lượng request Lambda, dung lượng DynamoDB ở mức nhỏ) áp dụng kể cả cho tài khoản Paid, khác với credit có thời hạn 6 tháng.

Phân biệt hai khái niệm hay bị nhầm: **Credit $200 / 6 tháng** là "tiền khuyến mãi có hạn dùng". **Always Free** là "hạn mức miễn phí luôn có sẵn" của hơn 30 dịch vụ. Hết 6 tháng Free plan mà không nâng cấp thì tài khoản đóng; nâng cấp lên Paid plan thì Always Free vẫn còn, nhưng dùng vượt hạn mức là bắt đầu tính tiền thật.

### 4. Các bẫy tốn tiền kinh điển

Đây là phần thực tế nhất của bài — và cũng là phần đề thi Cost-Optimized thích hỏi:

- **NAT Gateway:** Tính phí **theo giờ tồn tại + theo lượng dữ liệu đi qua**. Tạo NAT Gateway cho bài lab rồi quên xóa là cách cháy tiền nhanh nhất của người mới. Học xong phải xóa NAT Gateway ngay.
- **Elastic IP không gắn vào instance nào:** Địa chỉ IP tĩnh đang "thả rông" bị tính phí theo giờ. Không dùng thì phải **release** nó.
- **EC2 stop nhưng EBS vẫn tính tiền:** Stop instance chỉ tắt phần compute. Ổ đĩa EBS vẫn tồn tại và vẫn tính tiền storage cho đến khi bạn xóa volume. Muốn hết tính tiền hẳn phải **terminate instance + xóa EBS volume**.
- **Quên RDS và snapshot:** RDS instance quên tắt vẫn chạy 24/7. Snapshot của EBS/RDS chụp rồi quên cũng tích tiền theo dung lượng mỗi tháng.
- **Tài nguyên ở Region khác:** Bạn chuyển Region để test rồi quên. Billing Dashboard nhìn tổng thì thấy tốn tiền mà vào Region mặc định lại không thấy máy nào. Cách xử lý: kiểm tra từng Region, hoặc dùng Cost Explorer lọc theo Region và Resource Explorer.
- **S3 quên đồ cũ:** File lưu mãi vẫn tính tiền storage; nên đặt **S3 Lifecycle Policy** để chuyển tầng lưu trữ hoặc tự xóa.
- **Load Balancer, Elastic IP, EBS volume orphan:** Các tài nguyên "mồ côi" không còn phục vụ ai nhưng vẫn nằm trên hóa đơn.

### 5. Budget là chuông báo, không phải nắp chặn

Phải thuộc lòng câu này cho cả đời làm AWS lẫn khi đi thi:

**AWS Budgets và Billing Alarm là CHUÔNG BÁO, KHÔNG phải công tắc ngắt tiền.** Vượt ngân sách thì AWS gửi email/SNS cảnh báo cho bạn — hệ thống **không tự tắt** EC2 hay xóa tài nguyên giùm bạn. Bạn nhận được cảnh báo mà không vào xử lý thì tiền vẫn tiếp tục chạy.

Muốn tự động hành động khi vượt budget, phải tự kết hợp thêm: Budget Actions, hoặc SNS kích hoạt Lambda để stop instance. Mặc định thì không có gì tự ngắt cả. Đề thi hay gài câu "Budget sẽ tự động ngăn chi phí vượt quá $X" — câu đó là **SAI**.

### 6. Checklist an toàn ngày 1

Làm đủ danh sách này trong ngày đầu tiên tạo tài khoản:

1. Bật **MFA cho Root Account**, tạo IAM User/Identity Center riêng cho việc hằng ngày, không dùng Root.
2. **Không tạo Access Key cho Root.** Không lộ Access Key ở bất kỳ đâu — không up lên GitHub, không gửi qua chat, không chụp màn hình chứa key.
3. Tạo **AWS Budget $0 / $1 và $10** với cảnh báo email ở 50%, 80%, 100% — để có bất thường là biết ngay. Tạo thêm **CloudWatch Billing Alarm** (nhớ chuyển Region sang us-east-1).
4. Bật **Billing alerts** trong Billing Preferences và bật IAM User access to Billing nếu cần.
5. Xem qua **Billing Dashboard** và tập mở **Cost Explorer** để quen mặt.
6. Ước tính chi phí lab bằng **Pricing Calculator** trước khi tạo tài nguyên đắt như NAT Gateway, RDS.
7. Quy tắc cá nhân: tạo tài nguyên nào, ghi lại tài nguyên đó; học xong một buổi là **terminate + kiểm tra lại đúng Region** trước khi đóng máy.
8. Kiểm tra các Region khác xem có tài nguyên nào quên không — đặc biệt sau khi làm lab theo video dùng Region lạ.

### 7. Terminate đúng cách

- **Stop EC2:** Tắt máy ảo, hết tiền compute, nhưng **EBS vẫn tính tiền**, Elastic IP gắn vào vẫn còn đó. Dữ liệu trên Instance Store (nếu có) mất khi stop.
- **Terminate EC2:** Xóa hẳn máy ảo. EBS root volume mặc định bị xóa theo (nếu giữ thiết lập Delete on Termination), nhưng EBS volume phụ gắn thêm có thể còn sót lại — phải kiểm tra và xóa tay.
- Sau khi terminate, vào kiểm tra tiếp: **EBS Volumes** (còn volume nào `available` không?), **Snapshots**, **Elastic IPs** (release IP thừa), **NAT Gateway** (delete), **RDS instances/snapshots**. Xóa sạch "đồ mồ côi" mới thực sự hết tiền.

## Ví dụ đời thường

**Hóa đơn AWS giống như hóa đơn điện nước + tiền thuê mặt bằng ở Việt Nam.**

- **EC2 đang chạy** giống như bóng đèn đang bật — tắt đèn (stop) thì hết tiền điện phần đèn. Nhưng **EBS** giống như tiền thuê kho chứa đồ: bạn không đến kho nữa nhưng đồ còn để đó thì chủ kho vẫn thu tiền tháng. Muốn hết tiền kho thì phải dọn đồ đi (xóa volume) — đó là terminate đúng nghĩa.
- **NAT Gateway quên xóa** giống như thuê một anh bảo vệ đứng cổng tính lương theo giờ, kể cả ban đêm không có ai qua cổng anh vẫn được trả lương. Học xong bài lab mà quên "cho bảo vệ nghỉ" thì cuối tháng nhìn bảng lương giật mình.
- **AWS Budgets** giống như chuông báo cháy và tin nhắn cảnh báo của ngân hàng: nó kêu lên khi có khói, nhưng nó **không tự dập lửa**. Bạn nghe chuông mà không chạy vào tắt bếp thì nhà vẫn cháy — tiền vẫn trừ đều đều.
- **Free Tier mới với credit $200** giống như thẻ quà tặng 200 nghìn có hạn dùng 6 tháng trong siêu thị: dùng trong hạn mức thì trừ vào thẻ quà, hết hạn thì thẻ hết giá trị. Chỉ khi bạn tự đăng ký gói trả phí (Paid plan) thì siêu thị mới bắt đầu quẹt thẻ ngân hàng của bạn.
- **Đồ quên ở Region khác** giống như bạn có 3 căn nhà ở 3 tỉnh mà chỉ nhớ dọn 1 căn — 2 căn còn lại vẫn bị tính tiền điện nước tối thiểu mỗi tháng.

## Phân biệt dễ nhầm

| Cặp dễ nhầm | Cách phân biệt |
|---|---|
| Pricing Calculator vs Cost Explorer | Calculator = ước tính *trước* khi dùng. Cost Explorer = phân tích chi phí *đã* phát sinh |
| AWS Budgets vs Billing Alarm | Budgets đặt ngân sách + cảnh báo theo % ngân sách, có forecast. Billing Alarm là CloudWatch alarm trên metric hóa đơn, phải tạo ở us-east-1 |
| Stop vs Terminate EC2 | Stop = tắt máy, EBS vẫn còn và vẫn tính tiền. Terminate = xóa máy, cần kiểm tra xóa EBS/snapshot kèm theo |
| Free plan vs Paid plan | Free plan không bị trừ tiền thẻ, hết credit/hết 6 tháng thì đóng tài khoản. Paid plan dùng vượt là tính tiền thật |
| Credit $200 vs Always Free | Credit là tiền khuyến mãi 6 tháng. Always Free là hạn mức miễn phí dài hạn của 30+ dịch vụ |
| Budget vs "nắp chặn chi tiêu" | Budget chỉ cảnh báo, không tự ngắt tài nguyên. Muốn tự hành động phải cấu hình thêm Budget Action / Lambda |

## Bẫy đề thi

- Câu "AWS Budgets sẽ tự động dừng dịch vụ khi vượt ngân sách" là mệnh đề **sai**. Budgets chỉ alert. Đây là bẫy được lặp lại rất nhiều.
- Đề hỏi công cụ ước tính chi phí cho hệ thống sắp triển khai: chọn **AWS Pricing Calculator**, không phải Cost Explorer (Cost Explorer nhìn về quá khứ).
- Đề hỏi vì sao hóa đơn vẫn tăng sau khi đã stop EC2: đáp án là **EBS volume vẫn bị tính phí** (hoặc Elastic IP / snapshot còn tồn tại).
- Đề hỏi billing alarm không tạo được: nhớ là phải ở Region **us-east-1** mới thấy metric billing.
- Tài liệu bên ngoài nói "12 tháng 750h EC2 miễn phí" là tài liệu cũ — với tài khoản mới từ 15/07/2025, sự thật là **$100 credit ngay + tối đa $100 nữa, tổng $200 trong 6 tháng, Free plan không trừ tiền thẻ trừ khi nâng cấp Paid plan**. Đi thi SAA-C03 thì làm theo facts hiện hành, đừng bê nguyên kiến thức cũ.
- Đề Cost-Optimized hay cho tình huống NAT Gateway của môi trường dev chạy 24/7 gây tốn tiền — hướng xử lý là xóa khi không dùng, hoặc cân nhắc NAT Instance / VPC Endpoint tùy scenario trong các bài sau.

## Tóm tắt 5 dòng
AWS tính tiền theo pay-as-you-go cho compute, storage và data transfer out — và nhiều tài nguyên vẫn tính tiền khi bạn tưởng đã tắt, điển hình là EBS volume sau khi stop EC2.
Pricing Calculator để ước tính trước, Cost Explorer để phân tích chi phí đã phát sinh, Billing Dashboard để xem hóa đơn, AWS Budgets để đặt cảnh báo ngân sách.
Free Tier mới cho tài khoản từ 15/07/2025: $100 credit ngay + tối đa $100 nữa, tổng $200 trong 6 tháng, Free plan không trừ tiền thẻ trừ khi bạn tự nâng cấp Paid plan, kèm 30+ dịch vụ Always Free.
Bẫy cháy tiền số một là NAT Gateway quên xóa, Elastic IP thả rông, RDS/snapshot quên, và tài nguyên bỏ quên ở Region khác.
AWS Budgets là chuông báo chứ không phải nắp chặn chi tiêu, và checklist ngày 1 là bật MFA cho Root, đặt Budget + Billing Alarm ngay, và terminate kèm xóa sạch volume/snapshot/IP thừa sau mỗi buổi học.

## Quiz

**Câu 1:** A solutions architect needs to estimate the cost of a new architecture BEFORE deploying it on AWS. Which tool should they use?

A. AWS Cost Explorer
B. AWS Pricing Calculator
C. AWS Budgets
D. AWS Cost and Usage Report

**Câu 2:** A user stopped an Amazon EC2 instance for a month but still sees charges on the bill. What is the MOST likely cause?

A. Stopped EC2 instances still charge full compute costs
B. The attached Amazon EBS volume continues to incur storage charges
C. AWS charges a penalty fee for stopping instances
D. The instance was automatically restarted every day

**Câu 3:** Which statement about AWS Budgets is CORRECT?

A. AWS Budgets automatically stops all resources when the budget is exceeded
B. AWS Budgets prevents any spending beyond the set amount
C. AWS Budgets sends alerts when actual or forecasted costs exceed the threshold, but does not stop spending by itself
D. AWS Budgets deletes unused resources automatically

**Câu 4:** A company created a NAT Gateway for a test and left it running unused for a month. What charges will apply?

A. No charges, because no traffic passed through it
B. Only a one-time creation fee
C. Hourly charges for the NAT Gateway's existence plus any data processing charges
D. Charges only if an EC2 instance is running

**Câu 5:** Where must a CloudWatch Billing Alarm be created to monitor the estimated charges of an AWS account?

A. Any Region the user prefers
B. ap-southeast-1 (Singapore)
C. us-east-1 (N. Virginia)
D. The Region where most EC2 instances run

## Đáp án quiz

**Câu 1 — B.** Pricing Calculator là công cụ duy nhất trong danh sách dùng để ước tính chi phí *trước* khi triển khai. Cost Explorer và Cost and Usage Report đều phân tích chi phí đã xảy ra. Budgets là đặt ngân sách và cảnh báo.

**Câu 2 — B.** Stop EC2 chỉ dừng tiền compute. EBS volume gắn với instance vẫn tồn tại nên vẫn bị tính tiền storage. Muốn hết hẳn phải terminate và xóa volume. Đây là tình huống thực tế kinh điển và cũng là bẫy đề thi kinh điển.

**Câu 3 — C.** Phải nhớ như in: Budgets là chuông báo, không phải nắp chặn. Nó gửi alert qua email/SNS khi chi phí thực tế hoặc dự báo vượt ngưỡng, nhưng không tự stop/delete bất cứ thứ gì nếu bạn không cấu hình thêm hành động.

**Câu 4 — C.** NAT Gateway tính phí theo giờ tồn tại, kể cả khi không có traffic, cộng thêm phí xử lý dữ liệu nếu có dữ liệu đi qua. Quên xóa NAT Gateway là nguyên nhân cháy tiền số một của người học AWS.

**Câu 5 — C.** Billing metrics của CloudWatch chỉ có ở us-east-1 (N. Virginia). Muốn tạo Billing Alarm, bạn phải chuyển Console sang Region us-east-1 — chi tiết nhỏ nhưng đề thi rất thích hỏi.
