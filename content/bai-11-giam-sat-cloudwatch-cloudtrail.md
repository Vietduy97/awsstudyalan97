# Bài 11 — Giám Sát: CloudWatch, CloudTrail & AWS Config

## Mục tiêu bài học

- Phân biệt rạch ròi bộ ba giám sát: CloudWatch, CloudTrail, AWS Config — câu hỏi so sánh xuất hiện rất thường xuyên trong đề.
- Biết CloudTrail mặc định giữ Event History 90 ngày, và cách lưu lâu hơn.
- Hiểu các thành phần của CloudWatch: Metrics, Logs, Alarms, Events/EventBridge, Logs Insights.
- Biết chọn đúng công cụ khi đề hỏi "ai đã làm việc này?", "hệ thống đang khỏe không?", "cấu hình có bị đổi không?".

## Lý thuyết chính (tiếng Việt, giữ thuật ngữ English)

### 1. Bộ ba giám sát — Nhìn tổng thể trước

Ba dịch vụ này hay bị nhầm vì đều "ghi lại gì đó", nhưng mỗi dịch vụ trả lời một câu hỏi hoàn toàn khác nhau:

- **CloudWatch:** Hệ thống đang **khỏe hay mệt**? -> metrics, logs, alarms về hiệu năng.
- **CloudTrail:** **Ai** đã làm **gì** trong tài khoản? -> ghi lại API calls, phục vụ audit.
- **AWS Config:** **Cấu hình** của tài nguyên đã **thay đổi ra sao** theo thời gian? Có còn tuân thủ quy định không?

Học thuộc ba câu hỏi này là bạn đã ăn được phần lớn câu hỏi về giám sát trong đề SAA-C03.

### 2. CloudWatch — Giám sát hiệu năng

**Amazon CloudWatch** là dịch vụ monitoring trung tâm của AWS.

**Metrics:** số liệu đo theo thời gian. Ví dụ EC2 có các metric cơ bản như CPUUtilization, NetworkIn, NetworkOut, DiskRead/DiskWrite. Nhiều dịch vụ AWS tự gửi metric về CloudWatch mà bạn không cần cài thêm gì. Metric là dữ liệu dạng số theo chuỗi thời gian — không phải log chữ.

**CloudWatch Logs:** nơi chứa log dạng chữ: log ứng dụng, log hệ thống, log từ Lambda, log VPC Flow Logs... Bạn có thể gửi log từ EC2 (qua agent), từ Lambda (tự động) về đây để tìm kiếm và lưu trữ tập trung thay vì SSH vào từng máy.

**CloudWatch Alarms:** đặt ngưỡng trên một metric. Alarm có các trạng thái chính: **OK** và **ALARM** (ngoài ra còn INSUFFICIENT_DATA khi chưa đủ dữ liệu). Khi vào ALARM, alarm có thể gửi thông báo qua SNS, hoặc kích hoạt hành động như Auto Scaling. Ví dụ: CPU > 80% trong 5 phút -> ALARM -> gửi SNS + scale out.

**CloudWatch Events / Amazon EventBridge:** cơ chế phản ứng theo sự kiện. Một sự kiện xảy ra (EC2 đổi trạng thái, một lịch cron tới hạn) thì kích hoạt target như Lambda, SNS, SQS. **EventBridge** là thế hệ phát triển từ CloudWatch Events, mạnh hơn về tích hợp các ứng dụng SaaS và event bus — đề hiện nay thường dùng tên EventBridge.

**CloudWatch Logs Insights:** công cụ truy vấn log bằng ngôn ngữ query riêng, dùng để phân tích log trong CloudWatch Logs: ví dụ tìm 100 dòng error gần nhất, đếm số request theo từng IP. Nhận diện: đề nhắc "truy vấn / phân tích log" thì nghĩ tới Logs Insights.

### 3. CloudTrail — Ai đã làm gì?

**AWS CloudTrail** ghi lại các **API call** trong tài khoản AWS: ai (user/role nào), làm gì (CreateBucket, TerminateInstances...), khi nào, từ IP nào, thành công hay lỗi. Mọi thao tác qua Console, CLI, SDK đều là API call — nên CloudTrail gần như là camera an ninh của tài khoản.

CloudTrail phục vụ **audit, bảo mật và điều tra sự cố**: "Ai đã xóa cái bucket này?", "Ai vừa sửa Security Group lúc 2 giờ sáng?".

Điểm bắt buộc nhớ:

- Mặc định, CloudTrail cho xem **Event History trong 90 ngày** gần nhất trên console.
- Muốn lưu **lâu hơn 90 ngày**, muốn phân tích hoặc lưu trữ phục vụ compliance, bạn phải **tạo một Trail** và cho nó ghi log ra **S3 bucket** (có thể gửi thêm sang CloudWatch Logs).
- Event History miễn phí có sẵn không thay thế được Trail khi đề yêu cầu lưu trữ dài hạn.

