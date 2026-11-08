# Bài 04 — Lambda và Serverless

## Mục tiêu bài học
- Hiểu Serverless là gì và vì sao nó khác với việc thuê server truyền thống
- Hiểu AWS Lambda hoạt động như thế nào: function, trigger, event, execution role
- Nắm các giới hạn phải thuộc: timeout tối đa 15 phút, RAM 128MB–10GB
- Hiểu mô hình tính tiền Lambda: theo số request + GB-giây
- Biết các nguồn kích hoạt phổ biến: S3, API Gateway, SQS, SNS, EventBridge, DynamoDB
- Hiểu Concurrency và Cold Start ở mức khái niệm, biết yếu tố nào làm tăng/giảm cold start
- Phân biệt rõ khi nào dùng Lambda, khi nào dùng EC2
- Biết Elastic Beanstalk như cầu nối giữa EC2 và thế giới managed

## Lý thuyết chính

### 1. Serverless là gì?

**Serverless** không có nghĩa là "không có server". Server vẫn tồn tại — nhưng **AWS quản lý toàn bộ server thay bạn**: bạn không provision, không patch OS, không lo scale server, không trả tiền cho server đang ngồi chơi. Bạn chỉ tập trung vào code và logic nghiệp vụ.

Bốn đặc điểm của Serverless mà đề thi hay kiểm tra:

- **No server management:** Không có EC2 nào để bạn đăng nhập hay bảo trì.
- **Automatically scaling:** Tự scale theo lượng request, từ 0 lên hàng nghìn.
- **Pay for value:** Chỉ trả tiền khi code thực sự chạy. Không có request thì không tốn tiền compute.
- **Highly available by default:** AWS chạy function trên nhiều AZ trong Region.

Các dịch vụ serverless tiêu biểu của AWS: **Lambda** (compute), **S3** (storage), **DynamoDB** (database), **API Gateway**, **SQS**, **SNS**, **EventBridge**, **Step Functions**, **Fargate** (serverless container). Ngôi sao của bài này là Lambda.

### 2. AWS Lambda hoạt động như thế nào?

