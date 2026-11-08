# Bài 16 — CloudFormation: Infrastructure as Code trên AWS

## Mục tiêu bài học

Sau bài này, bạn sẽ có thể:

- Giải thích Infrastructure as Code (IaC) và vai trò của AWS CloudFormation: Template, Stack, Change Sets, Stack Policies, Drift Detection.
- Cấu trúc một Template YAML/JSON, biết **Resources là phần bắt buộc duy nhất**, và dùng được các Intrinsic Functions cốt lõi: Ref, Fn::GetAtt, Fn::Sub, Fn::ImportValue.
- Dùng Outputs và Cross-Stack References để chia sẻ giá trị giữa các Stack an toàn.
- Hiểu cfn-init / cfn-signal Helper Scripts cho EC2 và Nested Stacks ở mức khái niệm.
- Phân biệt CloudFormation vs Elastic Beanstalk vs SAM theo đúng tiêu chí đề thi SAA-C03 hay kiểm tra.

## Lý thuyết chính

### 1. Infrastructure as Code và CloudFormation

Tạo hạ tầng bằng tay trên Console (click-ops) có ba vấn đề lớn: chậm, dễ sai lệch giữa các môi trường, và không ai biết hạ tầng đã bị sửa những gì. **Infrastructure as Code** giải quyết bằng cách mô tả toàn bộ hạ tầng trong một file code: có version control, review được, tái tạo y hệt ở mọi môi trường, xóa sạch bằng một lệnh.

AWS CloudFormation là dịch vụ IaC gốc của AWS: bạn viết **Template**, CloudFormation đọc Template và tạo ra một **Stack** — tập hợp các tài nguyên AWS được quản lý như một đơn vị duy nhất.

```
Template (YAML/JSON) → CloudFormation → Stack → VPC, EC2, S3, RDS, IAM...
                                              ↕ tạo / cập nhật / xóa đồng bộ
```

**Lợi ích hay được đề thi nhấn mạnh:**
- **Tái lập (repeatable):** cùng một Template dựng được dev/test/prod giống hệt nhau.
- **Tự động và có thứ tự:** CloudFormation tự tính dependencies (ví dụ tạo VPC trước, Subnet sau, EC2 cuối cùng) và rollback khi có lỗi.
- **Xóa sạch:** Delete Stack là xóa toàn bộ tài nguyên của Stack, không sót "tài nguyên mồ côi" gây tốn tiền.
- **Không tốn phí dịch vụ:** CloudFormation miễn phí, bạn chỉ trả tiền cho tài nguyên nó tạo ra.

### 2. Cấu trúc Template

Template viết bằng **YAML hoặc JSON** (YAML phổ biến hơn vì dễ đọc), gồm các section chính:

| Section | Bắt buộc? | Nội dung |
|---------|-----------|----------|
| `AWSTemplateFormatVersion` | Không | Phiên bản định dạng template |
| `Description` | Không | Mô tả stack |
| `Parameters` | Không | Giá trị đầu vào lúc deploy (loại instance, tên môi trường...) để template tái sử dụng được |
| `Mappings` | Không | Bảng tra cứu tĩnh, ví dụ AMI ID theo Region |
| `Conditions` | Không | Điều kiện tạo tài nguyên, ví dụ chỉ tạo NAT Gateway ở prod |
| **`Resources`** | **BẮT BUỘC — duy nhất** | Các tài nguyên AWS cần tạo: `AWS::S3::Bucket`, `AWS::EC2::Instance`... |
| `Outputs` | Không | Giá trị xuất ra sau khi deploy: Bucket name, URL, ARN... |

Điểm phải thuộc lòng: **Resources là section duy nhất bắt buộc có**. Template thiếu mọi section khác vẫn hợp lệ, thiếu Resources thì không.

**Parameters nâng cao ở mức khái niệm:** AllowedValues (giới hạn lựa chọn), Default, NoEcho (che giá trị nhạy cảm như password trên console/log), SSM Parameter Store làm nguồn giá trị.

### 3. Stack và vòng đời Stack

