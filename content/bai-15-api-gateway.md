# Bài 15 — API Gateway: Cổng vào của kiến trúc Serverless

## Mục tiêu bài học

Sau bài này, bạn sẽ có thể:

- Phân biệt REST API, HTTP API và WebSocket API trong Amazon API Gateway theo tính năng, chi phí và use case, chọn đúng loại trong đề thi.
- Giải thích Lambda Proxy Integration và mẫu kiến trúc kinh điển **API Gateway + Lambda**.
- Chọn đúng cơ chế ủy quyền: IAM, Amazon Cognito User Pools, Lambda Authorizer.
- Áp dụng Throttling, API Caching, Usage Plans và API Keys để bảo vệ và tối ưu backend.
- Hiểu vòng đời Stage, Deployment, Stage Variables và nhận diện lỗi 429 / 502 thường gặp ở mức khái niệm.

## Lý thuyết chính

### 1. API Gateway là gì?

Amazon API Gateway là dịch vụ fully managed để tạo, xuất bản, bảo mật và giám sát API ở mọi quy mô. Nó là "cửa trước" (front door): client không gọi thẳng vào Lambda / EC2 / ECS / DynamoDB mà đi qua API Gateway để được xác thực, throttle, cache và validate trước.

```
Mobile / Web Client → API Gateway → Lambda / HTTP backend / AWS service
                         ↑
              Auth, Throttling, Caching, Validation
```

### 2. Ba loại API — Phân biệt cốt lõi

| Tiêu chí | REST API | HTTP API | WebSocket API |
|----------|----------|----------|---------------|
| Tính năng | **Đầy đủ nhất**: API Keys, Usage Plans, Request Validation, Caching, WAF, Canary... | **Thu gọn**: tập trung vào proxy tới Lambda / HTTP backend, hỗ trợ JWT Authorizer | Kết nối hai chiều persistent |
| Chi phí / Độ trễ | Cao hơn, độ trễ cao hơn một chút | **Rẻ hơn** (thấp hơn đáng kể), độ trễ thấp hơn | Tính theo số message + phút kết nối |
| Ủy quyền nổi bật | IAM, Cognito, Lambda Authorizer, Resource Policy | JWT (Cognito, OIDC), Lambda Authorizer, IAM | IAM, Lambda Authorizer |
| Dùng khi nào | Cần kiểm soát chặt: public API có thu phí, cần caching/validation/usage plan | Backend đơn giản cho Lambda, cần rẻ và nhanh, JWT là đủ | Chat, thông báo realtime, game, dashboard live |

**Quy tắc chọn nhanh cho đề thi:**
- Đề nhắc "usage plans, API keys, request validation, API caching, per-client throttling cho khách hàng bên thứ ba" → **REST API**.
- Đề nhắc "chi phí thấp nhất, API đơn giản cho Lambda, xác thực bằng JWT / Cognito / OIDC" → **HTTP API**.
- Đề nhắc "real-time two-way communication, chat application" → **WebSocket API**.

### 3. Lambda Proxy Integration — Mẫu serverless kinh điển

Với **Lambda Proxy Integration** (AWS_PROXY), API Gateway chuyển **toàn bộ** request (method, path, headers, query string, body) thành một JSON event đưa vào Lambda. Lambda trả về JSON gồm `statusCode`, `headers`, `body` và API Gateway biến nó thành HTTP response cho client.

Ưu điểm: không cần viết Mapping Template, Lambda toàn quyền quyết định response. Đây là cách tích hợp mặc định được khuyên dùng và xuất hiện trong hầu hết scenario.

Cách còn lại, **Non-Proxy (Custom) Integration**, dùng Mapping Template (VTL) để biến đổi request/response giữa client và backend — mạnh nhưng phức tạp, thường chỉ cần khi tích hợp trực tiếp với DynamoDB / SQS / EC2 HTTP backend mà không qua Lambda.

**Cặp bài trùng API Gateway + Lambda:**
API Gateway lo phần HTTP (routing, auth, throttle, cache), Lambda lo logic nghiệp vụ, cả hai đều serverless, tự scale và trả tiền theo request. Cộng thêm DynamoDB là thành bộ ba serverless kinh điển của SAA-C03.

> **Tình huống thực tế:** Một startup làm API cho mobile app: `POST /orders` → API Gateway → Lambda tạo đơn → DynamoDB. Lúc 10 user hay 100.000 user, kiến trúc không đổi, không server nào phải vận hành, chi phí tăng tuyến tính theo số request thực tế.

