# Bài 17 — ECS, EKS và Container

## Mục tiêu bài học

- Phân biệt được Container, VM (EC2) và Lambda ở mức ra quyết định chọn dịch vụ trong đề thi.
- Nắm vững Docker, ECR, ECS với 2 launch types, và các khái niệm Task Definition / Task / Service.
- Biết khi nào chọn EKS, khi nào chọn App Runner, và nhận diện đáp án Fargate khi đề nhắc "least operational overhead" / "minimal management".

## Lý thuyết chính

### 1. Ra quyết định: VM vs Container vs Lambda

Đây là câu hỏi nền tảng, đề thi không hỏi định nghĩa mà hỏi **scenario → chọn cái nào**.

| Tiêu chí | VM — EC2 | Container — ECS/EKS | Serverless Function — Lambda |
|---|---|---|---|
| Đơn vị triển khai | Cả máy ảo + OS | Image đóng gói app + dependencies | Chỉ code hàm |
| Ai quản lý OS / patching | Bạn | Bạn (EC2 launch type) hoặc AWS (Fargate) | AWS hoàn toàn |
| Thời gian chạy | Dài hạn, liên tục | Dài hạn, liên tục | Ngắn, theo event, tối đa 15 phút / lần chạy |
| Scaling | ASG theo instance | Theo Task | Tự động theo request |
| Phù hợp khi | Cần kiểm soát OS, phần mềm legacy, license theo máy | Đã có Docker workload, microservices, batch dài | Event-driven, API nhẹ, xử lý file, lịch cron ngắn |

**Quy tắc nhớ nhanh:**
- Đề nói "lift-and-shift, cần kiểm soát OS" → EC2.
- Đề nói "đã có Docker image / microservices" → ECS hoặc EKS.
- Đề nói "chạy code khi có sự kiện, không muốn quản lý server, chạy dưới 15 phút" → Lambda.

### 2. Docker — khái niệm cốt lõi

- **Docker Image:** bản đóng gói bất biến gồm code, runtime, libraries, dependencies. Build 1 lần, chạy giống nhau ở mọi nơi — giải quyết bài toán "chạy được trên máy tôi nhưng không chạy trên server".
- **Container:** một instance đang chạy của image. Nhẹ hơn VM vì **chia sẻ kernel của host OS**, không chứa cả Guest OS riêng như VM.
- **Dockerfile:** file mô tả cách build image.

Khác biệt cốt lõi với VM: VM ảo hóa phần cứng (hypervisor), container ảo hóa ở tầng OS → khởi động trong vài giây, mật độ đóng gói cao hơn.

### 3. Amazon ECR — Elastic Container Registry

- Là **kho chứa Docker image riêng (private registry)** của AWS, tương tự vai trò của S3 đối với file.
- Tích hợp IAM để kiểm soát ai được push/pull image, hỗ trợ scan lỗ hổng bảo mật trên image.
- Luồng chuẩn trong đề: `Build Docker image → Push lên ECR → ECS/EKS pull từ ECR để chạy`.
- Đừng nhầm ECR với ECS: ECR **lưu** image, ECS **chạy** image.

### 4. Amazon ECS — Elastic Container Service

Là **dịch vụ điều phối container (container orchestration) của AWS**, tích hợp sâu với IAM, ALB, CloudWatch, VPC. Đây là đáp án mặc định khi đề nói "chạy container trên AWS" mà không nhắc Kubernetes.

**Ba khái niệm bắt buộc thuộc:**

- **Task Definition:** bản thiết kế (blueprint) của Task — khai báo image nào (từ ECR), CPU/memory bao nhiêu, port, environment variables, IAM Role cho Task, log configuration. Giống như Launch Template của EC2.
- **Task:** một instance đang chạy theo Task Definition — tương đương "một nhóm container chạy cùng nhau". ECS dừng/một Task chết thì có thể thay Task mới.
- **Service:** lớp đảm bảo duy trì số lượng Task mong muốn (desired count), gắn với ALB để phân tải, tự thay thế Task bị lỗi, hỗ trợ auto scaling. Muốn ứng dụng chạy ổn định lâu dài → dùng Service, không chạy Task trần.

**Hai launch types — điểm thi quan trọng nhất bài này:**

| | EC2 Launch Type | Fargate Launch Type |
|---|---|---|
| Hạ tầng chạy container | EC2 instances do **bạn** quản lý trong Cluster | **Serverless** — AWS lo hạ tầng |
| Việc bạn phải làm | Chọn instance type, patch OS, scale cluster, tối ưu packing | Chỉ khai báo CPU/memory trong Task Definition |
| Thanh toán | Trả tiền EC2 instance (kể cả khi ít Task) | Trả tiền theo vCPU + memory mà Task thực dùng |
| Phù hợp khi | Cần kiểm soát sâu, cần GPU / instance đặc biệt, muốn dùng Spot / Savings Plans trên instance | Muốn **least operational overhead**, không muốn quản lý server |