- **Stack:** một instance đang sống của một Template. Update Template → Update Stack, CloudFormation tính toán thay đổi tối thiểu cần thiết.
- **Rollback:** tạo/cập nhật thất bại, CloudFormation tự quay về trạng thái tốt gần nhất (xóa tài nguyên vừa tạo khi Create fail). Có tùy chọn giữ lại tài nguyên lỗi để debug (Rollback on failure = disabled / `--disable-rollback`).
- **Stack Events:** dòng sự kiện chi tiết từng tài nguyên CREATE_IN_PROGRESS / COMPLETE / FAILED kèm lý do — nơi đầu tiên phải xem khi deploy lỗi.

#### Change Sets — Xem trước khi thay đổi

**Change Set** là bản **xem trước (preview)** những gì sẽ xảy ra nếu apply bản Template mới: tài nguyên nào được **Add / Modify / Remove**, và quan trọng nhất là tài nguyên nào sẽ bị **Replacement** (xóa đi tạo lại — ví dụ đổi một số thuộc tính của EC2/RDS sẽ buộc tạo tài nguyên mới, có nguy cơ mất dữ liệu/ngắt dịch vụ).

> Luồng làm việc chuẩn và an toàn: tạo Change Set → đọc kỹ, đặc biệt cột Replacement → mới Execute. Đề thi hỏi "làm sao biết trước update sẽ thay thế tài nguyên nào" → đáp án luôn là Change Sets.

#### Stack Policies — Chặn sửa/xóa tài nguyên quan trọng

**Stack Policy** là tài liệu JSON gắn vào Stack, quy định loại Update Action nào được phép trên tài nguyên nào. Tác dụng chính: **bảo vệ tài nguyên trọng yếu** (ví dụ RDS database production) khỏi bị vô tình update/xóa/replace khi ai đó update Stack.

Lưu ý: Stack Policy chỉ áp dụng cho hành động **Update** của Stack, không chặn việc xóa cả Stack hay sửa tài nguyên trực tiếp ngoài CloudFormation.

#### Drift Detection — Phát hiện sửa tay

**Drift** là tình trạng tài nguyên thật đã **lệch khỏi Template** vì ai đó sửa tay trên Console (đổi Security Group, tăng size, sửa tag...).

**Drift Detection** so sánh trạng thái thực tế với Template và báo cáo Stack/tài nguyên là `IN_SYNC` hay `DRIFTED` kèm chi tiết thuộc tính nào lệch. Nó **chỉ phát hiện, không tự sửa** — bạn phải tự quyết định sửa tay lại hay cập nhật Template cho khớp.

> **Tình huống thực tế:** Sau 6 tháng, team vận hành sửa tay nhiều chỗ để chữa cháy. Trước kỳ audit, chạy Drift Detection cho mọi Stack production để biết hạ tầng thật còn khớp với code không — scenario rất hay gặp trong đề ở dạng "how to identify manual changes made outside CloudFormation".

### 4. Intrinsic Functions — Hàm nội tại cốt lõi

Intrinsic Functions chỉ dùng được **bên trong Template**, là phần đề thi kiểm tra nhiều nhất của bài này:

| Hàm | Tác dụng | Ví dụ tình huống |
|-----|----------|------------------|
| **Ref** | Lấy giá trị của Parameter hoặc giá trị chính của Resource (ID/Name tùy loại) | `!Ref MyBucket` → tên S3 Bucket; `!Ref Environment` → giá trị parameter |
| **Fn::GetAtt** | Lấy **thuộc tính mở rộng** của Resource mà Ref không trả về | Lấy ARN của S3 Bucket, DNS name của Load Balancer: `!GetAtt MyLB.DNSName` |
| **Fn::Sub** | **Thay biến vào chuỗi** (string substitution), gộp giá trị thành một chuỗi | Tạo tên bucket `"${AWS::StackName}-data-${Environment}"`, dựng ARN, viết User Data script có biến |
| **Fn::ImportValue** | **Nhập giá trị được Export** từ Stack khác (Cross-Stack Reference) | Stack App nhập VPC ID do Stack Network đã export |
| Fn::Join / Fn::Split | Nối / tách chuỗi (biết ở mức khái niệm) | Ghép danh sách subnet, tách chuỗi ARN |
| Fn::Select / Fn::GetAZs | Chọn phần tử / lấy danh sách AZ của Region (mức khái niệm) | Chọn AZ thứ 2 để đặt subnet |
| Fn::If | Chọn giá trị theo Condition (mức khái niệm) | Prod dùng instance lớn, dev dùng instance nhỏ |

