# Bài 06 — EBS & EFS: Ổ đĩa cho EC2 và đĩa dùng chung

## Mục tiêu bài học
- Phân biệt rạch ròi 3 loại lưu trữ hay bị trộn lẫn nhất trong đề SAA-C03: `S3`, `EBS`, `EFS`.
- Nhớ được các loại `EBS volume`: `gp3/gp2`, `io1/io2`, `st1`, `sc1` và chọn đúng theo `IOPS` / `throughput`.
- Hiểu `EBS Snapshot`, `EBS encryption` và vì sao `Instance Store` mất dữ liệu khi `stop/terminate`.
- Biết khi nào đề đang mô tả `EFS` — từ khóa `NFS`, nhiều EC2 dùng chung, nhiều AZ.

## Lý thuyết chính (tiếng Việt dễ hiểu, giữ nguyên thuật ngữ English)

### Quy tắc ghi nhớ của cả bài
> **S3 = file cho internet/app, EBS = đĩa của 1 server, EFS = đĩa dùng chung nhiều server.**

Nếu thuộc lòng câu này, bạn đã loại được ít nhất 1-2 đáp án sai trong rất nhiều câu hỏi.

### 1. EBS — Elastic Block Store
EBS là ổ đĩa mạng (`block storage`) gắn vào một máy chủ ảo `EC2 instance`. Hãy nghĩ như ổ SSD/HDD cắm vào 1 máy tính. Instance tắt thì dữ liệu trên EBS vẫn còn (trừ khi bạn cố tình đặt xóa root volume khi terminate).

Nguyên tắc cơ bản: **1 EBS volume chỉ gắn vào 1 EC2 tại một thời điểm**. Ngoại lệ duy nhất hay thi: dòng `io1/io2` hỗ trợ `Multi-Attach` nhưng giới hạn — chỉ trong cùng AZ, số instance giới hạn. Ngoài ngoại lệ đó, cứ thấy "nhiều server cùng ghi vào 1 ổ" là EBS sai.

EBS volume bị khóa trong 1 `Availability Zone (AZ)`. Muốn chuyển AZ khác phải đi qua Snapshot.

### 2. Các loại EBS volume — phần hay thi nhất bài này
- **gp3 / gp2 — General Purpose SSD:** ổ SSD đa dụng, cân bằng giá/hiệu năng, dùng cho hầu hết bài toán: ổ boot, web server, dev/test. **gp3 baseline: 3,000 IOPS và 125 MB/s throughput** — dù volume nhỏ cũng được mức nền này, và tăng IOPS/throughput độc lập với dung lượng. gp3 là đời mới, rẻ và tốt hơn gp2, đề thi hiện nay ưu tiên gp3.
- **io1 / io2 — Provisioned IOPS SSD:** SSD hiệu năng cao, bạn trả tiền để mua IOPS cam kết. Dùng cho database lớn, hệ thống cần IOPS rất cao và ổn định. Đây là nhóm duy nhất có Multi-Attach (giới hạn).
- **st1 — Throughput Optimized HDD:** ổ HDD cho `big data`, data warehouse, log processing — cần đọc/ghi tuần tự lượng lớn (`throughput` cao) chứ không cần IOPS cao. Không dùng làm ổ boot.
- **sc1 — Cold HDD:** HDD rẻ nhất, cho dữ liệu rất ít truy cập kiểu file archive trên block storage. Không dùng làm ổ boot.

Mẹo phân biệt: cần **IOPS** (nhiều thao tác nhỏ, database) → nhìn nhóm SSD, đặc biệt io1/io2. Cần **throughput** (ít thao tác nhưng mỗi thao tác rất to, big data) → st1.

### 3. EBS Snapshot — sao lưu
`Snapshot` là bản sao lưu của EBS volume, lưu lên S3 (do AWS quản lý, bạn không thấy bucket đó). Đặc điểm:
- **Incremental (tăng dần):** snapshot đầu sao toàn bộ, các lần sau chỉ sao phần block thay đổi — tiết kiệm dung lượng và tiền.
- Từ snapshot bạn tạo được volume mới, **copy snapshot qua AZ khác hoặc Region khác** — đây là cách di chuyển dữ liệu EBS qua Region và là nền tảng cho backup / disaster recovery của EC2.
- Snapshot có thể dùng để tạo AMI hoặc khôi phục volume khi hỏng.

### 4. EBS Encryption
Volume EBS có thể mã hóa (`encryption at rest`). Volume, snapshot tạo từ volume đó và dữ liệu truyền giữa EC2 và EBS đều được mã hóa. Muốn mã hóa một volume cũ chưa mã hóa: tạo snapshot → copy snapshot có bật encryption → tạo volume mới từ snapshot đã mã hóa đó. Không có công tắc bật encryption trực tiếp trên volume đang chạy.

