# Bài 18 — Disaster Recovery

## Mục tiêu bài học

- Phân biệt dứt khoát RPO và RTO — cặp khái niệm xuất hiện gần như chắc chắn trong đề SAA-C03.
- Thuộc thứ tự 4 chiến lược Disaster Recovery (DR) theo chi phí tăng dần và thời gian phục hồi giảm dần.
- Biết các công cụ hỗ trợ DR của AWS và nguyên tắc chọn chiến lược theo yêu cầu kinh doanh, không chọn mặc định cái đắt nhất.

## Lý thuyết chính

### 1. RPO và RTO — hai con số quyết định mọi thứ

- **RPO — Recovery Point Objective:** bạn chấp nhận **mất dữ liệu tới thời điểm nào**. Hiểu đơn giản: "Nếu hệ thống sập ngay bây giờ, tôi chấp nhận mất tối đa bao nhiêu dữ liệu tính theo thời gian?" Ví dụ RPO = 1 giờ nghĩa là chấp nhận mất dữ liệu của 1 giờ gần nhất → backup/replication phải diễn ra ít nhất mỗi giờ.
  - RPO trả lời về **DỮ LIỆU (data loss)**, đơn vị là khoảng thời gian quay về quá khứ.
- **RTO — Recovery Time Objective:** **mất bao lâu để phục hồi** hệ thống hoạt động trở lại sau thảm họa. Ví dụ RTO = 30 phút nghĩa là từ lúc sập, tối đa 30 phút sau hệ thống phải chạy lại.
  - RTO trả lời về **THỜI GIAN CHẾT (downtime)**, đơn vị là khoảng thời gian hướng về tương lai.

> Mẹo nhớ: **RPO = Point = điểm dữ liệu trong quá khứ. RTO = Time = thời gian chờ phục hồi trong tương lai.**

Mọi quyết định DR trong đề thi đều bắt đầu từ hai con số này trong scenario. Đề cho RPO/RTO càng nhỏ → chiến lược càng đắt, càng phải chạy sẵn ở Region dự phòng.

### 2. Bốn chiến lược DR — thuộc theo thứ tự

Sắp xếp theo **chi phí tăng dần / thời gian phục hồi giảm dần**. Đây là trục so sánh mà đề thi luôn dùng:

| Thứ tự | Chiến lược | Trạng thái ở DR Region | RPO / RTO điển hình | Chi phí |
|---|---|---|---|---|
| 1 | **Backup & Restore** | Chỉ có backup, chưa có gì chạy | Hàng giờ | Rẻ nhất |
| 2 | **Pilot Light** | Hệ thống lõi tối thiểu luôn chạy | RTO khoảng chục phút | Thấp |
| 3 | **Warm Standby** | Bản thu nhỏ của hệ thống chạy sẵn | RTO vài phút | Trung bình |
| 4 | **Multi-Site Active-Active** | Hệ thống đầy đủ chạy đồng thời ở nhiều Region | RTO gần 0 | Đắt nhất |

**Chi tiết từng chiến lược:**

**(1) Backup & Restore — rẻ nhất, chậm nhất**
- Chỉ sao lưu dữ liệu (S3, snapshot, AWS Backup) sang Region khác. Khi có thảm họa mới bắt đầu dựng lại hạ tầng từ backup (thường bằng IaC như CloudFormation).
- RPO phụ thuộc tần suất backup, RTO phụ thuộc thời gian restore + dựng hạ tầng — tính bằng **hàng giờ**.
- Phù hợp: hệ thống không trọng yếu, ngân sách thấp, doanh nghiệp chấp nhận downtime dài.

**(2) Pilot Light — "mồi lửa" luôn cháy**
- Ví von bếp gas: ngọn lửa mồi nhỏ luôn cháy sẵn, cần là bùng lên ngay.
- Ở DR Region chỉ chạy **thành phần lõi tối thiểu** — quan trọng nhất là dữ liệu được replicate liên tục (ví dụ database replica). Phần ứng dụng tắt hoặc gần như tắt.
- Khi có thảm họa: bật scale up tầng ứng dụng xung quanh dữ liệu đã sẵn sàng → RTO khoảng **chục phút**.