> Cụm từ khóa vàng: đề nói **"migrate Docker workloads, minimal management / least operational overhead / no servers to manage" → đáp án là ECS on Fargate**. Đây là pattern lặp lại rất nhiều trong SAA-C03.

### 5. Amazon EKS — Elastic Kubernetes Service

- Là **Kubernetes được quản lý (managed Kubernetes)** trên AWS: AWS quản lý control plane, bạn quản lý hoặc dùng Fargate cho worker nodes / data plane.
- Chọn EKS khi: công ty **đã dùng Kubernetes** ở on-premises hoặc đa cloud, cần tính portable, cần hệ sinh thái Kubernetes (Helm, service mesh), hoặc team đã có kỹ năng Kubernetes.
- Không chọn EKS chỉ vì "nghe mạnh hơn ECS". Nếu đề không nhắc chữ Kubernetes, đáp án thường là ECS — đơn giản hơn, ít overhead hơn.

### 6. AWS App Runner — mức khái niệm

- Dịch vụ đơn giản nhất để deploy ứng dụng web/API: đưa **source code (GitHub) hoặc container image** vào, App Runner tự build, deploy, scale, cân bằng tải, cấp HTTPS.
- Phù hợp: team nhỏ, web app/API đơn giản, muốn nhanh nhất, không muốn đụng vào VPC/Cluster/ALB.
- Đánh đổi: ít khả năng tùy biến hạ tầng hơn ECS/EKS.
- Thứ tự độ đơn giản tăng dần về kiểm soát (và độ phức tạp): **App Runner (đơn giản nhất) → ECS on Fargate → ECS on EC2 / EKS (kiểm soát cao nhất)**.

## Ví dụ đời thường

Hãy hình dung 3 cách mở quán ăn:

- **EC2 như thuê mặt bằng trống:** bạn tự lắp bếp, bàn ghế, điện nước. Kiểm soát tối đa, cực nhất.
- **Container như xe bán đồ ăn (food truck) đóng gói sẵn:** bếp đã lắp sẵn trong xe, lái tới đâu bán tới đó, dọn rất nhanh. Docker image chính là chiếc xe đã đóng gói hoàn chỉnh.
- **Fargate như thuê ki-ốt trong trung tâm thương mại:** bạn chỉ mang món ăn (image) tới, trung tâm lo mặt bằng, điện nước, bảo trì. Bạn trả tiền theo ki-ốt bạn dùng.
- **Lambda như bán hàng theo đơn gọi món:** không có quán, khách gọi món nào bạn mới nấu món đó, xong thì dọn — trả tiền theo món.

ECR là **kho đậu xe food truck**, ECS là **đội điều phối xe**, EKS là điều phối theo **chuẩn Kubernetes quốc tế** — đội xe của hãng nào cũng đọc được cùng một sổ tay.

## Phân biệt dễ nhầm

- **ECR vs ECS:** ECR lưu image (registry), ECS chạy container (orchestration). Đề hỏi "store Docker images securely" → ECR. Đề hỏi "run/orchestrate containers" → ECS.
- **Task vs Service:** Task là một lần chạy, chết là hết. Service duy trì desired count, tự hồi sinh Task, gắn ALB. Ứng dụng production lâu dài → Service.
- **ECS vs EKS:** Cả hai đều chạy container. Chỉ chọn EKS khi đề nhắc **Kubernetes** rõ ràng hoặc yêu cầu portable / multi-cloud. Còn lại mặc định ECS.
- **Fargate vs Lambda:** Cả hai đều "serverless", nhưng Fargate chạy **container dài hạn** (web service, API chạy liên tục), Lambda chạy **hàm ngắn theo event** (tối đa 15 phút). Có Docker image chạy 24/7 → Fargate, không phải Lambda.
- **App Runner vs Fargate:** App Runner đơn giản hơn nữa — deploy thẳng từ source/image cho web app. Fargate cho bạn kiểm soát Task Definition, VPC, Service chi tiết hơn.

## Bẫy đề thi

- **Bẫy 1:** Đề mô tả "company has Docker containers, wants to migrate to AWS with minimal operational overhead, no Kubernetes experience" — đáp án cám dỗ là EKS vì nghe "chuẩn". Đáp án đúng: **ECS on Fargate**.
- **Bẫy 2:** Đề cho EC2 launch type trong đáp án kèm cụm "serverless" — sai. EC2 launch type không serverless. Chỉ Fargate mới serverless.
- **Bẫy 3:** Đề hỏi nơi lưu trữ image private + tích hợp IAM — nhiều bạn chọn S3. Sai, phải là **ECR**.
- **Bẫy 4:** Thấy chữ "container" là chọn Kubernetes. SAA mặc định ưu tiên dịch vụ managed của AWS (ECS) trừ khi scenario ép dùng Kubernetes.
- **Bẫy 5:** Chọn Lambda cho workload container chạy liên tục 24/7 hoặc chạy quá 15 phút — Lambda không đáp ứng được, phải dùng ECS/Fargate.

