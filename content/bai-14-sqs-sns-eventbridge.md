# Bài 14 — SQS, SNS & EventBridge: Decoupling và Event-Driven Architecture

## Mục tiêu bài học

Sau bài này, bạn sẽ có thể:

- Phân biệt SQS Standard và SQS FIFO về thứ tự, tính duy nhất, throughput và use case, tính được giới hạn 300 TPS / 3.000 TPS.
- Giải thích Visibility Timeout, Message Retention, Dead Letter Queue (DLQ), Long Polling và dùng chúng để xử lý message lỗi an toàn.
- Thiết kế kiến trúc **decouple** các tầng bằng SQS và mẫu **Fanout** bằng SNS → nhiều SQS Queue.
- Phân biệt SNS, SQS và EventBridge theo cơ chế push/pull, routing và nguồn sự kiện; biết khi nào dùng EventBridge Rules, Schedule và Schema Registry.
- Nhận diện vị trí của Step Functions như một lớp điều phối (orchestration) ở mức giới thiệu.

## Lý thuyết chính

### 1. Vì sao cần Decoupling?

Kiến trúc nối cứng (tightly coupled): Web Server gọi thẳng Processing Server. Processing Server chậm hoặc chết → Web Server chết theo, request của user bị mất, không scale độc lập được.

Kiến trúc tách rời (decoupled): Web Server chỉ việc ném công việc vào một hàng đợi rồi trả lời user ngay. Processing Server rảnh lúc nào thì lấy việc ra làm lúc đó, chết thì message vẫn nằm trong queue chờ.

Bộ ba SQS / SNS / EventBridge là trọng tâm của mọi câu hỏi decoupling trong SAA-C03.

### 2. Amazon SQS — Simple Queue Service

SQS là hàng đợi message được quản lý hoàn toàn (fully managed), tồn tại độc lập với compute. Producer gửi message vào Queue, Consumer **poll** (kéo) message ra xử lý rồi xóa message.

#### SQS Standard vs SQS FIFO

| Tiêu chí | SQS Standard | SQS FIFO |
|----------|--------------|----------|
| Thứ tự (Ordering) | Best-effort — cố gắng giữ thứ tự nhưng không đảm bảo | Đảm bảo nghiêm ngặt theo thứ tự gửi trong cùng Message Group |
| Tính duy nhất (Delivery) | **At-least-once** — một message có thể được giao hơn một lần | **Exactly-once processing** — deduplication trong cửa sổ 5 phút |
| Throughput | Gần như không giới hạn (nearly unlimited TPS) | **300 TPS** khi không batch, **3.000 TPS** khi batch (10 message/lần) |
| Tên Queue | Tên tự do | Bắt buộc có hậu tố `.fifo` |
| Use case | Hầu hết workload: xử lý ảnh, order, log — nơi thứ tự không quan trọng tuyệt đối | Giao dịch tài chính, trừ tiền, đặt vé theo thứ tự — sai thứ tự là sai tiền |

Hai khái niệm FIFO cần nhớ thêm ở mức khái niệm: **Message Group ID** (thứ tự chỉ đảm bảo trong cùng một group, các group khác nhau chạy song song) và **Deduplication ID** (chìa khóa chống trùng).

#### Các tham số SQS sống còn trong đề thi

**Visibility Timeout:**
- Khi một Consumer nhận message, message đó **không biến mất** mà bị ẩn khỏi các Consumer khác trong khoảng Visibility Timeout.
- **Mặc định 30 giây, tối đa 12 giờ.**
- Consumer xử lý xong phải chủ động gọi DeleteMessage trước khi hết timeout. Nếu xử lý chưa xong mà timeout đã hết, message **hiện lại** trong queue và Consumer khác có thể nhận trùng → đây chính là cơ chế at-least-once của Standard.
- Xử lý lâu hơn timeout → tăng Visibility Timeout hoặc dùng ChangeMessageVisibility để gia hạn trong lúc xử lý.

> **Bẫy kinh điển:** Video transcode mất 15 phút nhưng Visibility Timeout để 30 giây → cùng một video bị 5 worker xử lý trùng, tốn tiền và ghi đè kết quả. Đáp án: tăng Visibility Timeout lên lớn hơn thời gian xử lý tối đa.

