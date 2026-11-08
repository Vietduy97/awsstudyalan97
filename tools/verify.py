#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verify.py — Kiểm tra nhanh website đã sinh: đủ trang, đủ câu hỏi, không lỗi ký tự."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
errors, notes = [], []


def check(cond, msg):
    (notes if cond else errors).append(("✓ " if cond else "✘ ") + msg)


# 1) Đủ 21 trang bài học
lessons = sorted((ROOT / "bai-hoc").glob("bai-*.html"))
check(len(lessons) == 21, f"Số trang bài học: {len(lessons)} (kỳ vọng 21)")

# 2) Các trang chính tồn tại
for p in ["index.html", "bai-hoc/index.html", "cheatsheet/tong-hop.html",
          "cheatsheet/theo-dich-vu.html", "phan-biet.html", "tai-lieu.html",
          "de-thi/index.html", "de-thi/lam-bai-1.html", "de-thi/lam-bai-2.html",
          "de-thi/lam-bai-3.html", "assets/css/style.css", "assets/js/app.js",
          "assets/js/quiz.js", "assets/js/exam.js"]:
    check((ROOT / p).exists(), f"Tồn tại: {p}")

# 3) Dữ liệu đề thi: 3 bộ × 65 câu, đáp án hợp lệ, có giải thích
exams_js = (ROOT / "assets/data/exams.js").read_text(encoding="utf-8")
data = json.loads(exams_js[len("window.EXAM_DATA = "):].rstrip().rstrip(";"))
for setno in ("1", "2", "3"):
    qs = data[setno]["questions"]
    check(len(qs) == 65, f"Bộ {setno}: {len(qs)} câu (kỳ vọng 65)")
    bad = [q["n"] for q in qs if len(q["options"]) < 4 or not q["explanation"]
           or any(a not in q["options"] for a in q["answers"])]
    check(not bad, f"Bộ {setno}: mọi câu có ≥4 lựa chọn, đáp án hợp lệ, có giải thích" + (f" (lỗi: {bad})" if bad else ""))
    multi = sum(1 for q in qs if q["multi"])
    notes.append(f"  · Bộ {setno}: {multi} câu chọn 2 đáp án")

# 4) Quiz nhúng trong từng trang bài: 5 câu/trang
total_quiz = 0
for lp in lessons:
    html = lp.read_text(encoding="utf-8")
    m = re.search(r"window\.QUIZ_DATA = (\[.*?\]);</script>", html, re.S)
    if not m:
        errors.append(f"✘ {lp.name}: không thấy QUIZ_DATA")
        continue
    quiz = json.loads(m.group(1))
    total_quiz += len(quiz)
    if len(quiz) != 5:
        errors.append(f"✘ {lp.name}: quiz {len(quiz)} câu (kỳ vọng 5)")
    for q in quiz:
        if len(q["options"]) < 4 or q["answer"] not in q["options"] or not q["explanation"]:
            errors.append(f"✘ {lp.name}: câu {q['n']} thiếu dữ liệu")
check(total_quiz == 105, f"Tổng câu quiz: {total_quiz} (kỳ vọng 21×5=105)")

# 5) Toàn vẹn tiếng Việt: không ký tự thay thế U+FFFD, còn nguyên dấu
all_html = ""
for p in ROOT.rglob("*.html"):
    all_html += p.read_text(encoding="utf-8")
check("�" not in all_html, "Không có ký tự lỗi mã hóa (U+FFFD) trong HTML")
for probe in ["Bài học", "Đề thi mô phỏng", "Đã học", "Giải thích"]:
    check(probe in all_html, f"Chuỗi tiếng Việt nguyên vẹn: '{probe}'")

print("\n".join(notes))
if errors:
    print("\n".join(errors))
    sys.exit(1)
print("\nTẤT CẢ KIỂM TRA ĐỀU ĐẠT ✔")