**Phân biệt Ref vs Fn::GetAtt** — bẫy kinh điển nhất:
- Muốn ID/tên chính của tài nguyên → `Ref`.
- Muốn thuộc tính khác (ARN, DNS, endpoint...) → `Fn::GetAtt`.

### 5. Outputs và Cross-Stack References

- **Outputs:** phần Template khai báo giá trị xuất ra sau khi Stack tạo xong (hiển thị trên Console, truy vấn bằng CLI/API). Output có thể đặt cờ **Export** với một tên duy nhất trong Region + Account.
- **Cross-Stack Reference:** Stack B dùng `Fn::ImportValue` để nhập giá trị Stack A đã Export — ví dụ Stack Network export VPC ID và Subnet IDs, nhiều Stack App cùng import dùng chung.
- Hệ quả phải nhớ: tài nguyên đã được Stack khác import thì **Stack gốc không xóa/update được Export đó** cho tới khi Stack phụ thuộc bỏ tham chiếu. Đây là cơ chế an toàn nhưng cũng là nguyên nhân deploy bị chặn hay gặp.

> **Tình huống thực tế:** Team nền tảng quản lý một Stack `network-prod` chứa VPC dùng chung cho 15 ứng dụng. Mỗi ứng dụng là một Stack riêng import VPC ID qua Cross-Stack Reference. Nâng cấp mạng làm một chỗ, không team app nào phải copy-paste VPC ID, và không ai lỡ tay xóa được VPC đang có 15 app phụ thuộc.

### 6. Helper Scripts cho EC2: cfn-init và cfn-signal

EC2 nằm trong Stack cần cơ chế báo cho CloudFormation biết việc cài đặt bên trong máy đã xong hay chưa:

- **cfn-init:** script chạy trong EC2 (thường qua User Data), đọc phần metadata `AWS::CloudFormation::Init` trong Template để cài package, tạo file cấu hình, khởi động service một cách có cấu trúc — thay vì viết User Data shell script dài dòng khó bảo trì.
- **cfn-signal:** script báo tín hiệu thành công/thất bại về cho CloudFormation. Kết hợp với **CreationPolicy / ResourceSignal**: Stack **chờ tín hiệu** trong một khoảng timeout trước khi đánh dấu EC2 là CREATE_COMPLETE. Không nhận được tín hiệu success → Stack rollback.
- Cặp này hay xuất hiện trong scenario: "EC2 phải cài xong ứng dụng và báo về thì Stack mới coi là thành công, nếu cài lỗi thì rollback toàn bộ".

### 7. Nested Stacks — Ở mức khái niệm

**Nested Stack** là Stack con được tạo từ một Stack cha thông qua resource `AWS::CloudFormation::Stack`. Dùng khi một mẫu hạ tầng lặp lại nhiều lần (ví dụ module VPC, module ALB chuẩn) hoặc Template quá lớn cần tách nhỏ để tái sử dụng và quản trị theo team. Update Stack cha sẽ lan xuống các Stack con. Khác với Cross-Stack Reference: Nested là quan hệ **cha–con trong một cây triển khai**, Cross-Stack là các Stack **ngang hàng tham chiếu giá trị** của nhau.

### 8. Phân biệt CloudFormation vs Elastic Beanstalk vs SAM

| Tiêu chí | CloudFormation | Elastic Beanstalk | AWS SAM |
|----------|---------------|-------------------|---------|
| Bản chất | IaC khai báo **mọi tài nguyên AWS** | **PaaS** deploy ứng dụng nhanh | **Mở rộng (extension) của CloudFormation** cho serverless |
| Bạn quản lý | Toàn quyền và toàn trách nhiệm về hạ tầng | Chỉ đưa code, Beanstalk tự lo EC2/ELB/ASG | Khai báo Lambda, API Gateway, DynamoDB bằng cú pháp tắt ngắn gọn |
| Cú pháp | Template đầy đủ, dài | Không viết template hạ tầng (có thể tùy biến bằng .ebextensions) | Template SAM transform: `AWS::Serverless::Function`... biên dịch thành CloudFormation |
| Dùng khi nào | Cần kiểm soát chi tiết, hạ tầng phức tạp, chuẩn doanh nghiệp | Developer muốn **deploy app nhanh nhất**, ít quan tâm hạ tầng | Dự án **serverless** là chính, muốn template ngắn + công cụ build/deploy/test local |

