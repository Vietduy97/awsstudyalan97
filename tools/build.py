#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build.py — Sinh website tĩnh từ các file Markdown trong thư mục content/.

Cách dùng:
    pip install markdown
    python3 tools/build.py

Kết quả: các file HTML + dữ liệu JSON/JS được ghi vào thư mục gốc của repo
(index.html, bai-hoc/, cheatsheet/, de-thi/, tai-lieu.html, phan-biet.html,
assets/data/). Chỉ cần chạy lại script này sau khi sửa nội dung trong content/.
"""
import json
import re
import sys
from pathlib import Path

try:
    import markdown as md_lib
except ImportError:
    sys.exit("Thiếu thư viện 'markdown'. Cài bằng: pip install markdown")

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"

MD_EXTENSIONS = ["tables", "fenced_code", "sane_lists"]

LESSON_RE = re.compile(r"^bai-(\d{2})-.*\.md$")


# ----------------------------------------------------------------------------
# Tiện ích chung
# ----------------------------------------------------------------------------
def md_to_html(text: str) -> str:
    return md_lib.markdown(text, extensions=MD_EXTENSIONS)


def js_json(obj) -> str:
    """JSON an toàn để nhúng vào <script> (tránh lỗi với '</script' và ký tự lạ)."""
    s = json.dumps(obj, ensure_ascii=False)
    return s.replace("</", "<\\/").replace(" ", "\\u2028").replace(" ", "\\u2029")


def title_of(text: str, fallback: str) -> str:
    m = re.search(r"(?m)^#\s+(.+)$", text)
    return m.group(1).strip() if m else fallback


def collapse_ws(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


# ----------------------------------------------------------------------------
# Phân tích Quiz trong bài học
# ----------------------------------------------------------------------------
Q_MARK = re.compile(r"^\*\*(?:Câu|Question)\s+(\d+)\s*[:.]\*\*\s*(.*)$")
A_MARK = re.compile(
    r"^\*\*(?:Câu|Question)\s+(\d+)\s+—\s+(?:Đáp án\s*:?\s*)?([A-E])\.?\*\*\s*(.*)$"
)
OPT_MARK = re.compile(r"^([A-F])[.)]\s+(.*)$")


def split_sections(text: str):
    """Chia markdown theo heading '## '. Trả về list (heading_line, body)."""
    parts = []
    cur_head, cur = None, []
    for line in text.splitlines():
        if line.startswith("## "):
            if cur_head is not None or cur:
                parts.append((cur_head, "\n".join(cur)))
            cur_head, cur = line, []
        else:
            cur.append(line)
    parts.append((cur_head, "\n".join(cur)))
    return parts


def parse_questions(block: str, qmark_re):
    """Tách các câu hỏi trong 1 block. Trả về dict {num: {text, options{letter: text}}}."""
    questions = {}
    cur_num, cur_lines = None, []
    for line in block.splitlines():
        m = qmark_re.match(line.strip())
        if m:
            if cur_num is not None:
                questions[cur_num] = _finish_question(cur_lines)
            cur_num, cur_lines = int(m.group(1)), [m.group(2)]
        elif cur_num is not None:
            cur_lines.append(line)
    if cur_num is not None:
        questions[cur_num] = _finish_question(cur_lines)
    return questions


def _finish_question(lines):
    qtext_parts, options, cur_opt = [], {}, None
    for raw in lines:
        line = raw.rstrip()
        om = OPT_MARK.match(line.strip())
        if om:
            cur_opt = om.group(1)
            options[cur_opt] = om.group(2).strip()
        elif cur_opt is not None:
            if line.strip():
                options[cur_opt] = (options[cur_opt] + " " + line.strip()).strip()
        else:
            qtext_parts.append(line)
    return {"text": collapse_ws(" ".join(qtext_parts)), "options": options}


def parse_answers(block: str, amark_re):
    """Tách đáp án + giải thích. Trả về dict {num: {answer, explanation}}."""
    answers = {}
    chunks = re.split(r"(?m)^(?=\*\*(?:Câu|Question)\s+\d+\s+—)", block)
    for chunk in chunks:
        lines = chunk.splitlines()
        if not lines:
            continue
        m = amark_re.match(lines[0].strip())
        if not m:
            continue
        num, letter = int(m.group(1)), m.group(2)
        rest = [m.group(3)] + lines[1:]
        expl = collapse_ws(" ".join(rest))
        expl = re.sub(r"^Giải thích:\s*", "", expl)
        answers[num] = {"answer": letter, "explanation": expl}
    return answers


def parse_lesson_quiz(text: str, fname: str):
    sections = split_sections(text)
    quiz_block = ans_block = None
    for head, body in sections:
        if head and head.startswith("## Quiz"):
            quiz_block = body
        if head and head.startswith("## Đáp án quiz"):
            ans_block = body
    if quiz_block is None or ans_block is None:
        raise ValueError(f"{fname}: không tìm thấy mục Quiz / Đáp án quiz")
    questions = parse_questions(quiz_block, Q_MARK)
    answers = parse_answers(ans_block, A_MARK)
    out = []
    for num in sorted(questions):
        q = questions[num]
        if num not in answers:
            raise ValueError(f"{fname}: Câu {num} thiếu đáp án")
        if len(q["options"]) < 4:
            raise ValueError(f"{fname}: Câu {num} chỉ có {len(q['options'])} lựa chọn")
        out.append(
            {
                "n": num,
                "text": q["text"],
                "options": q["options"],
                "answer": answers[num]["answer"],
                "explanation": answers[num]["explanation"],
            }
        )
    return out


def strip_quiz_sections(text: str) -> str:
    """Bỏ mục Quiz + Đáp án quiz khỏi thân bài (đã thay bằng quiz tương tác)."""
    kept = []
    for head, body in split_sections(text):
        if head and (head.startswith("## Quiz") or head.startswith("## Đáp án quiz")):
            continue
        if head is not None:
            kept.append(head)
        if body.strip():
            kept.append(body)
    return "\n".join(kept).strip() + "\n"


# ----------------------------------------------------------------------------
# Phân tích đề thi mô phỏng
# ----------------------------------------------------------------------------
EXAM_Q_MARK = re.compile(r"^\*\*Câu\s+(\d+)\.\*\*\s*(.*)$")
EXAM_A_MARK = re.compile(
    r"^\*\*Câu\s+(\d+)\s+—\s+Đáp án:\s+([A-E](?:\s*,\s*[A-E])*)\*\*\s*(.*)$"
)


def parse_exam(qtext: str, atext: str, setno: int):
    questions = parse_questions(qtext, EXAM_Q_MARK)
    answers = {}
    chunks = re.split(r"(?m)^(?=\*\*Câu\s+\d+\s+—)", atext)
    for chunk in chunks:
        lines = chunk.splitlines()
        if not lines:
            continue
        m = EXAM_A_MARK.match(lines[0].strip())
        if not m:
            continue
        num = int(m.group(1))
        letters = [x.strip() for x in m.group(2).split(",")]
        body_lines = [m.group(3)] + lines[1:]
        keyword = ""
        expl_lines = []
        for ln in body_lines:
            km = re.match(r"^\s*Keyword:\s*(.+)$", ln)
            if km:
                keyword = km.group(1).strip()
            else:
                expl_lines.append(ln)
        answers[num] = {
            "answers": letters,
            "explanation": collapse_ws(" ".join(expl_lines)),
            "keyword": keyword,
        }
    out = []
    for num in sorted(questions):
        q = questions[num]
        if num not in answers:
            raise ValueError(f"Đề {setno}: Câu {num} thiếu đáp án")
        a = answers[num]
        bad = [x for x in a["answers"] if x not in q["options"]]
        if bad:
            raise ValueError(f"Đề {setno}: Câu {num} đáp án {bad} không có trong lựa chọn")
        if not a["explanation"]:
            raise ValueError(f"Đề {setno}: Câu {num} thiếu giải thích")
        out.append(
            {
                "n": num,
                "text": q["text"],
                "options": q["options"],
                "answers": a["answers"],
                "multi": len(a["answers"]) > 1,
                "explanation": a["explanation"],
                "keyword": a["keyword"],
            }
        )
    return out


# ----------------------------------------------------------------------------
# Template trang
# ----------------------------------------------------------------------------
def page_shell(title, body, depth=0, extra_head="", extra_scripts=""):
    prefix = "../" * depth
    return f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — Học AWS SAA-C03</title>
<link rel="stylesheet" href="{prefix}assets/css/style.css">
{extra_head}</head>
<body>
<header class="site-header">
  <div class="header-inner">
    <a class="brand" href="{prefix}index.html">☁️ Học AWS <span>SAA-C03</span></a>
    <nav class="main-nav">
      <a href="{prefix}index.html">Trang chủ</a>
      <a href="{prefix}bai-hoc/index.html">Bài học</a>
      <a href="{prefix}cheatsheet/tong-hop.html">Cheat Sheet</a>
      <a href="{prefix}phan-biet.html">Phân biệt</a>
      <a href="{prefix}de-thi/index.html">Đề thi</a>
      <a href="{prefix}tai-lieu.html">Tài liệu &amp; Video</a>
    </nav>
  </div>
</header>
<main class="container">
{body}
</main>
<footer class="site-footer">
  <p>Thư viện tự học AWS SAA-C03 bằng tiếng Việt · Tiến độ học được lưu trên trình duyệt này (localStorage).</p>
</footer>
<script src="{prefix}assets/js/app.js"></script>
{extra_scripts}</body>
</html>
"""