### 4. Ủy quyền và Bảo mật (Authorization)

API Gateway hỗ trợ nhiều cơ chế — đề thi kiểm tra bạn chọn đúng theo loại người dùng:

| Cơ chế | Đối tượng | Mô tả |
|--------|-----------|-------|
| **IAM Authorization** | AWS user/role, ứng dụng trong AWS | Dùng IAM Policy + chữ ký SigV4. Hợp cho API nội bộ, service-to-service trong AWS |
| **Cognito User Pools Authorizer** | Người dùng cuối (end user) | User đăng nhập qua Cognito, gửi JWT (ID Token) trong header, API Gateway tự validate với User Pool |
| **Lambda Authorizer** (trước đây gọi là Custom Authorizer) | Logic tùy biến, hệ thống auth bên ngoài | Một Lambda nhận token, tự kiểm tra (với DB, OAuth bên thứ ba...) và trả về IAM Policy cho phép/chặn. Kết quả được cache theo token để giảm số lần gọi Lambda |
| **JWT Authorizer (HTTP API)** | OIDC provider, Cognito | API Gateway tự validate JWT theo issuer/audience mà không cần Lambda |
| **Resource Policy + API Keys** | Kiểm soát truy cập bổ sung | Resource Policy chặn theo IP/source; API Key định danh client — lưu ý API Key **không phải** cơ chế bảo mật chính, phải kết hợp với Authorizer/Usage Plan |

Các lớp bảo vệ đi kèm: **AWS WAF** gắn vào REST API để chặn tấn công Layer 7, **HTTPS bắt buộc** với certificate ACM, **CORS** cấu hình cho trình duyệt gọi API khác domain.

### 5. Throttling — Chống backend bị quá tải

- **Account-level Throttling:** giới hạn tổng số request/giây trên toàn Region của tài khoản (mặc định ở mức khái niệm là 10.000 RPS với burst bằng token bucket) — bảo vệ toàn hệ thống.
- **Stage / API-level Throttling:** đặt giới hạn riêng cho từng API hoặc từng Stage (ví dụ Stage prod = 1.000 RPS).
- **Usage Plan + API Key (chỉ REST API):** gắn hạn mức riêng cho từng khách hàng: khách Free = 100 request/ngày, quota tháng cố định; khách trả phí = hạn mức cao hơn. Vượt hạn mức, API Gateway trả lỗi **429 Too Many Requests**.
- Throttling ở API Gateway giúp backend (đặc biệt là Lambda có concurrency limit hoặc một hệ thống legacy yếu) không bị dội bom khi traffic tăng đột biến.

### 6. API Caching

- Chỉ có ở **REST API**: bật cache theo từng Stage, API Gateway lưu response trong cache (TTL mặc định 300 giây, cấu hình từ 0–3600 giây).
- Request giống nhau trong TTL sẽ nhận response từ cache mà **không chạm vào backend** → giảm độ trễ, giảm số lần gọi Lambda/EC2, giảm chi phí backend.
- Kích thước cache có nhiều mức trả phí theo giờ. Có thể mã hóa cache và cho phép client bỏ qua cache bằng header khi cần.

> **Tình huống thực tế:** API danh mục sản phẩm ít thay đổi bị gọi 1 triệu lần/ngày làm Lambda và DynamoDB tốn chi phí đọc. Bật API Caching với TTL 300s, 5 phút mới có một request thật sự chạm backend, còn lại trả từ cache.

### 7. Stage, Deployment và Stage Variables

- **Deployment:** một bản snapshot (ảnh chụp) của cấu hình API tại một thời điểm. Sửa API xong phải **deploy lại** thì thay đổi mới có hiệu lực (với REST API).
- **Stage:** một môi trường của bản deployment: `dev`, `test`, `prod`. Mỗi Stage có URL riêng dạng `https://{api-id}.execute-api.{region}.amazonaws.com/{stage}`.
- **Stage Variables:** biến cấu hình theo Stage, ví dụ Stage `prod` trỏ tới Lambda alias prod, Stage `dev` trỏ tới Lambda dev, dùng cùng một API definition cho nhiều môi trường. Cũng dùng để trỏ Canary Deployment.
- **Canary Release Deployment:** phát hành bản mới cho một phần nhỏ traffic (ví dụ 10%) ở Stage prod, theo dõi lỗi rồi mới tăng lên 100% — biết ở mức khái niệm.