**(3) Warm Standby — bản thu nhỏ chạy sẵn**
- Một phiên bản **thu nhỏ nhưng đầy đủ chức năng** của hệ thống chạy sẵn ở DR Region (ít instance hơn, cấu hình nhỏ hơn), dữ liệu replicate liên tục.
- Khi có thảm họa: chỉ cần **scale up** lên kích thước production và chuyển traffic qua → RTO **vài phút**, nhanh hơn Pilot Light vì ứng dụng đã chạy sẵn, không phải dựng từ lõi.

**(4) Multi-Site Active-Active — nhanh nhất, đắt nhất**
- Hệ thống đầy đủ chạy **đồng thời** ở 2+ Region, traffic được phân phối qua cả hai (Route 53 / Global Accelerator). Một Region sập, Region còn lại gánh ngay.
- RTO **gần 0**, RPO gần 0. Đánh đổi: chi phí gần như gấp đôi và độ phức tạp vận hành cao nhất (xung đột dữ liệu hai chiều, consistency).
- Chỉ chọn khi scenario ghi rõ yêu cầu downtime gần như bằng 0 cho hệ thống trọng yếu.

### 3. Công cụ hỗ trợ DR trên AWS

- **AWS Backup:** dịch vụ **sao lưu tập trung (centralized backup)** cho nhiều dịch vụ AWS (EC2, EBS, RDS, DynamoDB, EFS...) — một nơi quản lý backup plan, chính sách lưu trữ, sao chép cross-Region. Đề hỏi "centrally manage backups across services" → AWS Backup.
- **S3 Cross-Region Replication (CRR):** tự động sao chép object sang bucket ở Region khác — nền tảng DR cho dữ liệu lưu trên S3.
- **RDS / Aurora Global Database:** replicate database xuyên Region. Aurora Global Database có độ trễ replication thường dưới 1 giây, phục vụ failover nhanh và read ở nhiều Region — công cụ quen thuộc cho Pilot Light / Warm Standby ở tầng dữ liệu.
- **Route 53 Failover Routing Policy:** gắn health check vào DNS record; khi endpoint chính fail health check, Route 53 tự chuyển traffic sang endpoint dự phòng. Đây là **cơ chế chuyển traffic** trong hầu hết kịch bản failover.
- **AWS DRS — Elastic Disaster Recovery:** ở mức khái niệm, là dịch vụ replicate liên tục ở tầng block storage của server (on-premises hoặc cloud khác) về AWS, để khi có thảm họa có thể khởi chạy máy chủ phục hồi trên AWS trong vài phút. Đề hỏi "continuously replicate on-premises servers to AWS for disaster recovery" → AWS DRS.

### 4. Nguyên tắc vàng khi chọn chiến lược

**Chọn theo yêu cầu kinh doanh về RPO/RTO và mức độ trọng yếu của hệ thống — không chọn cái đắt nhất mặc định.**

Trong phòng thi: đọc số RPO/RTO trong scenario trước, rồi đối chiếu bảng 4 chiến lược. Trong thực tế: mỗi giờ downtime tốn bao nhiêu tiền thiệt hại sẽ quyết định ngân sách DR xứng đáng — Active-Active cho hệ thống nội bộ ít người dùng là lãng phí, Backup & Restore cho hệ thống thanh toán là tự sát.

## Ví dụ đời thường

Hãy hình dung bạn mở một quán phở và lo sợ mặt bằng chính bị cháy (thảm họa):

- **RPO** là chuyện sổ sách/nguyên liệu: nếu cháy, bạn chấp nhận mất sổ sách ghi chép tới lúc nào? Sao lưu sổ mỗi ngày = RPO 24 giờ.
- **RTO** là chuyện mở bán lại: mất bao lâu từ lúc cháy tới lúc bán được bát phở đầu tiên ở địa điểm mới?
- **Backup & Restore:** bạn chỉ cất công thức và sổ sách ở nhà. Cháy quán thì đi thuê mặt bằng mới, mua nồi mới — rẻ nhất nhưng mấy ngày mới bán lại.
- **Pilot Light:** bạn giữ sẵn một mặt bằng nhỏ với bếp và nước dùng (phần lõi) luôn sẵn sàng. Cháy quán chính thì gọi nhân viên tới, mua thêm bàn ghế là bán được sau vài chục phút.
- **Warm Standby:** bạn có quán thứ hai nhỏ hơn đang bán thật, ít bàn hơn. Quán chính cháy thì dồn khách sang quán hai và kê thêm bàn — chỉ mất vài phút.
- **Active-Active:** hai quán lớn bằng nhau cùng đang bán, khách chia đều. Một quán cháy, quán còn lại gánh hết ngay lập tức — nhưng bạn trả tiền thuê hai mặt bằng lớn quanh năm.