## Tóm tắt 5 dòng

- Container đóng gói app + dependencies trong image, nhẹ hơn VM vì chia sẻ host kernel; ECR là kho lưu image riêng của AWS.
- ECS là dịch vụ orchestration của AWS: Task Definition là blueprint, Task là instance đang chạy, Service duy trì số Task và gắn ALB.
- ECS có 2 launch types: EC2 (tự quản instance) và Fargate (serverless, AWS lo hạ tầng — least operational overhead).
- EKS chỉ khi đề nhắc Kubernetes / cần portable; App Runner là cách deploy web app từ source/image đơn giản nhất.
- Thấy "migrate Docker workloads, minimal management" → chọn ECS on Fargate.

## Quiz

**Question 1.** A company has Docker-based microservices running on-premises. The company wants to migrate the containers to AWS with the least operational overhead. The team has no Kubernetes experience and does not want to manage or patch any servers. Which solution meets these requirements?

A. Run the containers on Amazon EKS with self-managed EC2 worker nodes.
B. Run the containers on Amazon ECS with the Fargate launch type, storing images in Amazon ECR.
C. Repackage each microservice as an AWS Lambda function.
D. Install Docker on EC2 instances and manage the containers manually.

**Question 2.** A developer builds a new Docker image for an application and needs a private, AWS-managed repository to store the image, with access controlled by IAM policies and integration with the container orchestration service that will pull the image. Which service should the developer use?

A. Amazon S3
B. AWS CodeCommit
C. Amazon Elastic Container Registry (Amazon ECR)
D. Amazon Elastic Block Store (Amazon EBS)

**Question 3.** A company already runs Kubernetes clusters on-premises and has a skilled platform team. The company wants to migrate its Kubernetes workloads to AWS while keeping the same Kubernetes tooling and manifests, and wants AWS to manage the Kubernetes control plane. Which solution meets these requirements?

A. Amazon ECS with the EC2 launch type
B. AWS App Runner
C. Amazon EKS
D. AWS Elastic Beanstalk

**Question 4.** An ECS Service must ensure that three copies of a web application task are always running, replace any task that fails a health check, and distribute incoming traffic across the tasks. Which ECS components are involved?

A. A Task Definition alone, without a Service
B. A Service maintaining the desired count of Tasks defined by a Task Definition, integrated with an Application Load Balancer
C. Individual Tasks launched manually from the console
D. An ECR repository with three stored images

**Question 5.** A small team wants to deploy a simple web API to AWS as quickly as possible. The team will provide the application source code from a GitHub repository and wants AWS to handle building, deploying, scaling, load balancing, and HTTPS with minimal configuration. Which service is the MOST suitable?

A. Amazon EKS with Fargate profiles
B. Amazon ECS with the EC2 launch type
C. Self-managed Docker Swarm on EC2 instances
D. AWS App Runner

## Đáp án quiz

**Câu 1 — Đáp án B.** ECS on Fargate là serverless, AWS quản lý hạ tầng bên dưới nên operational overhead thấp nhất cho Docker workload, và image lưu ở ECR. A sai vì EKS + tự quản worker nodes tốn công nhất và team không có kinh nghiệm Kubernetes. C sai vì microservices chạy liên tục không phù hợp mô hình Lambda theo event, giới hạn 15 phút. D sai vì tự cài Docker trên EC2 là tự quản toàn bộ.

**Câu 2 — Đáp án C.** ECR chính là private container registry của AWS, tích hợp IAM và vulnerability scanning, được ECS/EKS pull image trực tiếp. S3 lưu object/file chứ không phải registry cho Docker image theo chuẩn OCI. CodeCommit lưu source code, EBS là block storage cho EC2 — cả hai đều không liên quan tới container image.

**Câu 3 — Đáp án C.** Từ khóa quyết định là "already uses Kubernetes" + "keep same tooling/manifests" + "AWS manages control plane" → EKS. ECS dùng cơ chế orchestration riêng của AWS, không chạy Kubernetes manifests. App Runner và Elastic Beanstalk không phải Kubernetes.

**Câu 4 — Đáp án B.** Service là thành phần duy trì desired count, tự thay Task lỗi và tích hợp ALB để phân tải; Task Definition chỉ là blueprint khai báo image/CPU/memory. Chạy Task trần (A, C) không có cơ chế tự hồi sinh và cân bằng tải. ECR chỉ lưu image, không điều phối Task đang chạy.

**Câu 5 — Đáp án D.** App Runner được thiết kế đúng cho nhu cầu này: nhận source code hoặc image, tự build/deploy/scale/load balancing/HTTPS với cấu hình tối thiểu — đơn giản nhất trong các lựa chọn. EKS và ECS on EC2 đều đòi hỏi cấu hình cluster, VPC, ALB nhiều hơn mức cần thiết cho một web API đơn giản.