### 8. Request Validation và các tính năng REST API khác

- **Request Validation:** API Gateway kiểm tra request (tham số bắt buộc, kiểu dữ liệu theo Model/JSON Schema) và **chặn request sai ngay tại cổng**, backend không tốn công xử lý, trả lỗi 400 cho client.
- **Direct Integration với AWS Services:** API Gateway có thể gọi thẳng DynamoDB, SQS, Step Functions... mà không cần Lambda trung gian.
- **Import/Export API:** định nghĩa API bằng OpenAPI (Swagger), tích hợp với CloudFormation / SAM để quản lý dạng code.

### 9. Lỗi thường gặp ở mức khái niệm

- **429 Too Many Requests:** client vượt Throttling limit (account/stage/usage plan) hoặc Lambda concurrency qua trung gian. Cách xử lý: xem lại limit, yêu cầu tăng quota, thêm exponential backoff + retry phía client.
- **502 Bad Gateway:** thường do Lambda trả response **sai định dạng** của Proxy Integration (thiếu `statusCode`, `body` không phải string JSON hợp lệ), hoặc backend integration lỗi / timeout ở tầng tích hợp. Gặp 502 trong scenario serverless, hãy nghĩ đầu tiên tới định dạng response của Lambda.
- **403 Forbidden:** thiếu/không hợp lệ API Key, Authorizer từ chối, hoặc Resource Policy chặn.
- **504 Gateway Timeout:** backend không trả lời trong giới hạn timeout tích hợp của API Gateway (29 giây cho REST API ở mức khái niệm hay được nhắc) — workload chạy lâu phải chuyển sang mẫu bất đồng bộ: API Gateway → SQS → Lambda xử lý nền, trả job ID cho client poll kết quả.

## Ví dụ đời thường

Hãy hình dung API Gateway là **lễ tân kiêm bảo vệ của một tòa nhà văn phòng**:

- Khách (client) không tự đi thẳng vào phòng ban (Lambda, EC2) mà phải qua quầy lễ tân.
- Lễ tân kiểm tra **giấy tờ** trước: thẻ nhân viên nội bộ (IAM), thẻ cư dân đã đăng ký (Cognito), hoặc gọi cho một người chuyên xác minh khách lạ (Lambda Authorizer).
- Lễ tân giới hạn **lượt khách** mỗi giờ để tòa nhà không quá tải (Throttling); khách VIP mua gói dịch vụ được ưu tiên nhiều lượt hơn (Usage Plans + API Keys).
- Câu hỏi nào ngày nào cũng có người hỏi giống hệt (danh sách phòng ban) thì lễ tân **trả lời từ sổ tay có sẵn** thay vì gọi điện vào trong làm phiền (API Caching).
- Lễ tân cũng **kiểm tra hồ sơ ngay tại quầy**: thiếu giấy tờ thì trả về luôn, không chuyển vào trong (Request Validation).
- Tòa nhà có nhiều **khu vực theo giai đoạn** (Stage): khu thử nghiệm `dev` và khu chính thức `prod` — cùng một lễ tân nhưng dẫn khách tới đúng khu nhờ biển chỉ dẫn (Stage Variables).

## Phân biệt dễ nhầm

**1. REST API vs HTTP API**
- REST API: đầy đủ tính năng — Caching, Usage Plans, API Keys, Request Validation, WAF tích hợp chặt. Đắt hơn.
- HTTP API: rẻ hơn, nhanh hơn, ít tính năng hơn — không có Usage Plans/API Keys và Caching tích hợp kiểu REST. Hợp nhất với Lambda + JWT.
- Bẫy: đề yêu cầu "API keys and usage plans for third-party developers" mà chọn HTTP API là sai.

**2. Cognito User Pools Authorizer vs Lambda Authorizer**
- Cognito: user của bạn đăng nhập bằng hệ thống user pool có sẵn, API Gateway tự validate JWT — không cần viết code auth.
- Lambda Authorizer: logic xác thực **tùy biến** hoặc nằm ở hệ thống bên ngoài AWS (OAuth provider riêng, database token riêng) — bạn tự viết Lambda kiểm tra và trả về Policy.

**3. API Key vs Authorization**
- API Key chỉ để **định danh và áp Usage Plan** (biết client nào gọi, tính quota). Nó **không phải** là cơ chế bảo mật/ủy quyền thực sự. Luôn phải kết hợp API Key với IAM / Cognito / Lambda Authorizer.