**Message Retention Period:**
Message nằm trong queue tối đa **14 ngày** (mặc định 4 ngày). Quá hạn chưa ai xử lý thì bị xóa. Đề hỏi "message không được phép mất trong 10 ngày chờ xử lý" → đặt retention = 14 ngày là đáp án an toàn.

**Dead Letter Queue (DLQ):**
- Queue phụ chuyên chứa message xử lý thất bại nhiều lần.
- Tham số **maxReceiveCount**: một message bị nhận quá số lần này (ví dụ 3 lần) mà vẫn không bị xóa (tức xử lý vẫn fail) → SQS tự chuyển nó sang DLQ.
- DLQ giúp: không để "message độc" (poison message) kẹt vòng lặp vô hạn trong queue chính, đồng thời giữ lại để kỹ sư debug và redrive (đẩy lại) sau khi sửa lỗi.
- DLQ của FIFO Queue phải là FIFO Queue, DLQ của Standard phải là Standard.

**Long Polling vs Short Polling:**
- **Short Polling (mặc định):** Consumer hỏi liên tục, SQS trả lời ngay dù queue rỗng → nhiều empty response, tốn request và chi phí.
- **Long Polling:** đặt **WaitTimeSeconds** (tối đa 20 giây) — SQS chờ cho tới khi có message hoặc hết thời gian chờ mới trả lời. Giảm số request rỗng, giảm chi phí, giảm CPU cho Consumer. Đề thi cứ nhắc "reduce cost / reduce empty responses / reduce number of API calls" → **bật Long Polling**.

**Các điểm khác:**
- Message size tối đa 256 KB; message lớn hơn thì lưu vào S3 và gửi pointer (mẫu Extended Client Library) — biết ở mức khái niệm.
- SQS scale tự động theo throughput, không cần provision capacity.
- Mã hóa SSE-SQS / SSE-KMS, IAM Policy và Queue Policy kiểm soát ai được Send/Receive.

> **Tình huống thực tế:** Website bán vé concert: tầng web nhận 50.000 order trong 5 phút nhưng tầng thanh toán chỉ xử lý được 2.000 order/phút. Đặt SQS ở giữa: web ghi order vào queue và báo "đã ghi nhận", tầng thanh toán tiêu thụ dần trong 25 phút. Không sập hệ thống, không mất order nào, hai tầng scale độc lập. Đây là đáp án mẫu cho mọi câu "spikes, decouple, buffer, smooth traffic".

### 3. Amazon SNS — Simple Notification Service

SNS là dịch vụ **Pub/Sub** kiểu **push**: Publisher gửi một message vào một **Topic**, SNS lập tức **đẩy** message tới mọi Subscriber của Topic đó.

**Các loại Subscriber:**
- SQS Queue, Lambda Function, HTTP/HTTPS Endpoint
- Email, SMS
- Mobile Push Notification (APNS, FCM...)

**Đặc điểm:**
- Khác SQS ở chỗ Consumer **không phải poll** — SNS chủ động push.
- Một message gửi vào Topic sẽ được nhân bản tới **mọi** Subscriber.
- SNS Standard Topic: thứ tự best-effort, at-least-once. SNS FIFO Topic: giữ thứ tự + deduplication, **nhưng chỉ pair được với SQS FIFO Queue** làm Subscriber — không pair được với Lambda/Email như cách dùng thông thường của FIFO.
- **Message Filtering Policy:** Subscriber có thể khai báo chỉ nhận message có attribute khớp (ví dụ chỉ nhận order có `status = "paid"`), giảm xử lý thừa.

#### Mẫu Fanout — Mẫu kiến trúc kinh điển của bài này

```
                    ┌──→ SQS Queue 1 → Lambda xử lý kho
Producer → SNS Topic┼──→ SQS Queue 2 → Lambda gửi email / hóa đơn
                    └──→ SQS Queue 3 → Lambda phân tích dữ liệu
```