### 4. AWS Config — Lịch sử cấu hình và tuân thủ

**AWS Config** ghi lại **cấu hình (configuration)** của các tài nguyên AWS và sự thay đổi của chúng theo thời gian: Security Group này hôm qua mở port nào, hôm nay ai thêm port 22? Bucket này tuần trước có bật encryption không?

Ngoài ghi lịch sử, Config có **Config Rules**: các quy tắc tuân thủ để kiểm tra cấu hình có đúng chuẩn không, ví dụ:

- Mọi EBS volume phải được mã hóa.
- Mọi S3 bucket không được public.
- Mọi EC2 phải thuộc một VPC chỉ định.

Tài nguyên vi phạm sẽ bị đánh dấu **noncompliant**. Config cũng có thể gắn remediation (tự sửa) qua Systems Manager ở mức nâng cao. Lưu ý: Config ghi lại cấu hình tài nguyên, KHÔNG ghi API call của người dùng — đó là việc của CloudTrail.

## Ví dụ đời thường

Hãy tưởng tượng tài khoản AWS là một tòa nhà văn phòng:

- **CloudWatch** là bảng đồng hồ đo điện, nước và nhiệt độ phòng máy: CPU bao nhiêu phần trăm, RAM còn bao nhiêu, có nóng quá không thì chuông báo (Alarm) reo lên. Nó quan tâm tới **sức khỏe hệ thống**.
- **CloudTrail** là camera an ninh + sổ ghi ra vào: ai quẹt thẻ mở cửa phòng server lúc 2 giờ sáng, ai mang cái ổ cứng ra ngoài. Có chuyện gì thì tua lại camera (audit).
- **AWS Config** là hồ sơ kiểm kê tài sản: cái khóa cửa này tháng trước là khóa cơ, tháng này ai đổi thành khóa vân tay? Danh sách kiểm tra (Config Rules) sẽ báo ngay nếu có phòng nào lắp khóa không đúng chuẩn công ty.

Sự cố thật thường cần cả ba: Alarm của CloudWatch báo database bị xóa (hệ thống mệt), CloudTrail cho biết user nào đã gọi lệnh xóa (ai làm), AWS Config cho biết cấu hình backup của database đó đã bị tắt từ tuần trước (cấu hình đổi thế nào).

## Phân biệt dễ nhầm

### CloudWatch vs CloudTrail vs AWS Config

| Tiêu chí | CloudWatch | CloudTrail | AWS Config |
|---|---|---|---|
| Câu hỏi trả lời | Hệ thống khỏe không? | Ai đã làm gì? | Cấu hình đổi thế nào? |
| Dữ liệu ghi | Metrics, logs, alarms | API calls | Configuration snapshot & thay đổi |
| Mục đích chính | Monitoring hiệu năng | Audit, bảo mật | Tuân thủ (compliance) |
| Ví dụ | CPU vượt 80% | User X gọi TerminateInstances | SG vừa bị mở thêm port 22 |

### CloudWatch Logs vs CloudTrail

Log của CloudTrail là log về API call của tài khoản. Log trong CloudWatch Logs là log ứng dụng/hệ thống. Đừng vì thấy chữ "log" mà gộp hai thứ thành một. Trail có thể *gửi* log của nó *vào* CloudWatch Logs để phân tích, nhưng bản chất hai dịch vụ vẫn khác nhau.

### CloudWatch Alarms vs EventBridge

Alarm phản ứng theo **ngưỡng metric** (CPU > 80%). EventBridge phản ứng theo **sự kiện** (instance vừa chuyển sang trạng thái terminated) hoặc theo lịch. Đề cho ngưỡng số liệu thì chọn Alarm, cho "khi sự kiện X xảy ra thì chạy Lambda" thì chọn EventBridge.

## Bẫy đề thi

1. **"Ai đã xóa / sửa tài nguyên này?"** — Đáp án gần như luôn là **CloudTrail**, không phải CloudWatch.
2. **90 ngày của CloudTrail** — Đề yêu cầu "lưu audit log 1 năm cho compliance": phải tạo **Trail ghi ra S3**. Chỉ trông vào Event History mặc định là sai vì nó chỉ có 90 ngày.
3. **Kiểm tra tuân thủ cấu hình** — "Đảm bảo không bucket nào bị public, phát hiện ngay khi vi phạm" là bài của **AWS Config + Config Rules**, không phải CloudTrail (CloudTrail ghi lại hành động, không đánh giá cấu hình có đúng chuẩn hay không một cách liên tục).
4. **Metric cơ bản của EC2 không có RAM** — Ở mức khái niệm cơ bản, CloudWatch mặc định có CPU, network, disk của EC2; muốn metric chi tiết như memory usage thường phải cài CloudWatch Agent. Đây là chi tiết đề hay gài.
5. **Logs Insights không phải nơi lưu log** — Nơi lưu là CloudWatch Logs; Logs Insights là công cụ *truy vấn* trên log đó.