## Phân biệt dễ nhầm

- **RPO vs RTO:** RPO = mất bao nhiêu **dữ liệu** (nhìn về quá khứ). RTO = mất bao lâu **thời gian** để sống lại (nhìn về tương lai). Đề cố tình hoán đổi hai con số này trong đáp án.
- **Pilot Light vs Warm Standby:** Cả hai đều có dữ liệu replicate sẵn. Khác biệt: Pilot Light chỉ có **lõi tối thiểu** chạy (chủ yếu là dữ liệu), tầng ứng dụng phải bật/scale khi failover. Warm Standby có **cả hệ thống thu nhỏ chạy sẵn**, failover chỉ là scale up. Warm Standby nhanh hơn và đắt hơn.
- **Multi-AZ vs Multi-Region DR:** Multi-AZ chống lỗi ở tầng Availability Zone trong cùng Region (dịch vụ như RDS Multi-AZ) — đây là High Availability, **không phải** DR xuyên Region. Thảm họa cấp Region cần chiến lược Multi-Region.
- **AWS Backup vs AWS DRS:** Backup sao lưu dữ liệu theo lịch để restore sau. DRS replicate liên tục ở tầng block của server để **khởi chạy lại server** trên AWS khi có thảm họa — mục đích và cơ chế khác nhau.
- **S3 CRR vs S3 Versioning:** Versioning giữ các phiên bản trong cùng bucket/Region. CRR sao object **sang Region khác**. Chống thảm họa Region phải có CRR.

## Bẫy đề thi

- **Bẫy 1:** Scenario cho "RTO of 15 minutes, RPO of 1 hour, minimize cost" — đáp án cám dỗ là Warm Standby/Active-Active cho "chắc ăn". Nhưng Pilot Light với dữ liệu replicate liên tục đáp ứng được mức chục phút với chi phí thấp hơn. Thi SAA là thi **đủ yêu cầu với chi phí thấp nhất**, không phải mạnh nhất.
- **Bẫy 2:** Đề hỏi RPO nhưng đáp án diễn đạt bằng thời gian downtime, hoặc ngược lại. Luôn tự hỏi: câu này đang nói về **mất dữ liệu** hay **thời gian phục hồi**?
- **Bẫy 3:** Chọn RDS Multi-AZ làm giải pháp "disaster recovery across Regions" — sai phạm vi, Multi-AZ chỉ trong một Region.
- **Bẫy 4:** Quên cơ chế chuyển traffic: dựng xong hệ thống dự phòng nhưng đáp án thiếu Route 53 Failover / health check thì failover không tự xảy ra.
- **Bẫy 5:** Thấy chữ "backup" là chọn Backup & Restore, dù scenario yêu cầu RTO vài phút — restore từ backup không thể đạt RTO vài phút, phải có hệ thống chạy sẵn (Warm Standby trở lên).

## Tóm tắt 5 dòng

- RPO = chấp nhận mất dữ liệu tới thời điểm nào (quá khứ); RTO = mất bao lâu để phục hồi (tương lai).
- Bốn chiến lược theo chi phí tăng / phục hồi nhanh dần: Backup & Restore (hàng giờ) → Pilot Light (chục phút) → Warm Standby (vài phút) → Multi-Site Active-Active (gần 0).
- Công cụ: AWS Backup tập trung, S3 CRR, RDS/Aurora Global Database, Route 53 Failover chuyển traffic, AWS DRS replicate server về AWS.
- Pilot Light chỉ chạy lõi dữ liệu tối thiểu; Warm Standby chạy sẵn bản thu nhỏ đầy đủ — phân biệt ở tầng ứng dụng có chạy sẵn hay không.
- Luôn chọn chiến lược theo RPO/RTO của bài toán kinh doanh, không mặc định chọn phương án đắt nhất.

## Quiz