Một sự kiện "OrderPlaced" được phát một lần, **nhiều hệ thống độc lập cùng nhận và xử lý song song**. Thêm hệ thống mới chỉ cần subscribe thêm một Queue, không sửa Producer.

Vì sao Fanout dùng **SNS + SQS** thay vì SNS gọi thẳng Lambda? Vì SQS đóng vai trò bộ đệm bền vững: Lambda/consumer sập hoặc quá tải, message vẫn nằm trong Queue kèm DLQ và cơ chế retry có kiểm soát, không mất sự kiện. Đề thi rất thích chi tiết này.

> **Tình huống thực tế:** Hệ thống e-commerce: khi đơn hàng được tạo, kho phải trừ tồn, kế toán phải xuất hóa đơn, marketing phải gửi email, data team phải ghi nhận. Dùng Fanout SNS → 4 SQS Queue, 4 team xử lý độc lập, một team sập không ảnh hưởng ba team còn lại.

### 4. Amazon EventBridge

EventBridge là **Event Bus** không máy chủ, là bước tiến hóa của CloudWatch Events.

**Khái niệm cốt lõi:**
- **Event Bus:** kênh trung tâm nhận sự kiện. Có Default Bus (sự kiện từ AWS services), Custom Bus (ứng dụng của bạn), Partner Bus (từ SaaS bên thứ ba).
- **Rule:** khớp sự kiện theo **Event Pattern** (nội dung JSON của sự kiện: source, detail-type, giá trị các field...) rồi chuyển tới Target. Một Rule có tối đa 5 Target ở mức khái niệm cơ bản.
- **Target:** Lambda, SQS, SNS, Step Functions, ECS Task, API Destination (HTTP endpoint bên ngoài), v.v.
- **Schedule:** Rule chạy theo lịch kiểu **cron** hoặc **rate** (ví dụ rate(1 hour), cron lúc 8h sáng thứ Hai) — thay thế được CloudWatch Events Scheduled Rule và một phần nhu cầu cron job đơn giản.
- **Schema Registry:** lưu trữ và khám phá cấu trúc (schema) của các loại sự kiện trên bus, giúp developer biết sự kiện trông như thế nào và sinh code binding. Biết ở mức khái niệm.
- **Archive & Replay:** lưu trữ sự kiện và phát lại (replay) vào Target — hữu ích khi sửa bug xong muốn xử lý lại sự kiện cũ. Biết ở mức khái niệm.
- **Tích hợp SaaS:** nhận sự kiện trực tiếp từ các đối tác như Zendesk, Datadog, Shopify... mà không cần tự viết polling.

**EventBridge khác SQS/SNS ở điểm nào?**
- Routing **theo nội dung sự kiện** (content-based routing) chi tiết tới từng field trong JSON, mạnh hơn SNS Filtering và vượt xa SQS (SQS không routing, chỉ là hàng đợi).
- Nguồn sự kiện phong phú: mọi AWS service phát sự kiện có cấu trúc về EventBridge (EC2 đổi trạng thái, S3 object tạo mới qua EventBridge, CodePipeline đổi stage...).
- Có lịch (schedule) tích hợp, có Schema Registry, có khả năng gửi tới API bên ngoài AWS.

> **Tình huống thực tế:** Yêu cầu "khi EC2 instance chuyển sang trạng thái terminated, hãy gửi cảnh báo vào SQS và chạy Lambda dọn dẹp; đồng thời mỗi sáng 7h chạy một Lambda tổng hợp báo cáo". Cả hai đều làm bằng EventBridge: một Rule theo Event Pattern trạng thái EC2, một Rule theo Schedule cron.

### 5. Step Functions — Nhắc ở mức giới thiệu

AWS Step Functions là **State Machine** điều phối nhiều Lambda / AWS service thành một workflow có thứ tự, có rẽ nhánh, chạy song song, retry và xử lý lỗi theo từng bước.

Khác biệt cốt lõi: SQS/SNS/EventBridge là **truyền sự kiện** (choreography — các thành phần tự phản ứng), còn Step Functions là **điều phối tập trung** (orchestration — một bộ não điều khiển trình tự). Scenario mô tả "quy trình nhiều bước có thứ tự, chờ duyệt của con người, retry theo bước" → nghĩ tới Step Functions.

