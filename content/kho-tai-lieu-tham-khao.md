# Kho tài liệu tham khảo — Học AWS SAA-C03

> Danh mục link đã được kiểm chứng ngày 08/11/2026. Chỉ gồm link + ghi chú ngắn "dùng khi nào". Không sao chép nội dung của bên thứ ba — hãy học trực tiếp tại nguồn.
> ⚠️ Tránh xa các trang "exam dump" (rò rỉ đề thật): AWS cấm, đáp án thường sai, và học thuộc đáp án sẽ không qua được kỳ thi thật vốn toàn câu hỏi tình huống. Chỉ dùng các nguồn chính thống dưới đây.

---

## 1. Tài liệu chính thức của AWS (quan trọng nhất)

| Tài liệu | Link | Dùng khi nào |
|---|---|---|
| SAA-C03 Exam Guide (PDF, bản 1.1) | https://d1.awsstatic.com/training-and-certification/docs-sa-assoc/AWS-Certified-Solutions-Architect-Associate_Exam-Guide.pdf | Đọc đầu tiên và đọc lại cuối khóa — đây là văn bản định nghĩa phạm vi đề thi |
| Câu hỏi mẫu chính thức (10 câu, có đáp án + giải thích) | https://d1.awsstatic.com/training-and-certification/docs-sa-assoc/AWS-Certified-Solutions-Architect-Associate_Sample-Questions_v4.1_FINAL.pdf | Làm quen format đề thật ngay tuần 1 |
| Trang chứng chỉ SAA-C03 | https://aws.amazon.com/certification/certified-solutions-architect-associate/ | Kiểm tra thông tin đề thi mới nhất trước khi đặt lịch thi |
| AWS Well-Architected Framework | https://aws.amazon.com/architecture/well-architected/?ref=gs | Khung tư duy nền cho mọi câu hỏi tình huống (6 trụ cột) |
| Well-Architected — tài liệu đầy đủ (HTML/PDF) | https://docs.aws.amazon.com/wellarchitected/ | Đọc sâu từng trụ cột: Security, Reliability, Performance, Cost |
| Whitepaper: Disaster Recovery of Workloads on AWS | Từ trang Well-Architected phía trên | Ôn chiến lược DR (Bài 18) — phần hay ra đề |
| Danh mục Whitepapers & Guides | http://aws.amazon.com/whitepapers/ | Tra cứu thêm khi cần (vd: DDoS Resiliency) |

## 2. Học chính thức trên AWS Skill Builder (miễn phí phần lớn)

| Tài nguyên | Link | Dùng khi nào |
|---|---|---|
| Nền tảng Skill Builder | https://skillbuilder.aws/ | Đăng ký tài khoản Builder ID miễn phí, không cần thẻ |
| Exam Prep Plan SAA-C03 (18h25m, 100+ câu hỏi, 40 flashcards) | https://skillbuilder.aws/search?searchText=exam-readiness-aws-certified-solutions-architect-associate-digital&showRedirectNotFoundBanner=true | Lộ trình ôn thi chính thức theo từng domain |
| Official Practice Question Set (20 câu, MIỄN PHÍ) | https://skillbuilder.aws/search?searchText=exam-prep-official-practice-question-set-aws-certified-solutions-architect-associate-saa-c03-english&showRedirectNotFoundBanner=true | Làm "lạnh" tuần 1 để chẩn đoán trình độ, làm lại gần cuối khóa |
| Official Practice Exam (65 câu/130 phút, tính điểm như thật) | https://skillbuilder.aws/ (cần gói thuê bao $29/tháng) | Kiểm tra sẵn sàng cuối cùng trước khi đặt lịch thi thật |
| AWS Power Hour: Architecting Associate (Season 7) | https://aws.amazon.com/training/twitch/aws-power-hour-architecting-associate-season-7/ | Xem bổ trợ hằng tuần — chuyên gia AWS giảng + giải câu hỏi kiểu đề thi |

## 3. Giai đoạn Beginner — từ số 0 (trước khi vào SAA)