**4. Throttling ở API Gateway vs Lambda Concurrency**
- API Gateway Throttling chặn request ở cổng theo RPS/quota.
- Lambda Reserved/Provisioned Concurrency giới hạn số execution đồng thời ở phía compute.
- Lỗi 429 có thể đến từ một trong hai nơi — đọc kỹ scenario xem giới hạn nằm ở tầng nào.

**5. API Caching vs Backend Caching (ElastiCache / DynamoDB DAX)**
- API Caching lưu **HTTP response** ngay tại API Gateway, backend hoàn toàn không bị gọi.
- ElastiCache/DAX lưu dữ liệu ở tầng data, backend vẫn bị gọi nhưng đọc data nhanh hơn. Hai lớp này bổ sung nhau, không thay thế nhau.

**6. Stage vs Deployment**
- Deployment là **bản chụp cấu hình**, Stage là **môi trường trỏ tới một Deployment**. Sửa API mà không deploy lại thì Stage vẫn chạy bản cũ — nguồn gốc của nhiều câu "đã sửa nhưng không có tác dụng".

## Bẫy đề thi

1. **Workload chạy lâu qua API Gateway đồng bộ.** Tác vụ xử lý 5 phút gắn thẳng sau REST API sẽ dính timeout và trả 504. Mẫu đúng: API Gateway nhận request → đẩy vào SQS / khởi động Step Functions → trả về 202 + job ID ngay, client kiểm tra kết quả sau.

2. **Chọn HTTP API vì rẻ nhưng đề lại yêu cầu Usage Plans.** Tiết kiệm chi phí không thắng được yêu cầu tính năng: Usage Plans, API Keys, Request Validation, API Caching chỉ có đầy đủ ở REST API.

3. **Coi API Key là bảo mật.** Scenario "API bị truy cập trái phép dù đã bật API Key" — vì API Key bị lộ/dùng chung và không có Authorizer. Đáp án đúng luôn bổ sung cơ chế ủy quyền thật.

4. **Lỗi 502 mà đi sửa Throttling.** 502 trong cặp API Gateway + Lambda Proxy gần như luôn do Lambda trả sai format (body không phải string, thiếu statusCode, ném exception không bắt). 429 mới là bài toán throttling/quota.

5. **Quên deploy sau khi sửa API (REST).** Thay đổi Method/Integration/Authorizer chỉ là bản nháp cho tới khi tạo Deployment mới vào Stage. Đề hay cài chi tiết này trong scenario "đã cấu hình đúng nhưng client vẫn nhận hành vi cũ".

6. **Dùng Lambda Authorizer cho mọi request mà quên cache.** Lambda Authorizer có kết quả được cache theo token (TTL cấu hình được) để tránh gọi Lambda xác thực cho từng request — chi tiết giúp giảm chi phí và độ trễ, hay xuất hiện trong đáp án tối ưu.

7. **WebSocket bị nhầm với HTTP thường.** Yêu cầu chat realtime, thông báo đẩy hai chiều liên tục mà chọn REST/HTTP API polling là sai cả về kiến trúc lẫn chi phí — phải là WebSocket API.

8. **Caching cho dữ liệu nhạy cảm theo user.** API Cache dùng chung theo cache key; nếu cấu hình sai, response của user này có thể trả cho user khác. Scenario dữ liệu cá nhân/thay đổi liên tục → tắt cache hoặc thiết kế cache key cẩn thận, và cân nhắc TTL ngắn.

## Tóm tắt 5 dòng

1. API Gateway là front door có quản lý cho backend: REST API đầy đủ tính năng nhất (caching, usage plans, API keys, request validation), HTTP API rẻ và nhanh hơn cho Lambda/JWT, WebSocket API cho giao tiếp hai chiều realtime.
2. Lambda Proxy Integration chuyển toàn bộ request cho Lambda quyết định response, tạo thành cặp serverless kinh điển API Gateway + Lambda (+ DynamoDB).
3. Ủy quyền gồm IAM cho nội bộ AWS, Cognito User Pools cho end user, Lambda Authorizer cho logic xác thực tùy biến/bên ngoài; API Key chỉ định danh và áp quota chứ không phải bảo mật.
4. Throttling ở mức account và stage cùng Usage Plans bảo vệ backend và chia hạn mức theo khách hàng; API Caching (TTL mặc định 300s) giảm tải và độ trễ cho backend.
5. Deployment là bản chụp cấu hình, Stage là môi trường (dev/prod) với Stage Variables riêng; lỗi 429 là vượt throttling/quota, 502 thường do Lambda Proxy trả sai định dạng response.