**Question 1.** A company can tolerate losing no more than 15 minutes of transaction data if a disaster occurs, and the application must be running again within 30 minutes. In DR terminology, which pair correctly describes these requirements?

A. RPO is 30 minutes and RTO is 15 minutes.
B. RPO is 15 minutes and RTO is 30 minutes.
C. Both values describe the Recovery Time Objective.
D. RPO measures downtime and RTO measures data loss.

**Question 2.** A company requires a disaster recovery solution with an RTO of a few minutes. A scaled-down but fully functional version of the production environment must already be running in the DR Region with data replicated continuously, ready to scale up when a disaster occurs. Which DR strategy meets these requirements?

A. Backup and Restore
B. Pilot Light
C. Warm Standby
D. Multi-Site Active-Active with full capacity in both Regions

**Question 3.** A company wants the lowest-cost disaster recovery approach for a non-critical internal application. The business accepts an RTO of several hours and an RPO of several hours. Backups are copied to a second AWS Region, and infrastructure will be created from those backups only if a disaster occurs. Which DR strategy is this?

A. Backup and Restore
B. Warm Standby
C. Multi-Site Active-Active
D. Pilot Light with a running database replica

**Question 4.** A solutions architect must centrally manage and automate backups for Amazon EC2, Amazon RDS, Amazon EBS, and Amazon DynamoDB across multiple accounts, including copying backups to a second Region for disaster recovery. Which service should the architect use?

A. AWS Elastic Disaster Recovery (AWS DRS)
B. Amazon S3 Cross-Region Replication
C. AWS Backup
D. Amazon Route 53

**Question 5.** An application runs in a primary Region with a warm standby environment in a secondary Region. The company wants traffic to automatically move to the secondary Region if the primary Region's application endpoint becomes unhealthy. Which solution achieves this?

A. Amazon Route 53 failover routing policy with health checks
B. Amazon S3 Cross-Region Replication
C. AWS Backup with cross-Region copy
D. An Amazon CloudFront origin group with a single origin

## Đáp án quiz

**Câu 1 — Đáp án B.** "Mất tối đa 15 phút dữ liệu" là RPO (nói về data loss, nhìn về quá khứ). "Chạy lại trong 30 phút" là RTO (nói về downtime, nhìn về tương lai). Đáp án A hoán đổi hai giá trị — đây là bẫy kinh điển. C và D sai định nghĩa.

**Câu 2 — Đáp án C.** Từ khóa "scaled-down but fully functional version already running" + RTO vài phút chính là định nghĩa Warm Standby. Backup & Restore (A) không có gì chạy sẵn, RTO hàng giờ. Pilot Light (B) chỉ có lõi dữ liệu tối thiểu, tầng ứng dụng chưa chạy nên phục hồi chậm hơn (chục phút). D đáp ứng được về tốc độ nhưng vượt yêu cầu và đắt nhất — đề yêu cầu đúng mô tả của Warm Standby.

**Câu 3 — Đáp án A.** Chỉ có backup ở Region khác, hạ tầng dựng lại khi có thảm họa, RPO/RTO hàng giờ, chi phí thấp nhất → Backup & Restore. Các chiến lược còn lại đều có thành phần chạy sẵn ở DR Region nên đắt hơn mức cần thiết cho ứng dụng không trọng yếu.

**Câu 4 — Đáp án C.** AWS Backup là dịch vụ sao lưu **tập trung** cho nhiều dịch vụ AWS, hỗ trợ backup plan và cross-Region copy — khớp từng từ khóa trong đề. S3 CRR chỉ sao object S3, không quản lý backup của RDS/EC2/DynamoDB. AWS DRS replicate server ở tầng block để phục hồi máy chủ, không phải quản lý backup tập trung. Route 53 là DNS, không liên quan backup.

**Câu 5 — Đáp án A.** Route 53 failover routing + health check là cơ chế chuẩn để tự động chuyển traffic DNS sang Region dự phòng khi endpoint chính unhealthy. S3 CRR và AWS Backup lo về dữ liệu sao lưu, không chuyển traffic ứng dụng. CloudFront origin group cần cấu hình failover giữa các origin và không phải đáp án mô tả đúng kịch bản chuyển traffic cấp Region trong ngữ cảnh này như Route 53.