## Ví dụ đời thường

Hãy hình dung một **bưu điện và hệ thống thông báo khu phố**:

- **SQS** là **hộp thư chờ** của một cửa hàng sửa xe. Khách để xe và phiếu yêu cầu vào hàng chờ, thợ rảnh thì lấy phiếu ra sửa. Phiếu "biến mất tạm thời" khi một thợ đang cầm (Visibility Timeout) để thợ khác không sửa trùng chiếc xe. Phiếu nào thợ bó tay 3 lần thì bỏ sang một hộp riêng "xe khó" (DLQ) cho tổ trưởng xem.
- **Long Polling** là thợ đứng chờ ở quầy, nhân viên tiếp tân bảo "anh ngồi chờ, có phiếu mới em gọi" thay vì thợ cứ 5 giây chạy ra hỏi "có việc chưa?" tốn sức cả hai bên.
- **SNS** là **loa phường**: phường phát một thông báo, mọi nhà đăng ký nghe đều nhận cùng lúc. Phường không chờ từng nhà tới hỏi (push, không phải poll).
- **Fanout SNS → SQS** là loa phường thông báo "ngày mai cắt điện", nhưng mỗi đội (điện lực, nước, trường học) đều **ghi thông báo vào sổ việc riêng** của mình để xử lý theo tốc độ riêng — ai bận thì việc vẫn nằm trong sổ, không trôi mất.
- **EventBridge** là **trung tâm điều phối thông minh có lịch**: nó không chỉ phát loa, mà còn đọc nội dung — "nếu là thông báo cháy thì gọi đội cứu hỏa, nếu là lịch tiêm chủng thì nhắn trường học" (routing theo nội dung), và tự phát thông báo định kỳ 7h sáng mỗi ngày (schedule).

## Phân biệt dễ nhầm

**1. SQS vs SNS**
- SQS = Queue, **pull/poll**, 1 message chỉ 1 consumer xử lý, có lưu trữ chờ tới 14 ngày — để **decouple và làm bộ đệm**.
- SNS = Pub/Sub, **push**, 1 message tới **nhiều** subscriber cùng lúc, không lưu trữ chờ lâu dài — để **phát tán thông báo**.
- Cần cả hai (một sự kiện cho nhiều bên, mỗi bên xử lý độc lập và không được mất) → Fanout.

**2. SQS Standard vs SQS FIFO**
- Standard: at-least-once (có thể trùng), best-effort order, throughput gần như vô hạn.
- FIFO: exactly-once, đúng thứ tự, nhưng giới hạn 300 TPS (không batch) / 3.000 TPS (có batch), tên queue phải có `.fifo`.
- Consumer của Standard **bắt buộc phải idempotent** (xử lý trùng vẫn cho kết quả đúng) vì message có thể đến hai lần.

**3. SNS FIFO vs SNS Standard**
- SNS FIFO Topic **chỉ** gửi được tới **SQS FIFO Queue**. Cần thứ tự đầu-cuối thì cả chuỗi phải là FIFO: FIFO Topic → FIFO Queue.
- Gửi thông báo tới Email/SMS/Mobile Push thông thường thì dùng SNS Standard.

**4. EventBridge vs SNS**
- Cả hai đều phát sự kiện tới nhiều đích. EventBridge thắng ở: routing theo nội dung JSON chi tiết, event bus tách theo ứng dụng, schedule cron/rate, Schema Registry, tích hợp SaaS và replay sự kiện.
- SNS thắng ở: đơn giản, độ trễ push thấp, gửi trực tiếp SMS/Email/Mobile Push cho người dùng cuối.

**5. Visibility Timeout vs Message Retention**
- Visibility Timeout (30 giây mặc định, tối đa 12 giờ): message **đang bị một consumer giữ** thì ẩn bao lâu.
- Retention (tối đa 14 ngày): message **nằm chờ trong queue** được bao lâu trước khi bị xóa.
- Nhầm hai con số này là bẫy trắc nghiệm kinh điển.