| Tài nguyên | Link | Dùng khi nào |
|---|---|---|
| AWS Cloud Practitioner Essentials (12h45m, miễn phí) — khóa chính thức "Beginners start here" | https://aws.amazon.com/training/learn-about/cloud-practitioner/ | Khóa nền tảng đầu tiên, đi kèm giai đoạn Beginner |
| AWS Technical Essentials (4h, có bản phụ đề tiếng Việt) | https://www.classcentral.com/course/aws-technical-essentials-tieng-viet-417592 | Khóa thực hành chính thức thứ hai, nhẹ nhàng cho người Việt |
| freeCodeCamp — AWS Cloud Practitioner CLF-C02 (Andrew Brown, ~14h, miễn phí) | https://www.freecodecamp.org/news/aws-certified-cloud-practitioner-study-course-pass-the-exam-with-this-free-13-hour-course/ | Học video trọn khóa Beginner, có phần làm theo từng bước |
| First Cloud Journey — AWS Study Group Vietnam (tiếng Việt, thực hành từng bước) | https://cloudjourney.awsstudygroup.com/vi/ | Mọi bài lab thực hành bằng tiếng Việt: tài khoản, Budgets, VPC, EC2, serverless |
| Mì AI — loạt "Mì AWS" (video tiếng Việt ngắn) | https://www.youtube.com/watch?v=ogkbs9OZL5o (Clip 1) | Nghe khái niệm bằng tiếng Việt trước khi học tài liệu tiếng Anh |
| Trang Free Tier chính thức (quy định credit MỚI) | https://aws.amazon.com/free/ | Đọc kỹ trước khi tạo tài khoản: $100 + tối đa $100 credit/6 tháng, gói Free plan |
| Hướng dẫn AWS Budgets chống phát sinh chi phí | https://docs.aws.amazon.com/hands-on/latest/control-your-costs-free-tier-budgets/control-your-costs-free-tier-budgets.html | Làm NGAY ngày đầu mở tài khoản |
| AWS Educate (lab miễn phí, không cần thẻ) | https://aws.amazon.com/education/awseducate/ | Thực hành S3/EC2 trong môi trường có sẵn nếu chưa mở được tài khoản thật |
| AWS Workshops (Level 100 = Beginner) | https://workshops.aws/?tag=Beginner | Lab thực hành theo chủ đề khi cần luyện thêm |

## 4. Khóa học video SAA-C03

| Khóa học | Link | Dùng khi nào |
|---|---|---|
| freeCodeCamp — SAA-C03 Full Course (Andrew Brown, 50h29m, MIỄN PHÍ) | https://www.youtube.com/watch?v=c3Cn4xYfxJY | Khóa video chính của giai đoạn SAA — học theo từng đoạn theo tuần, đừng xem liền 50 giờ |
| Stephane Maarek — Ultimate SAA-C03 (Udemy, trả phí, ~27.5h) | https://www.udemy.com/course/aws-certified-solutions-architect-associate-saa-c03/ | Nếu mua 1 khóa trả phí thì đây là lựa chọn phổ biến nhất — CHỈ mua khi sale ($12–25), đừng trả giá gốc |
| Adrian Cantrill — SAA-C03 (trả phí ~$40) | https://learn.cantrill.io/p/aws-certified-solutions-architect-associate-saa-c03 | Học sâu kiến trúc + thực hành; file demo/lab miễn phí tại https://github.com/acantril/aws-sa-associate-saac03 |
| VietDevOps — loạt video AWS theo lộ trình SAA-C03 (tiếng Việt) | https://www.youtube.com/watch?v=UGCBCeop9Zw | Lượt ôn thứ hai bằng tiếng Việt |

## 5. GitHub — ghi chú & tài liệu cộng đồng