**AWS Lambda** là dịch vụ **Function as a Service (FaaS)**: bạn tải lên một đoạn code gọi là **Lambda Function** (viết bằng Python, Node.js, Java, Go, C#, Ruby...), và Lambda chỉ chạy đoạn code đó **khi có sự kiện kích hoạt**. Ngoài thời gian chạy đó, function "không tồn tại" và bạn không tốn xu nào.

Quy trình 4 bước:

1. Bạn viết code và tạo Function, chọn **Runtime** (ví dụ Python 3.12), cấu hình Memory và Timeout, và gắn một **Execution Role** (IAM Role) định nghĩa function được phép gọi dịch vụ gì — ví dụ đọc S3, ghi DynamoDB. Đây là ứng dụng trực tiếp của Bài 01: Lambda dùng Role, không dùng Access Key.
2. Một **Event (sự kiện)** xảy ra từ một **Trigger (nguồn kích hoạt)**.
3. Lambda provision một môi trường chạy (execution environment), thực thi code với dữ liệu của event truyền vào.
4. Chạy xong, Lambda tính tiền đúng theo thời gian chạy và bộ nhớ đã cấu hình, rồi môi trường có thể được giữ lại một lúc để tái sử dụng hoặc bị dọn đi.

Ngoài code tự viết, Lambda còn chạy được **container image** đóng gói sẵn. Function có thể được cấu hình qua các **Environment Variables**, gắn vào VPC nếu cần truy cập tài nguyên private, và có cơ chế **Versions + Aliases** để triển khai an toàn.

### 3. Triggers — ai gọi Lambda dậy?

Đây là danh sách phải thuộc, vì đề thi hỏi liên tục:

- **Amazon S3:** File vừa được upload lên bucket → Lambda chạy để xử lý. Ví dụ: ảnh vừa tải lên thì tự tạo thumbnail.
- **Amazon API Gateway:** Có HTTP request gọi vào API → Lambda xử lý và trả kết quả. Đây là combo xây backend/serverless API kinh điển nhất.
- **Amazon SQS:** Có message trong hàng đợi → Lambda được kích hoạt để xử lý message. Lambda tự scale theo độ dài queue.
- **Amazon SNS:** Có notification được publish → Lambda xử lý.
- **Amazon EventBridge / CloudWatch Events:** Sự kiện theo lịch (cron) hoặc theo sự kiện hệ thống. Ví dụ: cứ 1 giờ chạy Lambda dọn dẹp một lần — thay cho việc để một EC2 chạy 24/7 chỉ để chờ.
- **DynamoDB Streams:** Dữ liệu trong bảng DynamoDB thay đổi → Lambda phản ứng.
- **CloudWatch Logs, Kinesis, Cognito, Alexa...:** Các nguồn khác ở mức biết tên.

Điểm chung: Lambda là **event-driven** — bị động chờ sự kiện, không chủ động chạy liên tục.

### 4. Cấu hình quan trọng: Memory, Timeout, và các giới hạn cứng

Các con số này là **facts phải thuộc lòng** cho đề thi:

- **Timeout tối đa: 15 phút (900 giây).** Một lần chạy của Lambda không bao giờ dài hơn 15 phút. Quá 15 phút, Lambda bị cắt. Workload chạy lâu hơn 15 phút (render video dài, training model, batch job hàng giờ) thì **Lambda không phù hợp** — phải nghĩ tới EC2, ECS/Fargate hoặc Step Functions phối hợp.
- **Memory (RAM): từ 128MB đến 10GB.** Bạn chọn RAM, và AWS cấp CPU **tỷ lệ theo RAM** đã chọn — tăng RAM đồng nghĩa tăng cả sức mạnh CPU và tăng giá mỗi giây. Vì vậy đôi khi tăng RAM lại làm tổng chi phí rẻ hơn vì code chạy nhanh hơn hẳn.
- **/tmp storage:** Dung lượng đĩa tạm cho function, ở mức cơ bản là 512MB và cấu hình được lớn hơn.
- **Deployment package:** Có giới hạn kích thước cho file zip tải trực tiếp; package lớn thì dùng container image hoặc để trên S3.

Các giới hạn này chính là "luật chơi" để đề thi gài bẫy: cho một tác vụ chạy 30 phút rồi hỏi dùng Lambda được không — đáp án là không.

### 5. Cách Lambda tính tiền

Mô hình tính tiền của Lambda gồm hai thành phần:

- **Số request:** Tính theo số lần function được gọi (invoke).
- **Thời gian chạy tính theo GB-giây (GB-second):** Lấy lượng RAM đã cấu hình (tính theo GB) nhân với thời gian chạy thực tế (tính bằng mili-giây, cộng dồn thành giây). RAM cấu hình càng cao, đơn giá mỗi giây càng cao; code chạy càng lâu, tiền càng nhiều.

Hệ quả quan trọng: **Không có request thì hóa đơn Lambda bằng 0.** Không có khái niệm "máy đang bật chờ" như EC2 On-Demand. Đây là lý do Lambda cực rẻ cho workload thưa, không đều — và là điểm đối lập hoàn hảo với EC2 trong các câu hỏi Cost-Optimized.

### 6. Concurrency — độ đồng thời

**Concurrency** là số instance của function đang chạy **cùng một lúc** để xử lý các event đồng thời. 1.000 request đến cùng lúc thì Lambda có thể chạy hàng trăm, hàng nghìn bản sao function song song — tự scale mà bạn không cấu hình server nào cả.

Các khái niệm cần biết ở mức Associate:

- **Default concurrency limit:** Mỗi Region có hạn mức tổng concurrency cho toàn tài khoản (mặc định ở mức 1.000 concurrent executions, có thể yêu cầu tăng qua Service Quotas). Vượt hạn mức thì request bị **throttling** (từ chối/tạm hoãn).
- **Reserved Concurrency:** Dành riêng một lượng concurrency cho một function quan trọng, đảm bảo nó luôn có "suất chạy" và đồng thời đặt trần để nó không ăn hết quota của các function khác.
- **Provisioned Concurrency:** Trả tiền để giữ sẵn môi trường đã khởi tạo, nhằm **xóa cold start** cho function cần latency ổn định (xem mục dưới).

### 7. Cold Start ở mức khái niệm

**Cold Start** là độ trễ xảy ra khi Lambda phải **khởi tạo môi trường chạy mới** cho một request: tải code, khởi động runtime, chạy code khởi tạo ngoài handler. Request đầu tiên (hoặc request đến sau một thời gian function không được gọi) sẽ chậm hơn bình thường một chút.

Các request sau đó được xử lý bởi môi trường đã "ấm" (warm) thì không có cold start — gọi là **Warm Start**.

Yếu tố ảnh hưởng cold start cần biết:

- **Runtime:** Ngôn ngữ biên dịch/khởi động nặng như Java/.NET thường cold start lâu hơn Python/Node.js.
- **Memory cấu hình:** RAM càng cao, CPU cấp càng nhiều nên khởi tạo càng nhanh.
- **Kích thước package:** Code và thư viện càng cồng kềnh, tải và khởi tạo càng lâu.
- **VPC:** Function gắn vào VPC trước đây bị cold start lâu hơn rõ rệt (AWS đã cải thiện nhiều, nhưng đề thi vẫn có thể nhắc VPC làm tăng cold start).
- **Cách giảm cold start:** Dùng **Provisioned Concurrency**, chọn runtime nhẹ, giảm kích thước package, tăng memory. Đổi lại, Provisioned Concurrency tốn tiền ngay cả khi không có request — đánh đổi cost lấy latency.

Cold start chỉ là vấn đề nếu ứng dụng của bạn cực kỳ nhạy cảm với độ trễ (real-time). Với đa số bài toán xử lý file, xử lý queue, cron job — cold start vài trăm mili-giây là không đáng kể.

### 8. Lambda vs EC2 — khi nào dùng cái nào?

| Tiêu chí | Lambda | EC2 |
|---|---|---|
| Quản lý server | AWS lo hết | Bạn lo OS, patch, scale |
| Thời gian chạy mỗi tác vụ | **Tối đa 15 phút** | Không giới hạn |
| Cách tính tiền | Theo request + GB-giây, không chạy = 0 đồng | Theo giờ/giây khi instance đang chạy (kể cả lúc rảnh) |
| Kích hoạt | Event-driven (S3, API Gateway, SQS...) | Chạy liên tục, luôn sẵn sàng |
| Scale | Tự động, gần như tức thì | Phải cấu hình Auto Scaling |
| Phù hợp nhất | Tác vụ ngắn, theo sự kiện, traffic không đều, API backend nhẹ, xử lý file/message, cron job | Ứng dụng chạy dài, cần kiểm soát OS, phần mềm đặc thù, workload ổn định 24/7, tác vụ > 15 phút |

Quy tắc chọn nhanh cho đề thi: **ngắn + theo sự kiện + không đều → Lambda. Dài + liên tục + cần kiểm soát → EC2 (hoặc Fargate/ECS).**

### 9. Elastic Beanstalk — cầu nối

**AWS Elastic Beanstalk** không phải serverless — nó là **PaaS** đã gặp ở Bài 00. Bạn chỉ cần tải code ứng dụng web lên, Beanstalk tự provision EC2, Load Balancer, Auto Scaling, monitoring bên dưới và quản lý giúp bạn, nhưng bạn vẫn nhìn thấy và tùy chỉnh được các tài nguyên đó khi cần.

Vai trò của Beanstalk trong lộ trình học: nó là **cầu nối** cho người mới — chưa cần hiểu sâu từng dịch vụ lẻ như khi dùng EC2 thuần, nhưng cũng chưa "buông hết" như Lambda. Đề thi thường dùng Beanstalk cho scenario: "developer muốn deploy ứng dụng nhanh, không muốn quản lý hạ tầng chi tiết, nhưng ứng dụng là web app chạy liên tục không phù hợp với Lambda 15 phút". Nhớ: Beanstalk **miễn phí dịch vụ**, bạn chỉ trả tiền cho tài nguyên nó tạo ra (EC2, ELB...).

## Ví dụ đời thường

**Lambda giống như gọi thợ sửa ống nước theo vụ việc, EC2 giống như thuê một người giúp việc ở hẳn trong nhà.**

- **EC2** là người giúp việc sống tại nhà: tháng nào cũng trả lương cố định kể cả ngày không có việc gì, được cái gọi phát có mặt ngay và làm việc dài hơi bao lâu cũng được.
- **Lambda** là thợ sửa ống nước gọi qua ứng dụng: nhà không rò nước thì không gọi, không tốn đồng nào. Ống nước vỡ (sự kiện S3 upload file, có request API) thì thợ xuất hiện, sửa xong tính tiền đúng số phút sửa nhân với tay nghề (GB-giây), rồi thợ về. Cần 10 thợ cùng lúc vì cả khu chung cư cùng vỡ ống thì ứng dụng điều 10 thợ tới song song — đó là Concurrency.
- **Cold Start** là lần đầu gọi thợ vào buổi sáng sớm: thợ cần thời gian mặc đồ, lấy đồ nghề, chạy xe tới nhà — chậm hơn bình thường một chút. Các lần gọi sau trong ngày, thợ đã ở gần khu vực nên tới nhanh — đó là Warm Start. **Provisioned Concurrency** giống như trả tiền giữ một thợ trực sẵn trong tòa nhà 24/7: tốn tiền trực, nhưng có việc là xử lý ngay không chờ đợi.
- **Timeout 15 phút** là quy định của hãng thợ: mỗi ca sửa tối đa 15 phút, việc nào cần 2 tiếng thì không gọi thợ theo vụ được — phải thuê đội thi công ở lại dài hạn, tức là EC2/Fargate.
- **Trigger** giống như chuông báo: có người bấm chuông cửa (API Gateway nhận request), có thư nhét vào hộp thư (SQS có message), có đồ mới bỏ vào kho (S3 có file) là thợ tự biết việc mà đến làm, không cần ai ngồi canh.

## Phân biệt dễ nhầm

| Cặp dễ nhầm | Cách phân biệt |
|---|---|
| Lambda vs EC2 | Lambda event-driven, tối đa 15 phút/lần chạy, không chạy = 0 tiền. EC2 chạy liên tục, trả tiền khi máy bật kể cả lúc rảnh |
| Lambda vs Elastic Beanstalk | Lambda là serverless/FaaS — chỉ có code, không thấy server. Beanstalk là PaaS — vẫn có EC2 bên dưới do AWS provision hộ |
| Cold Start vs Warm Start | Cold Start là lần khởi tạo môi trường mới nên chậm. Warm Start tái sử dụng môi trường đang ấm nên nhanh |
| Reserved Concurrency vs Provisioned Concurrency | Reserved là dành quota + đặt trần concurrency. Provisioned là trả tiền giữ môi trường khởi tạo sẵn để xóa cold start |
| Timeout vs Concurrency | Timeout là giới hạn thời gian của *một* lần chạy (max 15 phút). Concurrency là số lần chạy *song song* cùng lúc |
| Execution Role vs Resource-based Policy của Lambda | Execution Role quy định function được gọi ra dịch vụ nào. Resource-based Policy của Lambda quy định ai/dịch vụ nào được gọi vào function |

## Bẫy đề thi

- Đề cho tác vụ chạy **30 phút / 1 giờ** rồi gợi ý Lambda: sai ngay vì **timeout tối đa 15 phút**. Đáp án đúng thường là EC2, ECS/Fargate, hoặc Step Functions điều phối nhiều bước.
- Đề hỏi cách giảm chi phí cho ứng dụng có traffic rất thưa, vài request mỗi giờ: **Lambda thắng EC2** vì không chạy thì không tốn tiền, trong khi EC2 vẫn tính tiền 24/7.
- Đề hỏi Lambda cần quyền đọc S3: đáp án là gắn **Execution Role (IAM Role)**, tuyệt đối không nhúng Access Key vào Environment Variables — bẫy này nối thẳng với kiến thức Bài 01.
- Đề mô tả function bị **throttling** khi traffic tăng đột biến: nguyên nhân là chạm trần **concurrency limit** của Region/account, cách xử lý là yêu cầu tăng quota hoặc đặt Reserved Concurrency cho function quan trọng.
- Đề hỏi ứng dụng nhạy cảm latency bị chậm ở request đầu tiên sau thời gian dài không ai dùng: đó là **Cold Start**, giải pháp là **Provisioned Concurrency** — nhưng nhớ nó làm tăng chi phí.
- Tăng Memory cho Lambda không chỉ tăng RAM: nó **tăng cả CPU** và có thể làm function chạy nhanh hơn, tổng tiền GB-giây thậm chí giảm. Đề thi thích kiểm tra điểm ngược intuition này.
- Lambda mặc định chạy ngoài VPC. Muốn Lambda truy cập RDS trong private subnet thì phải **gắn Lambda vào VPC** — lúc đó cần cấu hình subnet/security group và lưu ý chuyện truy cập Internet của function.

## Tóm tắt 5 dòng
Serverless nghĩa là AWS quản lý toàn bộ server, bạn chỉ viết code — Lambda là dịch vụ FaaS tiêu biểu, chỉ chạy function khi có event từ trigger như S3, API Gateway, SQS hay EventBridge.
Giới hạn cứng phải thuộc: timeout tối đa 15 phút, memory 128MB–10GB, và tăng memory cũng đồng nghĩa tăng CPU được cấp.
Lambda tính tiền theo số request cộng với GB-giây thời gian chạy nhân RAM đã cấu hình, nên không có request thì hóa đơn bằng 0 — ngược hẳn EC2.
Concurrency là số function chạy song song tự scale theo traffic, còn Cold Start là độ trễ khởi tạo môi trường mới, giảm được bằng Provisioned Concurrency nhưng phải trả thêm tiền.
Chọn Lambda cho tác vụ ngắn, theo sự kiện, traffic không đều; chọn EC2 cho workload dài hơn 15 phút, chạy liên tục hoặc cần kiểm soát OS; Elastic Beanstalk là PaaS ở giữa hai thế giới này.

## Quiz

**Câu 1:** What is the maximum timeout for a single AWS Lambda function execution?

A. 5 minutes
B. 15 minutes
C. 30 minutes
D. 60 minutes

**Câu 2:** A company uploads images to Amazon S3 and wants thumbnails to be created automatically every time a new image is uploaded. Which solution is MOST suitable and cost-effective?

A. Run a dedicated EC2 instance 24/7 that polls the S3 bucket
B. Trigger an AWS Lambda function from S3 events to generate the thumbnails
C. Use a Reserved Instance to process the images
D. Store the images and process them manually at the end of the day

**Câu 3:** How is AWS Lambda priced?

A. By the hour, based on the instance type selected
B. By the number of requests and the duration of execution measured in GB-seconds
C. By a fixed monthly subscription fee
D. By the amount of data stored in the function

**Câu 4:** A video rendering workload takes approximately 45 minutes to complete for each job. A solutions architect is asked whether Lambda is suitable. What is the correct assessment?

A. Lambda is suitable because it automatically scales
B. Lambda is suitable if the memory is increased to 10 GB
C. Lambda is NOT suitable because its maximum timeout is 15 minutes; a service such as EC2 or Fargate should be used
D. Lambda is suitable if Provisioned Concurrency is enabled

**Câu 5:** Users report that an API backed by Lambda is occasionally slow on the first request after long periods of inactivity, but fast afterwards. What phenomenon is this, and how can it be mitigated?

A. Throttling; increase the account concurrency limit
B. Cold start; enable Provisioned Concurrency
C. Memory leak; increase the function timeout
D. Network latency; move the function to another Region

## Đáp án quiz

**Câu 1 — B.** 15 phút (900 giây) là giới hạn cứng của Lambda — con số bắt buộc thuộc lòng. Bất kỳ workload nào dài hơn đều phải rời Lambda sang EC2/Fargate/Batch hoặc dùng Step Functions chia nhỏ công việc.

**Câu 2 — B.** Đây là use case serverless mẫu mực nhất: event S3 kích hoạt Lambda xử lý file ngay khi upload, không tốn tiền lúc không có ảnh nào. Phương án EC2 chạy 24/7 để polling vừa tốn tiền vừa là anti-pattern mà đề thi luôn đặt làm đáp án sai.

**Câu 3 — B.** Lambda tính tiền theo 2 thành phần: số lần invoke + thời gian chạy tính bằng GB-giây (RAM cấu hình × số giây chạy). Không có khái niệm chọn instance type hay trả theo giờ như EC2.

**Câu 4 — C.** 45 phút > 15 phút timeout tối đa nên Lambda bị loại ngay từ vòng gửi xe, bất kể tăng RAM (B) hay bật Provisioned Concurrency (D) — hai lựa chọn đó không thay đổi được giới hạn timeout. Đáp án đúng phải chuyển sang dịch vụ chạy dài như EC2 hoặc Fargate.

**Câu 5 — B.** Request đầu tiên sau thời gian dài không dùng bị chậm, các request sau nhanh — đó là dấu hiệu nhận diện kinh điển của Cold Start. Cách giảm chính thống là Provisioned Concurrency (giữ môi trường khởi tạo sẵn, chấp nhận trả thêm phí). Throttling liên quan đến concurrency limit, là hiện tượng khác hẳn.