def lesson_href(slug, depth):
    return ("../" * depth) + f"bai-hoc/{slug}.html"


# ----------------------------------------------------------------------------
# Build chính
# ----------------------------------------------------------------------------
def main():
    files = {p.name: p.read_text(encoding="utf-8") for p in sorted(CONTENT.glob("*.md"))}

    lesson_files = sorted(
        [n for n in files if LESSON_RE.match(n)], key=lambda n: int(LESSON_RE.match(n).group(1))
    )
    lessons = []  # {slug, num, title, group}
    for fname in lesson_files:
        num = int(LESSON_RE.match(fname).group(1))
        slug = f"bai-{num:02d}"
        lessons.append(
            {
                "slug": slug,
                "num": num,
                "file": fname,
                "title": title_of(files[fname], fname),
                "group": "beginner" if num <= 12 else "saa",
            }
        )

    # ---- Dữ liệu JS dùng chung: danh sách bài học -------------------------
    lessons_js = [
        {"slug": l["slug"], "num": l["num"], "title": l["title"], "group": l["group"]}
        for l in lessons
    ]
    (ROOT / "assets/data/lessons.js").write_text(
        "window.LESSONS = " + js_json(lessons_js) + ";\n", encoding="utf-8"
    )

    # ---- Trang từng bài học + quiz ---------------------------------------
    for i, les in enumerate(lessons):
        text = files[les["file"]]
        quiz = parse_lesson_quiz(text, les["file"])
        if len(quiz) != 5:
            raise ValueError(f"{les['file']}: quiz có {len(quiz)} câu (kỳ vọng 5)")
        body_html = md_to_html(strip_quiz_sections(text))
        prev_link = next_link = ""
        if i > 0:
            p = lessons[i - 1]
            prev_link = f'<a class="btn btn-ghost" href="{p["slug"]}.html">← {p["title"]}</a>'
        if i < len(lessons) - 1:
            n = lessons[i + 1]
            next_link = f'<a class="btn btn-ghost" href="{n["slug"]}.html">{n["title"]} →</a>'
        group_label = "Giai đoạn 1 · Beginner" if les["group"] == "beginner" else "Giai đoạn 2 · SAA nâng cao"
        body = f"""
<article class="lesson">
  <p class="crumb"><a href="index.html">Bài học</a> · {group_label}</p>
  <div class="md-body">{body_html}</div>
  <section class="lesson-actions">
    <label class="done-toggle"><input type="checkbox" id="lesson-done"> <span>Đánh dấu đã học xong bài này</span></label>
  </section>
  <section id="quiz-box" class="quiz-box"></section>
  <nav class="lesson-nav">{prev_link}<span class="spacer"></span>{next_link}</nav>
</article>
<script>window.LESSON_SLUG = "{les['slug']}"; window.QUIZ_DATA = {js_json(quiz)};</script>
"""
        html = page_shell(
            les["title"],
            body,
            depth=1,
            extra_scripts='<script src="../assets/js/quiz.js"></script>\n',
        )
        (ROOT / "bai-hoc" / f"{les['slug']}.html").write_text(html, encoding="utf-8")
    print(f"✓ {len(lessons)} trang bài học + quiz (21×5 câu)")

    # ---- Trang mục lục bài học -------------------------------------------
    def lesson_cards(group):
        cards = []
        for l in [x for x in lessons if x["group"] == group]:
            short = re.sub(r"^Bài \d+ — ", "", l["title"])
            cards.append(
                f"""<a class="lesson-card" href="{l['slug']}.html" data-slug="{l['slug']}" data-title="{l['title'].lower()}">
  <span class="lesson-num">Bài {l['num']:02d}</span>
  <span class="lesson-name">{short}</span>
  <span class="lesson-state" data-state-for="{l['slug']}"></span>
</a>"""
            )
        return "\n".join(cards)

    body = f"""
<h1>📚 Danh sách bài học</h1>
<p class="lead">21 bài học theo đúng lộ trình: Giai đoạn 1 (Beginner, Bài 00–12) rồi Giai đoạn 2 (SAA nâng cao, Bài 13–20). Mỗi bài có quiz 5 câu ở cuối.</p>
<div class="search-box"><input type="search" id="lesson-search" placeholder="🔎 Tìm bài học… (vd: S3, VPC, Lambda)"></div>
<h2>Giai đoạn 1 · Beginner — từ số 0</h2>
<div class="lesson-grid">{lesson_cards('beginner')}</div>
<h2>Giai đoạn 2 · SAA nâng cao</h2>
<div class="lesson-grid">{lesson_cards('saa')}</div>
<script>window.PAGE_INIT = 'lessons-index';</script>
"""
    (ROOT / "bai-hoc/index.html").write_text(page_shell("Danh sách bài học", body, depth=1), encoding="utf-8")

    # ---- Trang chủ / Dashboard --------------------------------------------
    roadmap_html = md_to_html(files["00-lo-trinh-va-huong-dan.md"])
    # Biến `ten-file.md` trong roadmap thành link tới trang tương ứng
    def file_link(m):
        fname = m.group(1)
        lm = LESSON_RE.match(fname)
        if lm:
            return f'<a href="bai-hoc/bai-{lm.group(1)}.html"><code>{fname}</code></a>'
        mapping = {
            "cheatsheet-tong-hop-saa.md": "cheatsheet/tong-hop.html",
            "cheatsheet-theo-dich-vu.md": "cheatsheet/theo-dich-vu.html",
            "phan-biet-cac-dich-vu.md": "phan-biet.html",
            "kho-tai-lieu-tham-khao.md": "tai-lieu.html",
            "de-mo-phong-01.md": "de-thi/index.html",
            "de-mo-phong-02.md": "de-thi/index.html",
            "de-mo-phong-03.md": "de-thi/index.html",
        }
        if fname in mapping:
            return f'<a href="{mapping[fname]}"><code>{fname}</code></a>'
        return m.group(0)

    roadmap_html = re.sub(r"<code>([a-z0-9\-]+\.md)</code>", file_link, roadmap_html)
    roadmap_html = roadmap_html.replace("<li>[ ]", '<li class="task-item"><span class="task-box"></span>')
    roadmap_html = roadmap_html.replace("<li>[x]", '<li class="task-item done"><span class="task-box checked"></span>')

    body = f"""
<section class="hero">
  <h1>☁️ Học AWS SAA-C03 — từ số 0 đến ngày thi</h1>
  <p>Thư viện tiếng Việt gồm 21 bài học, cheat sheet, bảng phân biệt dịch vụ, kho tài liệu/video và 3 đề mô phỏng 65 câu chấm điểm như thi thật.</p>
</section>
<section class="dashboard" id="dashboard">
  <div class="stat-card"><div class="stat-num" id="stat-lessons">–</div><div class="stat-label">Bài đã học / 21</div><div class="progress"><div class="progress-bar" id="bar-lessons"></div></div></div>
  <div class="stat-card"><div class="stat-num" id="stat-quizzes">–</div><div class="stat-label">Quiz đã làm (điểm cao nhất)</div><div class="progress"><div class="progress-bar" id="bar-quizzes"></div></div></div>
  <div class="stat-card"><div class="stat-num" id="stat-exams">–</div><div class="stat-label">Lượt thi thử · điểm cao nhất</div><div class="progress"><div class="progress-bar" id="bar-exams"></div></div></div>
  <div class="stat-card action-card">
    <div class="stat-label">Học tiếp từ chỗ dở</div>
    <a class="btn btn-primary" id="continue-btn" href="bai-hoc/index.html">Bắt đầu học →</a>
    <button class="btn btn-danger-ghost" id="reset-progress" type="button">Xóa tiến độ đã lưu</button>
  </div>
</section>
<section class="quick-links">
  <a class="quick-card" href="bai-hoc/index.html"><strong>📚 21 bài học</strong><span>Theo lộ trình Beginner → SAA</span></a>
  <a class="quick-card" href="de-thi/index.html"><strong>📝 3 đề mô phỏng</strong><span>65 câu · 130 phút · chấm điểm /1000</span></a>
  <a class="quick-card" href="cheatsheet/tong-hop.html"><strong>⚡ Cheat Sheet</strong><span>Ôn nước rút trước ngày thi</span></a>
  <a class="quick-card" href="tai-lieu.html"><strong>🎬 Tài liệu &amp; Video</strong><span>Khóa học, lab, nguồn chính thống</span></a>
</section>
<article class="md-body roadmap">{roadmap_html}</article>
<script src="assets/data/lessons.js"></script>
<script>window.PAGE_INIT = 'dashboard';</script>
"""
    (ROOT / "index.html").write_text(page_shell("Trang chủ", body, depth=0), encoding="utf-8")
    print("✓ Trang chủ / Dashboard + lộ trình")

    # ---- Cheat sheets & Phân biệt -----------------------------------------
    for src, out, title in [
        ("cheatsheet-tong-hop-saa.md", "cheatsheet/tong-hop.html", "Cheat Sheet Tổng Hợp"),
        ("cheatsheet-theo-dich-vu.md", "cheatsheet/theo-dich-vu.html", "Cheat Sheet Theo Dịch Vụ"),
        ("phan-biet-cac-dich-vu.md", "phan-biet.html", "Phân Biệt Các Dịch Vụ"),
    ]:
        html_body = md_to_html(files[src])
        switcher = ""
        if "cheatsheet" in src:
            other = "theo-dich-vu.html" if "tong-hop" in src else "tong-hop.html"
            other_label = "Cheat Sheet Theo Dịch Vụ" if "tong-hop" in src else "Cheat Sheet Tổng Hợp"
            switcher = f'<p class="crumb"><a href="{other}">→ Xem thêm: {other_label}</a></p>'
        body = f'<article class="md-body">{switcher}{html_body}</article>'
        depth = 1 if "/" in out else 0
        (ROOT / out).write_text(page_shell(title, body, depth=depth), encoding="utf-8")
    print("✓ Cheat sheets + Phân biệt")

    # ---- Tài liệu & Video: bảng → thẻ (cards) ------------------------------
    res_html = build_resources(files["kho-tai-lieu-tham-khao.md"])
    body = f'<article class="resources">{res_html}</article>'
    (ROOT / "tai-lieu.html").write_text(page_shell("Tài liệu & Video", body, depth=0), encoding="utf-8")
    print("✓ Tài liệu & Video (cards)")

    # ---- Đề thi ------------------------------------------------------------
    exams = {}
    for setno in (1, 2, 3):
        qs = parse_exam(
            files[f"de-mo-phong-0{setno}.md"], files[f"de-mo-phong-0{setno}-dap-an.md"], setno
        )
        if len(qs) != 65:
            raise ValueError(f"Đề {setno}: có {len(qs)} câu (kỳ vọng 65)")
        exams[str(setno)] = {
            "title": f"Đề mô phỏng SAA-C03 — Bộ 0{setno}",
            "minutes": 130,
            "passScore": 720,
            "questions": qs,
        }
    (ROOT / "assets/data/exams.js").write_text(
        "window.EXAM_DATA = " + js_json(exams) + ";\n", encoding="utf-8"
    )

    cards = "\n".join(
        f"""<a class="exam-card" href="lam-bai-{n}.html">
  <span class="exam-num">Bộ 0{n}</span>
  <span class="exam-name">Đề mô phỏng SAA-C03 — Bộ 0{n}</span>
  <span class="exam-meta">65 câu · 130 phút · đạt 720/1000</span>
  <span class="lesson-state" data-exam-state-for="{n}"></span>
</a>"""
        for n in (1, 2, 3)
    )
    body = f"""
<h1>📝 Đề thi mô phỏng SAA-C03</h1>
<p class="lead">3 bộ đề × 65 câu tiếng Anh kiểu đề thật. Làm bài có đồng hồ đếm ngược 130 phút, nộp bài để xem điểm quy đổi /1000 (đạt từ 720) và lời giải thích tiếng Việt cho từng câu.</p>
<div class="lesson-grid">{cards}</div>
<h2>Lịch sử làm bài của bạn</h2>
<div id="exam-history"><p class="muted">Chưa có lượt làm bài nào được lưu.</p></div>
<script>window.PAGE_INIT = 'exam-index';</script>
"""
    (ROOT / "de-thi/index.html").write_text(page_shell("Đề thi mô phỏng", body, depth=1), encoding="utf-8")

    for n in (1, 2, 3):
        body = f"""
<h1>📝 Đề mô phỏng — Bộ 0{n}</h1>
<div id="exam-root" data-set="{n}"></div>
<script src="../assets/data/exams.js"></script>
<script>window.PAGE_INIT = 'exam-run';</script>
"""
        html = page_shell(
            f"Làm bài — Đề mô phỏng Bộ 0{n}",
            body,
            depth=1,
            extra_scripts='<script src="../assets/js/exam.js"></script>\n',
        )
        (ROOT / f"de-thi/lam-bai-{n}.html").write_text(html, encoding="utf-8")
    print("✓ Đề thi: 3 bộ × 65 câu (kèm đáp án + giải thích)")

    print("\nHoàn tất. Chạy kiểm tra: python3 tools/verify.py")