### 5. Instance Store — đĩa vật lý tạm, cực nhanh nhưng mất là hết
`Instance Store` là ổ đĩa vật lý gắn trực tiếp vào máy chủ vật lý chứa EC2 instance của bạn. Tốc độ rất nhanh vì ở ngay trong máy.

Đổi lại: nó là `ephemeral storage` (lưu trữ tạm). **Instance bị stop hoặc terminate thì dữ liệu trên Instance Store mất sạch.** Reboot thì thường vẫn còn. Chỉ dùng cho cache, buffer, dữ liệu tạm — thứ mất cũng tạo lại được, tuyệt đối không để database hay file quan trọng ở đây.

### 6. EFS — Elastic File System
EFS là hệ thống file dùng chung theo giao thức `NFS`, hoạt động ở cấp `Region` và trải nhiều AZ.

- **Nhiều EC2 instance gắn (mount) vào cùng 1 EFS đồng thời** và cùng đọc/ghi — đây là khác biệt sống còn so với EBS.
- Tự động co giãn dung lượng theo lượng file, bạn không phải cấp phát trước như EBS.
- Có `storage class` IA: **EFS Infrequent Access (EFS IA)** kết hợp `lifecycle` — file ít truy cập tự chuyển sang lớp rẻ hơn, giống ý tưởng Lifecycle của S3.
- Chỉ dùng cho Linux (vì NFS). Đề nhắc Windows file share dùng chung thì không phải EFS.

Use case kinh điển: dàn web server nhiều instance cùng đọc/ghi một kho file chung (ảnh upload, file người dùng), WordPress dùng chung thư mục nội dung.

## Ví dụ đời thường
Hãy tưởng tượng bạn mở một quán cà phê có nhiều chi nhánh trong cùng thành phố.

**EBS** như tủ lạnh riêng trong bếp của 1 chi nhánh. Chỉ đầu bếp của chi nhánh đó mở được tủ đó. Chi nhánh đóng cửa nghỉ (stop) thì tủ lạnh vẫn cắm điện, đồ vẫn còn — đó là EBS. Nhưng tủ hỏng chi nhánh khác không dùng ké được.

**Instance Store** như thớt và rổ đựng nguyên liệu sơ chế để ngay trên bàn bếp. Dùng rất nhanh tay, nhưng quán đóng cửa dọn dẹp (terminate) là đổ bỏ hết. Không ai cất hành tỏi đã thái vào đó để qua tuần.

**EFS** như kho nguyên liệu trung tâm của cả chuỗi. Mọi chi nhánh cùng vào lấy cà phê, sữa, ly giấy từ một kho duy nhất. Thêm chi nhánh mới là nó vào dùng chung ngay, không phải mua kho riêng — đó chính là cảnh nhiều EC2 cùng mount EFS.

**S3** (nhắc lại bài trước) thì như bạn chụp ảnh món ăn và đăng lên fanpage cho cả internet xem — không phải tủ lạnh, cũng không phải kho bếp.

## Phân biệt dễ nhầm
| Tiêu chí | EBS | EFS | Instance Store |
|---|---|---|---|
| Gắn vào | 1 EC2 (trừ io2 Multi-Attach giới hạn) | Nhiều EC2 đồng thời | 1 EC2 (đĩa vật lý trong máy) |
| Phạm vi | 1 AZ | Cả Region, nhiều AZ | 1 instance |
| Giao thức / kiểu | Block storage | File system — NFS | Block storage vật lý |
| Stop instance | Dữ liệu còn | Dữ liệu còn (độc lập với EC2) | **Mất dữ liệu** |
| Dùng cho | Ổ đĩa server, database nhỏ | File dùng chung nhiều server | Cache / dữ liệu tạm |

Phân biệt thêm trong nhóm EBS:
- `gp3` vs `io2`: gp3 đủ cho 90% trường hợp, giá tốt. io2 khi cần IOPS cam kết rất cao, ổn định cho database quan trọng.
- `st1` vs `sc1`: cùng là HDD, st1 nhanh hơn cho big data throughput, sc1 rẻ nhất cho dữ liệu lạnh nhất.
- `IOPS` vs `throughput`: IOPS = số thao tác đọc/ghi mỗi giây. Throughput = lượng dữ liệu MB/s. Database cần IOPS, big data/log cần throughput.