| Repo | Link | Dùng khi nào |
|---|---|---|
| ⭐ vntechies/aws-saa-c03 (TIẾNG VIỆT) | https://github.com/vntechies/aws-saa-c03 | Tài liệu bạn đồng hành chính: notes theo dịch vụ, 50+ tình huống có lời giải, bảng keyword→dịch vụ, cây quyết định, lộ trình 6 tuần |
| keenanromain/AWS-SAA-C02-Study-Guide (2.1k sao) | https://github.com/keenanromain/AWS-SAA-C02-Study-Guide | Đọc song song khóa Maarek + FAQ từng dịch vụ (tên C02 nhưng nội dung cốt lõi dùng tốt cho C03, đối chiếu Exam Guide) |
| ChathurangaVKD/AWS-Certified-Solutions-Architect-Associate-SAA-C03 | https://github.com/ChathurangaVKD/AWS-Certified-Solutions-Architect-Associate-SAA-C03 | Notes + sơ đồ kiến trúc + lab, cập nhật đều (10/2026) |
| RonitSachdev/aws-saa-c03-guides | https://github.com/RonitSachdev/aws-saa-c03-guides | 38 guides giải thích bằng ẩn dụ + mẫu câu hỏi |
| AWSCertificationsWiki | https://github.com/awscertifications/awscertificationswiki/blob/HEAD/docs/associate/solutions-architect.md | Danh mục tài nguyên được cộng đồng tuyển chọn |
| VNTechies (blog tiếng Việt) | https://vntechies.dev/ | Đọc thêm bài chuyên sâu + kinh nghiệm thi của người Việt |

## 6. Luyện đề (practice exams) uy tín

| Nguồn | Link | Dùng khi nào |
|---|---|---|
| Tutorials Dojo — SAA-C03 Practice Exams ($14.99, hay sale ~$11) | https://portal.tutorialsdojo.com/courses/aws-certified-solutions-architect-associate-practice-exams/ | Ngân hàng đề luyện chính giai đoạn nước rút: chế độ timed/review/theo domain; có bản dùng thử 30 câu miễn phí |
| Tutorials Dojo — Study Path & Cheat Sheets (miễn phí) | https://tutorialsdojo.com/tag/aws-study-path/ | Cheat sheet từng dịch vụ để ôn tuần cuối |
| Neal Davis — Practice Exams (Udemy, 6 đề/390 câu) | https://www.udemy.com/course/aws-certified-solutions-architect-associate-practice-tests-k/ | Đề luyện bổ sung nếu cần thêm số lượng |
| Whizlabs — SAA-C03 (có 1 đề miễn phí) | https://www.whizlabs.com/aws-solutions-architect-associate/ | Làm đề miễn phí trước, cân nhắc mua sau |

## 7. Tài liệu tra cứu nhanh theo dịch vụ (chính thức)

| Nhu cầu | Link |
|---|---|
| Tạo IAM user (hướng dẫn chính thức) | https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html |
| Launch EC2 instance đầu tiên (10 phút) | https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/tutorial-launch-my-first-ec2-instance.html |
| Lưu & lấy file với S3 (hands-on) | https://docs.aws.amazon.com/hands-on/latest/backup-files-to-amazon-s3/backup-files-to-amazon-s3.html |
| Tạo VPC | https://docs.aws.amazon.com/vpc/latest/userguide/create-vpc.html |
| Tạo RDS DB instance | https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_Tutorials.WebServerDB.CreateDBInstance.html |
| Tạo bảng DynamoDB | https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/getting-started-step-1.html |
| Lambda "Hello World" serverless | https://aws.amazon.com/tutorials/run-serverless-code/ |
| Bắt đầu với CloudFront | https://aws.amazon.com/cloudfront/getting-started/ |
| Cổng Getting Started (toàn bộ tutorial chính thức) | https://aws.amazon.com/getting-started/ |
| Ramp-Up Guide: Cloud Essentials (PDF) | https://aws.amazon.com/training/ramp-up-guides/ (chọn Cloud Essentials) |

---

*Cập nhật: 08/11/2026. Giá cả và nội dung khóa học có thể thay đổi — kiểm tra tại nguồn trước khi mua.*