**6. DLQ vs Queue chính**
- DLQ không phải nơi xử lý nghiệp vụ — nó là nơi **cách ly message độc** sau khi vượt `maxReceiveCount` lần nhận thất bại, phục vụ debug và redrive.

## Bẫy đề thi

1. **Chọn FIFO khi cần throughput cực cao.** Đề cho "hàng chục nghìn message/giây, thứ tự không quan trọng" mà chọn FIFO là sai vì FIFO chạm trần 300/3.000 TPS. Đáp án đúng là Standard.

2. **Quên tính idempotent cho SQS Standard.** Vì at-least-once, message chắc chắn có lúc bị giao trùng. Kiến trúc đúng phải xử lý trùng an toàn (ví dụ kiểm tra Order ID trong DynamoDB trước khi trừ tiền lần nữa).

3. **Visibility Timeout ngắn hơn thời gian xử lý.** Triệu chứng: cùng một job bị xử lý nhiều lần đồng thời, log trùng lặp. Cách sửa: tăng Visibility Timeout hoặc gia hạn bằng ChangeMessageVisibility, không phải tăng số consumer.

4. **Dùng SNS một mình khi không được phép mất sự kiện.** SNS push mà subscriber đang sập và không có SQS đệm thì sự kiện có nguy cơ mất / khó retry có kiểm soát. Yêu cầu "không mất, xử lý độc lập, có retry và DLQ" → Fanout SNS → SQS.

5. **Nhầm SNS FIFO pair với mọi subscriber.** SNS FIFO Topic chỉ pair với SQS FIFO. Đề bẫy bằng phương án "SNS FIFO Topic → Lambda để đảm bảo thứ tự" — không phải cặp được hỗ trợ cho đảm bảo FIFO end-to-end.

6. **Dùng SQS cho bài toán broadcast.** Một message trong SQS chỉ được **một** consumer lấy đi. Muốn 5 hệ thống cùng nhận 1 sự kiện thì phải qua SNS/EventBridge phân phát ra 5 Queue, không phải cho 5 consumer cùng poll một Queue.

7. **Quên Long Polling khi đề nhắc chi phí.** "Hàng triệu empty responses, hóa đơn Lambda/polling cao" → WaitTimeSeconds > 0 (Long Polling), đáp án rất hay lặp lại.

8. **EventBridge Schedule bị quên.** Cần chạy tác vụ theo cron trên AWS mà không muốn duy trì EC2 chạy crontab → EventBridge Scheduler / EventBridge Rule với cron/rate expression gọi Lambda.

## Tóm tắt 5 dòng

1. SQS là hàng đợi pull dùng để decouple các tầng: Standard at-least-once, thứ tự best-effort, throughput gần như vô hạn; FIFO exactly-once, đúng thứ tự, giới hạn 300 TPS không batch và 3.000 TPS có batch.
2. Visibility Timeout mặc định 30 giây (tối đa 12 giờ) ẩn message đang được xử lý, Retention tối đa 14 ngày, DLQ với maxReceiveCount cách ly message độc, Long Polling (WaitTimeSeconds) giảm request rỗng và chi phí.
3. SNS là pub/sub kiểu push tới SQS, Lambda, Email, SMS, Mobile Push; SNS FIFO Topic chỉ pair với SQS FIFO Queue.
4. Mẫu Fanout SNS → nhiều SQS Queue cho phép một sự kiện được nhiều hệ thống xử lý song song, độc lập, bền vững nhờ bộ đệm và DLQ của SQS.
5. EventBridge là event bus với routing theo nội dung sự kiện, nguồn sự kiện phong phú từ AWS và SaaS, lịch cron/rate và Schema Registry; Step Functions là lớp điều phối workflow nhiều bước ở tầng trên.

## Quiz — 5 câu hỏi tiếng Anh kiểu đề thi

**Question 1.** A financial application processes stock trade orders. The order in which trades are received must be strictly preserved, and each trade must be processed exactly once without duplicates. Throughput is moderate at about 200 transactions per second. Which Amazon SQS queue type should the solutions architect use?

A. SQS Standard queue with Long Polling enabled
B. SQS FIFO queue
C. SQS Standard queue with a Dead Letter Queue
D. Amazon SNS Standard topic

