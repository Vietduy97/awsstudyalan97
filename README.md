# ☁️ Học AWS SAA-C03 — Website tự học tiếng Việt

Website tĩnh (static site) chứa trọn bộ thư viện tự học **AWS Certified Solutions Architect – Associate (SAA-C03)** bằng tiếng Việt, dành cho người bắt đầu từ số 0:

- **21 bài học** theo lộ trình Beginner (Bài 00–12) → SAA nâng cao (Bài 13–20), mỗi bài kèm **quiz 5 câu** làm trực tiếp trên web, chấm điểm và hiện giải thích ngay.
- **3 đề mô phỏng** × 65 câu tiếng Anh kiểu đề thật: làm bài với đồng hồ đếm ngược **130 phút**, lưới điều hướng câu hỏi, nộp bài ra **điểm quy đổi /1000** (đạt từ 720) và lời giải thích tiếng Việt từng câu.
- **Cheat Sheet** tổng hợp + theo dịch vụ, **bảng phân biệt** các dịch vụ hay nhầm.
- **Kho tài liệu & video** chính thống (khóa học miễn phí, lab tiếng Việt, nguồn luyện đề uy tín).
- **Theo dõi tiến độ**: bài đã học, điểm quiz cao nhất, lịch sử thi thử — hiển thị ở trang chủ.

## Cách chạy trên máy local

Không cần cài gì ngoài Python 3:

```bash
cd aws-study-site
python3 -m http.server 8000
# Mở trình duyệt: http://localhost:8000
```

> Mở trực tiếp file `index.html` bằng trình duyệt cũng chạy được (mọi dữ liệu đều nhúng sẵn / nạp bằng thẻ script thường).

## Cách đưa lên GitHub Pages

1. Tạo repo mới trên GitHub, đẩy toàn bộ thư mục này lên nhánh `main`.
2. Vào repo → **Settings** → **Pages** → *Build and deployment* → Source: **Deploy from a branch** → Branch: `main` / thư mục `/ (root)` → Save.
3. Sau ~1 phút, web chạy tại `https://<tên-github>.github.io/<tên-repo>/`. Mọi đường link trong web đều là link tương đối nên chạy đúng cả ở thư mục con này.

## Lưu ý về tiến độ học

Web tĩnh không có máy chủ, nên tiến độ (bài đã học, điểm quiz, lịch sử thi) được lưu bằng **localStorage ngay trên trình duyệt** của bạn: đổi máy / đổi trình duyệt / xóa dữ liệu duyệt web thì tiến độ sẽ mất. Đây là đánh đổi cố ý để web chạy được ở bất cứ đâu mà không cần backend.

## Cập nhật nội dung

Toàn bộ nội dung gốc nằm ở dạng Markdown trong thư mục `content/` (32 file). Sửa nội dung ở đó rồi sinh lại web:

```bash
pip install markdown   # chỉ cần 1 lần
python3 tools/build.py # sinh lại toàn bộ HTML + dữ liệu quiz/đề thi
python3 tools/verify.py # kiểm tra: đủ 21 bài, 105 câu quiz, 3×65 câu đề thi
```

`tools/build.py` tự động: chuyển Markdown → HTML cho từng bài; tách quiz cuối mỗi bài và đáp án thành dữ liệu tương tác; gộp 3 bộ đề + file đáp án thành dữ liệu đề thi; biến bảng link trong kho tài liệu thành các thẻ (cards).

## Cấu trúc thư mục

```
.
├── index.html              # Trang chủ: dashboard tiến độ + lộ trình học
├── bai-hoc/                # Mục lục + 21 trang bài học (sinh tự động)
├── cheatsheet/             # 2 trang cheat sheet (sinh tự động)
├── phan-biet.html          # Bảng phân biệt dịch vụ (sinh tự động)
├── tai-lieu.html           # Kho tài liệu & video dạng thẻ (sinh tự động)
├── de-thi/                 # Mục lục đề + 3 trang làm bài (sinh tự động)
├── assets/
│   ├── css/style.css       # Giao diện (không dùng CDN)
│   ├── js/                 # app.js (tiến độ), quiz.js, exam.js
│   └── data/               # lessons.js, exams.js (sinh tự động)
├── content/                # ★ Nội dung gốc Markdown — sửa ở đây
└── tools/                  # build.py (sinh web), verify.py (kiểm tra)
```

## Nguồn nội dung

Nội dung học được biên soạn riêng cho thư viện này (đề mô phỏng là đề tự biên soạn theo format đề thật, không phải đề rò rỉ). Các link ngoài trỏ tới nguồn chính thống: AWS Skill Builder, freeCodeCamp, First Cloud Journey (AWS Study Group Vietnam), vntechies…