- **Beanstalk không phải IaC đa năng:** nó trừu tượng hóa hạ tầng để deploy code nhanh; cần VPC/RDS/IAM tùy biến sâu thì phải quay về CloudFormation.
- **SAM không thay thế CloudFormation:** SAM Template được CloudFormation xử lý sau bước transform — mọi Stack SAM vẫn là Stack CloudFormation.

## Ví dụ đời thường

Hãy hình dung việc **xây nhà theo bản vẽ**:

- **Template** là bản vẽ kiến trúc hoàn chỉnh: móng ở đâu, mấy phòng, đường điện nước thế nào. **Resources** là phần bản vẽ các phòng — bản vẽ không có phòng thì không phải bản vẽ nhà, nên nó là phần bắt buộc duy nhất.
- **Stack** là ngôi nhà thật được xây từ bản vẽ đó. Một bản vẽ xây được nhiều ngôi nhà giống hệt ở các khu đất khác nhau (dev, test, prod).
- **Parameters** là những lựa chọn của chủ nhà lúc xây: sơn màu gì (biến đầu vào), nhà vẫn theo cùng một bản vẽ.
- **Change Set** là lúc nhà thầu đưa tờ giấy: "sửa theo yêu cầu mới thì phòng này giữ nguyên, phòng kia phải đập xây lại (replacement)" — bạn xem và gật đầu **trước khi** người ta cầm búa.
- **Stack Policy** là quy định dán ở phòng máy chủ: "phòng này không ai được tự ý sửa trong lúc nâng cấp nhà".
- **Drift Detection** là đoàn kiểm tra cầm bản vẽ đi đối chiếu nhà thật: "sao ở đây có thêm một bức tường không có trong bản vẽ?" — họ chỉ ghi biên bản, không tự đập tường (chỉ phát hiện, không tự sửa).
- **Fn::Sub** giống điền tên vào mẫu thư: "Kính gửi ${Tên}, mã đơn của bạn là ${Mã}" — một khuôn, nhiều giá trị thật.
- **Cross-Stack Reference** là khu đô thị: bản vẽ hệ thống đường và cấp nước (Stack Network) công bố sẵn số hiệu tuyến ống, bản vẽ từng ngôi nhà chỉ việc ghi "nối vào tuyến ống số X" (ImportValue) thay vì tự đào hệ thống nước riêng.

## Phân biệt dễ nhầm

**1. Ref vs Fn::GetAtt**
- `Ref` lấy giá trị định danh chính (ID/tên) của resource hoặc giá trị của parameter.
- `Fn::GetAtt` lấy thuộc tính phụ: ARN, DNS name, endpoint. Cần ARN mà dùng Ref là sai — bẫy số 1 của bài này.

**2. Change Sets vs Stack Policies vs Drift Detection**
- Change Sets: xem trước **hậu quả của lần update sắp tới** (trước khi thay đổi).
- Stack Policies: **chặn** các update nguy hiểm lên tài nguyên quan trọng (trong lúc update).
- Drift Detection: phát hiện **lệch lạc đã xảy ra** do sửa tay ngoài CloudFormation (sau khi thay đổi).
- Ba công cụ ứng với ba thời điểm: trước — trong — sau.

**3. Cross-Stack Reference vs Nested Stacks**
- Cross-Stack: các Stack độc lập, ngang hàng; Stack này **import output đã export** của Stack kia bằng Fn::ImportValue.
- Nested: Stack **con nằm trong Stack cha**, cha quản lý vòng đời của con như một resource.