**Question 2.** A video processing application uses an SQS queue to trigger workers. Each video takes up to 15 minutes to transcode, but the same video is often processed by multiple workers at the same time, causing wasted compute and overwritten outputs. What is the MOST likely cause and solution?

A. The message retention period is too short; increase it to 14 days
B. Short Polling is enabled; enable Long Polling instead
C. The visibility timeout is shorter than the processing time; increase the visibility timeout
D. The queue is a Standard queue; migrate it to an SNS topic

**Question 3.** An e-commerce company needs an OrderPlaced event to be processed independently by the inventory system, the billing system, and the analytics system. Each system must be able to process events at its own pace, no event must be lost if a system is temporarily down, and failed events must be captured for investigation. Which architecture meets these requirements?

A. Publish events to an SNS topic with Lambda functions subscribed directly for each system
B. Send events to a single SQS Standard queue polled by all three systems
C. Publish events to an SNS topic with a separate SQS queue subscribed for each system, each with its own Dead Letter Queue
D. Use an EventBridge rule that sends every event to a single Lambda function that calls all three systems synchronously

**Question 4.** A company uses SQS to decouple a web tier from a processing tier. The processing tier polls the queue continuously and the company notices a large number of empty responses and unnecessary API costs. Which change will reduce these costs?

A. Decrease the visibility timeout to 0 seconds
B. Enable Long Polling by setting WaitTimeSeconds to 20
C. Reduce the message retention period to 1 day
D. Configure a Dead Letter Queue with maxReceiveCount set to 3

**Question 5.** A solutions architect needs a service that routes events based on the detailed content of each event's JSON fields, receives events natively from many AWS services and third-party SaaS applications, and also runs a Lambda function on a cron schedule. Which service should the architect choose?

A. Amazon SNS with message filtering policies
B. Amazon SQS Standard with scheduled polling
C. Amazon EventBridge with rules, event patterns, and scheduled rules
D. AWS Step Functions with a Wait state

## Đáp án quiz

**Question 1 — Đáp án: B**
Giải thích: Yêu cầu "strictly preserved order + exactly-once + throughput 200 TPS" khớp chính xác với SQS FIFO (giới hạn 300 TPS không batch nên 200 TPS vẫn đáp ứng được). Standard chỉ at-least-once và thứ tự best-effort nên có thể trùng và sai thứ tự — không chấp nhận được với giao dịch tài chính.

**Question 2 — Đáp án: C**
Giải thích: Khi Visibility Timeout (mặc định 30 giây) hết trước khi worker xử lý xong 15 phút, message hiện lại trong queue và worker khác nhận trùng. Cách sửa là tăng Visibility Timeout lớn hơn thời gian xử lý tối đa (hoặc gia hạn trong lúc chạy). Retention, Long Polling không liên quan tới lỗi xử lý trùng này.

**Question 3 — Đáp án: C**
Giải thích: Đây là mẫu Fanout kinh điển: SNS nhân bản sự kiện ra 3 SQS Queue riêng. Mỗi hệ thống xử lý theo tốc độ riêng (decouple), Queue lưu sự kiện khi hệ thống sập nên không mất, DLQ bắt sự kiện lỗi để điều tra. Phương án B sai vì một message trong một Queue chỉ được một consumer lấy; phương án A thiếu bộ đệm bền vững và DLQ cho từng hệ thống.

**Question 4 — Đáp án: B**
Giải thích: Long Polling với WaitTimeSeconds (tối đa 20 giây) khiến SQS chờ tới khi có message mới trả lời, cắt giảm mạnh số empty response và chi phí API so với Short Polling hỏi liên tục. Các phương án còn lại thay đổi timeout/retention/DLQ, không tác động tới số lần poll rỗng.

**Question 5 — Đáp án: C**
Giải thích: Content-based routing theo từng field JSON, nguồn sự kiện phong phú từ AWS + SaaS, Schema Registry và lịch cron/rate là bộ tính năng định danh của EventBridge. SNS Filtering đơn giản hơn và không có bus/schedule/schema như EventBridge; Step Functions là điều phối workflow chứ không phải event bus.