## Tóm tắt 5 dòng

CloudWatch lo hiệu năng: Metrics (số liệu), Logs (log chữ), Alarms (ngưỡng OK/ALARM), EventBridge (phản ứng theo sự kiện), Logs Insights (truy vấn log).
CloudTrail ghi lại API calls — ai làm gì, lúc nào — phục vụ audit; Event History mặc định chỉ 90 ngày.
Muốn lưu CloudTrail lâu hơn phải tạo Trail ghi log ra S3.
AWS Config ghi lại lịch sử cấu hình tài nguyên và dùng Config Rules để kiểm tra tuân thủ (compliance).
Gặp câu "ai làm" chọn CloudTrail, "khỏe không" chọn CloudWatch, "cấu hình có đổi / có đúng chuẩn không" chọn AWS Config.

## Quiz — 5 câu hỏi tiếng Anh kiểu đề thi (A/B/C/D)

**Question 1:** A security team needs to find out which IAM user terminated a production EC2 instance last night. Which service provides this information?

A. Amazon CloudWatch Metrics
B. AWS CloudTrail
C. AWS Config
D. Amazon VPC Flow Logs

**Question 2:** A company must retain an audit record of all API activity in its AWS account for 1 year for compliance purposes. What should the architect do?

A. Rely on the CloudTrail Event History in the console
B. Create a CloudTrail trail that delivers log files to an Amazon S3 bucket
C. Enable CloudWatch Logs Insights queries on EC2 logs
D. Create an AWS Config rule for API logging

**Question 3:** An operations team wants an alert whenever the average CPU utilization of an EC2 instance stays above 80% for 5 minutes, and a notification must be sent automatically. Which solution meets this requirement?

A. A CloudWatch Alarm on the CPUUtilization metric with an SNS notification action
B. A CloudTrail trail with an S3 bucket
C. An AWS Config rule on the instance
D. A Route 53 Health Check

**Question 4:** A compliance officer wants to be notified whenever an S3 bucket is configured to allow public access, and wants a history of configuration changes for all buckets. Which service should be used?

A. AWS CloudTrail Event History only
B. Amazon CloudWatch Logs
C. AWS Config with config rules
D. AWS Trusted Advisor

**Question 5:** An analyst needs to run queries over application logs stored centrally to count errors per hour and find the most frequent error messages. Which feature should they use?

A. CloudWatch Logs Insights
B. CloudTrail Lake dashboards only in the console home page
C. VPC Flow Logs
D. AWS Config aggregator

## Đáp án quiz

**Câu 1 — Đáp án B.**
Giải thích tiếng Việt: Câu hỏi "ai đã làm gì" là lãnh địa của **CloudTrail** — nó ghi lại API call `TerminateInstances` kèm danh tính IAM user, thời gian và IP nguồn. CloudWatch Metrics chỉ có số liệu hiệu năng, không biết ai bấm nút.

**Câu 2 — Đáp án B.**
Giải thích tiếng Việt: Event History mặc định chỉ giữ **90 ngày**, không đạt yêu cầu 1 năm. Phải tạo **Trail** ghi log ra S3 để lưu trữ dài hạn phục vụ compliance. Đây là bẫy số ngày kinh điển của CloudTrail.

**Câu 3 — Đáp án A.**
Giải thích tiếng Việt: Ngưỡng trên metric (CPU > 80% trong 5 phút) + gửi thông báo là đúng nghiệp vụ của **CloudWatch Alarm** với action là SNS. Các phương án còn lại không theo dõi metric hiệu năng theo ngưỡng.

**Câu 4 — Đáp án C.**
Giải thích tiếng Việt: Kiểm tra cấu hình có tuân thủ chuẩn hay không + lịch sử thay đổi cấu hình là việc của **AWS Config** với Config Rules (ví dụ rule cấm S3 public). CloudTrail ghi hành động của người dùng, không đánh giá trạng thái cấu hình một cách liên tục.

**Câu 5 — Đáp án A.**
Giải thích tiếng Việt: Truy vấn và phân tích log ứng dụng đã lưu trong CloudWatch Logs là chức năng của **CloudWatch Logs Insights**. Flow Logs là metadata traffic mạng, không phải log ứng dụng.