## Quiz — 5 câu hỏi tiếng Anh kiểu đề thi

**Question 1.** A company plans to sell access to a public API to third-party developers. It must issue keys to identify each developer, enforce different daily quotas and throttling limits per developer plan, and validate incoming requests against a defined schema before they reach the backend. Which type of API in Amazon API Gateway should the solutions architect choose?

A. HTTP API with a JWT authorizer
B. WebSocket API with an IAM authorizer
C. REST API with usage plans, API keys, and request validation
D. HTTP API with a Lambda authorizer

**Question 2.** A startup is building a simple mobile backend using AWS Lambda and Amazon DynamoDB. Users sign in with a third-party OpenID Connect provider that issues JWT tokens. The company wants the lowest cost and lowest latency, and does not need API keys, usage plans, or API caching. Which API type is the best choice?

A. REST API
B. HTTP API
C. WebSocket API
D. REST API with a private integration

**Question 3.** Users of a serverless application receive intermittent 502 Bad Gateway errors from an API Gateway REST API that uses Lambda proxy integration. The Lambda function runs without errors in its own tests, but returns a JSON object directly as its result without statusCode and with a non-string body. What is the MOST likely cause of the 502 errors?

A. The API has exceeded its account-level throttling limit
B. The Lambda function's response does not match the proxy integration output format
C. The API cache TTL is set too low
D. The Cognito user pool authorizer token has expired

**Question 4.** A product catalog API receives over a million requests per day, but the catalog changes only a few times per day. The backend Lambda function and database are under heavy read load, and most responses are identical. Which API Gateway feature will MOST effectively reduce backend load and response latency?

A. Enable API caching on the stage with an appropriate TTL
B. Increase the stage-level throttling limit
C. Add a Lambda authorizer to the method
D. Deploy the API to an additional stage

**Question 5.** A company uses API Gateway and Lambda for its public API. During a marketing campaign, traffic spikes tenfold and legitimate users start receiving HTTP 429 errors, while the company also wants to protect a fragile legacy backend from being overwhelmed. Which actions should the solutions architect take? (Choose the best single answer.)

A. Disable throttling entirely so no user receives a 429 error
B. Review and raise the API throttling limits where appropriate, and keep usage-plan throttling in place to protect the backend
C. Replace the REST API with a WebSocket API
D. Turn off the Lambda authorizer and remove all API keys

## Đáp án quiz

**Question 1 — Đáp án: C**
Giải thích: Bộ yêu cầu "API keys + quotas/throttling theo từng gói khách hàng (usage plans) + request validation theo schema" là tính năng đặc trưng chỉ có đầy đủ ở REST API. HTTP API không hỗ trợ usage plans và API keys, WebSocket API dùng cho giao tiếp hai chiều chứ không phải quản lý API công khai kiểu này.

**Question 2 — Đáp án: B**
Giải thích: HTTP API được thiết kế cho kịch bản Lambda proxy đơn giản với JWT Authorizer (Cognito/OIDC), chi phí và độ trễ thấp hơn REST API. Vì đề nói rõ không cần API keys, usage plans hay caching nên không có lý do trả thêm tiền cho REST API.

**Question 3 — Đáp án: B**
Giải thích: Với Lambda Proxy Integration, Lambda bắt buộc trả về đúng định dạng gồm `statusCode`, `headers` và `body` dạng string. Trả sai định dạng, API Gateway không dựng được HTTP response và trả 502 Bad Gateway. Lỗi vượt throttling sẽ là 429, không phải 502.

**Question 4 — Đáp án: A**
Giải thích: Dữ liệu ít thay đổi mà bị đọc cực nhiều là ca kinh điển của API Caching: bật cache ở Stage với TTL phù hợp (mặc định 300 giây), phần lớn request được trả ngay từ cache, Lambda và database gần như không bị chạm vào. Tăng throttling chỉ cho phép thêm tải vào backend, đi ngược yêu cầu giảm tải.

**Question 5 — Đáp án: B**
Giải thích: Lỗi 429 nghĩa là đã chạm giới hạn throttling. Xử lý đúng là rà soát và nâng giới hạn ở mức account/stage cho phù hợp tải thật, đồng thời vẫn giữ throttling theo usage plan để bảo vệ backend legacy mong manh. Tắt hẳn throttling (A) sẽ khiến backend bị dội sập, đúng điều công ty muốn tránh.