def build_resources(text: str) -> str:
    """Kho tài liệu: mỗi mục '## ' chứa bảng link → chuyển thành lưới thẻ."""
    out = []
    sections = split_sections(text)
    for head, body in sections:
        if head is None:
            if body.strip():
                out.append(f'<div class="md-body">{md_to_html(body)}</div>')
            continue
        out.append(md_to_html(head))
        # Tách phần text thường và các dòng của bảng
        lines = body.splitlines()
        intro, rows, in_table = [], [], False
        for line in lines:
            s = line.strip()
            if s.startswith("|") and s.endswith("|"):
                cells = [c.strip() for c in s.strip("|").split("|")]
                if all(re.fullmatch(r":?-{2,}:?", c) for c in cells):
                    in_table = True
                    continue
                if not in_table and cells and ("Link" in cells or "Tài nguyên" in cells or "Tài liệu" in cells or "Khóa học" in cells):
                    in_table = True  # dòng tiêu đề bảng
                    continue
                if len(cells) >= 3:
                    rows.append(cells[:3])
                elif len(cells) == 2:
                    rows.append([cells[0], cells[1], ""])
                in_table = True
            else:
                if s:
                    intro.append(line)
        if intro:
            out.append(f'<div class="md-body">{md_to_html(chr(10).join(intro))}</div>')
        if rows:
            cards = []
            for name, link, note in rows:
                url = link if link.startswith("http") else ""
                name_html = md_to_html(name).replace("<p>", "").replace("</p>", "")
                note_html = md_to_html(note).replace("<p>", "").replace("</p>", "") if note else ""
                if url:
                    cards.append(
                        f'<a class="res-card" href="{url}" target="_blank" rel="noopener">'
                        f'<span class="res-name">{name_html}</span><span class="res-note">{note_html}</span>'
                        f'<span class="res-url">{url}</span></a>'
                    )
                else:
                    cards.append(
                        f'<div class="res-card"><span class="res-name">{name_html}</span>'
                        f'<span class="res-note">{note_html} {link}</span></div>'
                    )
            out.append('<div class="res-grid">' + "\n".join(cards) + "</div>")
    return "\n".join(out)


if __name__ == "__main__":
    main()