## Bẫy đề thi
- Đề viết "multiple EC2 instances must access the same file system concurrently" + "NFS" → đáp án là **EFS**, không bao giờ là EBS thường.
- Thấy `io2 Multi-Attach` là ngoại lệ có giới hạn (cùng AZ) — đừng vì ngoại lệ này mà chọn EBS cho bài toán file share nhiều AZ.
- Câu hỏi về dữ liệu biến mất sau khi stop instance → thủ phạm là **Instance Store**, không phải EBS.
- Cần chuyển EBS volume sang AZ/Region khác → phải qua **Snapshot** (copy snapshot rồi tạo volume mới), không kéo trực tiếp volume qua được.
- Database cần IOPS cực cao và ổn định → `io1/io2`, không phải gp3. Ngược lại, web server thông thường chọn io2 là lãng phí tiền, đề Cost sẽ chấm sai.
- Chỉ nhớ con số này là đủ cho gp3: **3,000 IOPS + 125 MB/s baseline**. Đề hay dùng con số này làm keyword nhận diện.
- EFS là cho Linux qua NFS. Hệ điều hành và giao thức là gợi ý điểm trong đề.

## Tóm tắt 5 dòng
EBS là ổ đĩa block storage của 1 EC2 trong 1 AZ, snapshot sao lưu tăng dần và copy được qua Region/AZ.
gp3 là SSD đa dụng (baseline 3,000 IOPS, 125 MB/s), io1/io2 cho IOPS cam kết cao, st1/sc1 là HDD cho throughput và dữ liệu lạnh.
Instance Store nhanh nhưng là đĩa tạm — stop/terminate là mất dữ liệu.
EFS là file system NFS dùng chung cho nhiều EC2 đồng thời trên cả Region, có lớp IA + lifecycle.
Nhớ: S3 cho internet/app, EBS cho 1 server, EFS cho nhiều server dùng chung.

## Quiz — 5 câu hỏi tiếng Anh kiểu đề thi (A/B/C/D)

**Question 1.** A web application runs on multiple EC2 instances in different Availability Zones. All instances must read and write to the same shared file system at the same time using the NFS protocol. Which storage service should be used?
A. Amazon EBS gp3
B. EC2 Instance Store
C. Amazon EFS
D. Amazon S3 Glacier Deep Archive

**Question 2.** A database workload requires sustained high IOPS with consistent performance and the company is willing to pay for provisioned performance. Which EBS volume type is most appropriate?
A. sc1 Cold HDD
B. st1 Throughput Optimized HDD
C. gp3 General Purpose SSD with default settings only
D. io2 Provisioned IOPS SSD

**Question 3.** An EC2 instance was stopped for maintenance. After starting it again, the team found that data on one volume had disappeared, while data on the root volume remained intact. Which storage most likely lost the data?
A. Amazon EBS
B. EC2 Instance Store
C. Amazon EFS
D. EBS Snapshot stored in S3

**Question 4.** A company needs to move an EBS volume's data from `us-east-1` to `eu-west-1` for disaster recovery. What is the correct approach?
A. Directly attach the volume to an instance in eu-west-1
B. Create a snapshot, copy the snapshot to eu-west-1, then create a new volume from the copied snapshot
C. Enable EFS lifecycle on the volume
D. Convert the volume to S3 One Zone-IA

**Question 5.** A data analytics job processes very large files sequentially and needs high throughput at the lowest cost. IOPS is not a concern, and the volume will not be used as a boot volume. Which EBS type fits best?
A. io1 Provisioned IOPS SSD
B. st1 Throughput Optimized HDD
C. io2 Block Express
D. Instance Store

## Đáp án quiz

**Câu 1 — Đáp án C.** Từ khóa quyết định là "multiple instances + same file system + concurrently + NFS". Đó là mô tả textbook của EFS. EBS thường chỉ gắn 1 instance, Instance Store càng không dùng chung được, Glacier là archive của S3.

**Câu 2 — Đáp án D.** Cần IOPS cao, ổn định, chấp nhận trả tiền cho hiệu năng cam kết (`provisioned`) → io1/io2. st1/sc1 là HDD cho throughput/dữ liệu lạnh, không cho IOPS cao. gp3 tốt cho đa dụng (baseline 3,000 IOPS) nhưng không phải lựa chọn khi đề nhấn mạnh provisioned IOPS cho database lớn.

**Câu 3 — Đáp án B.** Chỉ Instance Store mới mất dữ liệu khi instance stop/terminate vì đó là đĩa vật lý tạm (`ephemeral`). EBS và EFS đều độc lập với vòng đời instance nên dữ liệu vẫn còn.

**Câu 4 — Đáp án B.** EBS volume bị khóa trong 1 AZ, không attach trực tiếp qua Region được. Cách chuẩn: tạo Snapshot → copy snapshot sang Region đích → tạo volume mới từ snapshot đã copy.

**Câu 5 — Đáp án B.** File lớn, đọc/ghi tuần tự, cần throughput cao, giá rẻ, không cần IOPS, không phải boot volume → st1 sinh ra đúng cho bài này (big data, log processing). io1/io2 đắt và thừa IOPS, là đáp án bẫy về chi phí.