**4. CloudFormation vs Elastic Beanstalk**
- Cần mô tả và kiểm soát **hạ tầng** chi tiết → CloudFormation.
- Chỉ muốn **đẩy code lên chạy nhanh**, chấp nhận nền tảng tự quyết hạ tầng → Elastic Beanstalk.

**5. SAM vs CloudFormation**
- SAM là lớp cú pháp tắt **trên** CloudFormation dành riêng cho serverless, không phải dịch vụ đối thủ. Template SAM cuối cùng vẫn deploy bằng CloudFormation.

**6. Outputs vs Export**
- Mọi Export đều là Output, nhưng không phải Output nào cũng Export. Chỉ Output có khai báo Export mới được Stack khác ImportValue; Output thường chỉ để hiển thị và truy vấn.

## Bẫy đề thi

1. **Hỏi section bắt buộc duy nhất.** Đáp án là **Resources**. Template có thể không có Parameters, Outputs, Mappings... nhưng không thể không có Resources.

2. **Update làm mất dữ liệu mà không ai báo trước.** Nếu team dùng Change Sets và đọc kỹ cột **Replacement = True** cho RDS/EC2 thì đã thấy trước nguy cơ. Scenario "làm sao preview thay đổi, đặc biệt tài nguyên nào bị thay thế" → Change Sets.

3. **Nhầm Drift Detection là công cụ tự vá.** Nó chỉ **báo cáo** drift. Muốn hết drift phải chủ động: sửa tay ngược lại, hoặc update Stack/Template. Đáp án "enable drift detection to automatically fix changes" là sai.

4. **Stack Policy bị tưởng là chặn được mọi thứ.** Stack Policy chỉ giới hạn **Stack Update Actions**. Nó không ngăn xóa toàn bộ Stack, không ngăn user có quyền sửa thẳng tài nguyên trên Console.

5. **Xóa Stack Network thất bại không rõ lý do.** Thường vì Output của nó đang bị Stack khác ImportValue. Phải gỡ tham chiếu ở các Stack phụ thuộc trước — đây là hệ quả thiết kế của Cross-Stack References, không phải lỗi dịch vụ.

6. **Dùng Ref để lấy ARN.** Ref của S3 Bucket trả về tên bucket, không phải ARN. Lấy ARN/DNS/endpoint → Fn::GetAtt. Đề thi lặp lại bẫy này rất nhiều lần với nhiều loại resource.

7. **EC2 báo CREATE_COMPLETE dù ứng dụng cài thất bại.** Vì thiếu CreationPolicy + cfn-signal: CloudFormation chỉ biết EC2 đã boot xong chứ không biết app bên trong thành công. Muốn Stack chờ và rollback khi cài app lỗi → cfn-init cài đặt + cfn-signal báo về + CreationPolicy chờ tín hiệu.

8. **Chọn Beanstalk cho yêu cầu IaC kiểm soát toàn diện.** Beanstalk tiện cho deploy app nhưng không phải công cụ khai báo mọi tài nguyên AWS. Yêu cầu "define all infrastructure as code, full control, reproducible" → CloudFormation (hoặc SAM nếu thuần serverless).

9. **Fn::ImportValue dùng giá trị chưa Export.** ImportValue chỉ hoạt động với Output **đã Export** và tên export phải **duy nhất trong Account + Region**. Thiếu Export ở Stack nguồn là nguyên nhân template validate/deploy lỗi kinh điển.

## Tóm tắt 5 dòng

1. CloudFormation là dịch vụ IaC của AWS: Template YAML/JSON mô tả hạ tầng, Stack là tập tài nguyên được tạo và quản lý như một đơn vị, tạo/cập nhật/xóa đồng bộ và rollback khi lỗi.
2. Trong Template, Resources là section bắt buộc duy nhất; Parameters/Mappings/Conditions/Outputs là tùy chọn giúp template tái sử dụng và linh hoạt.
3. Change Sets cho xem trước thay đổi và cảnh báo Replacement, Stack Policies chặn update vào tài nguyên quan trọng, Drift Detection phát hiện (không tự sửa) các thay đổi làm tay ngoài Template.
4. Intrinsic Functions cốt lõi: Ref lấy giá trị chính, Fn::GetAtt lấy thuộc tính như ARN/DNS, Fn::Sub thay biến vào chuỗi, Fn::ImportValue nhập giá trị Export từ Stack khác cho Cross-Stack References.
5. cfn-init/cfn-signal giúp EC2 cài đặt và báo tín hiệu về Stack kèm CreationPolicy; Nested Stacks tổ chức template lớn dạng cha–con; CloudFormation khác Beanstalk (PaaS deploy app nhanh) và là nền tảng mà SAM mở rộng cho serverless.

## Quiz — 5 câu hỏi tiếng Anh kiểu đề thi

**Question 1.** A solutions architect is writing an AWS CloudFormation template in YAML. Which section of the template is the ONLY section that must be included for the template to be valid?

A. Parameters
B. Outputs
C. Resources
D. Mappings

**Question 2.** Before updating a production CloudFormation stack, a team wants to preview exactly which resources will be added, modified, or replaced, because replacing the database would cause downtime. Which CloudFormation feature should the team use?

A. Drift Detection
B. Stack Policy
C. Change Sets
D. cfn-signal

**Question 3.** A network stack exports its VPC ID. An application stack needs to use that VPC ID when launching resources, and the value must always stay in sync with the network stack. Which intrinsic function should the application stack's template use?

A. Ref
B. Fn::GetAtt
C. Fn::Sub
D. Fn::ImportValue

**Question 4.** An operations team discovers that engineers have been making manual changes to production resources through the AWS Management Console, and the actual infrastructure no longer matches the CloudFormation templates. Which feature will identify the resources that have been modified outside of CloudFormation?

A. Change Sets
B. Drift Detection
C. Stack Policies
D. Nested Stacks

**Question 5.** A development team wants to deploy a Java web application as quickly as possible. The developers do not want to design or manage the underlying infrastructure in detail, but they still want AWS to handle provisioning, load balancing, and auto scaling for the application environment. Which service is the best fit?

A. AWS CloudFormation
B. AWS SAM
C. Amazon Elastic Beanstalk
D. AWS Step Functions

## Đáp án quiz

**Question 1 — Đáp án: C**
Giải thích: Resources là section duy nhất bắt buộc trong CloudFormation Template — nó khai báo các tài nguyên AWS cần tạo. Parameters, Outputs, Mappings, Conditions đều là tùy chọn; template thiếu chúng vẫn hợp lệ, thiếu Resources thì không.

**Question 2 — Đáp án: C**
Giải thích: Change Sets tạo bản xem trước của lần update: tài nguyên nào Add/Modify/Remove và đặc biệt tài nguyên nào bị Replacement (xóa tạo lại). Team phải review Change Set rồi mới Execute. Drift Detection dùng để phát hiện sửa tay sau này, Stack Policy để chặn update — cả hai đều không cho preview thay đổi.

**Question 3 — Đáp án: D**
Giải thích: Đây là mẫu Cross-Stack Reference: Stack Network Export VPC ID trong Outputs, Stack App dùng Fn::ImportValue để nhập vào. Ref chỉ tham chiếu resource/parameter trong cùng một template, Fn::GetAtt lấy thuộc tính của resource cùng stack, Fn::Sub chỉ thay biến vào chuỗi.

**Question 4 — Đáp án: B**
Giải thích: Drift Detection so sánh trạng thái thực tế của tài nguyên với Template và báo cáo tài nguyên nào đã DRIFTED do thay đổi ngoài CloudFormation. Lưu ý nó chỉ phát hiện và báo cáo, không tự sửa. Stack Policy chặn update, Change Sets xem trước update — không công cụ nào trong số đó rà soát được sửa tay đã xảy ra.

**Question 5 — Đáp án: C**
Giải thích: Elastic Beanstalk là dịch vụ PaaS: developer chỉ đưa code, Beanstalk tự lo provisioning, Load Balancer và Auto Scaling — đúng yêu cầu "deploy nhanh, không muốn quản lý hạ tầng chi tiết". CloudFormation cho toàn quyền kiểm soát IaC nhưng đòi hỏi tự khai báo mọi thứ, SAM là mở rộng của CloudFormation cho serverless, Step Functions là điều phối workflow chứ không phải nền tảng deploy ứng dụng.
