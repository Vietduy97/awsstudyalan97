/* Học AWS SAA-C03 — logic dùng chung: lưu tiến độ (localStorage), Dashboard,
   mục lục bài học, mục lục đề thi. */
(function () {
  "use strict";

  var KEY = "awsStudy.v1";

  function load() {
    try {
      var raw = localStorage.getItem(KEY);
      if (raw) {
        var data = JSON.parse(raw);
        if (data && typeof data === "object") {
          return {
            lessonsDone: data.lessonsDone || {},
            quizBest: data.quizBest || {},
            examAttempts: Array.isArray(data.examAttempts) ? data.examAttempts : []
          };
        }
      }
    } catch (e) { /* dữ liệu hỏng -> bắt đầu lại */ }
    return { lessonsDone: {}, quizBest: {}, examAttempts: [] };
  }

  function save(data) {
    try { localStorage.setItem(KEY, JSON.stringify(data)); } catch (e) { /* bỏ qua */ }
  }

  window.AWSStudy = {
    load: load,
    save: save,
    isLessonDone: function (slug) { return !!load().lessonsDone[slug]; },
    setLessonDone: function (slug, done) {
      var d = load();
      if (done) { d.lessonsDone[slug] = true; } else { delete d.lessonsDone[slug]; }
      save(d);
    },
    recordQuiz: function (slug, score, total) {
      var d = load(), cur = d.quizBest[slug];
      if (!cur || score > cur.score) {
        d.quizBest[slug] = { score: score, total: total, at: new Date().toISOString() };
        save(d);
      }
    },
    recordExam: function (attempt) {
      var d = load();
      d.examAttempts.push(attempt);
      save(d);
    }
  };

  function fmtDate(iso) {
    var d = new Date(iso);
    if (isNaN(d.getTime())) return "";
    return d.toLocaleString("vi-VN", { day: "2-digit", month: "2-digit", year: "numeric", hour: "2-digit", minute: "2-digit" });
  }
  window.AWSStudy.fmtDate = fmtDate;

  /* ---------------- Dashboard ---------------- */
  function initDashboard() {
    var lessons = window.LESSONS || [];
    var d = load();
    var doneCount = lessons.filter(function (l) { return d.lessonsDone[l.slug]; }).length;
    document.getElementById("stat-lessons").textContent = doneCount + " / " + lessons.length;
    document.getElementById("bar-lessons").style.width = (lessons.length ? (doneCount / lessons.length) * 100 : 0) + "%";

    var quizSlugs = Object.keys(d.quizBest);
    var quizSum = quizSlugs.reduce(function (s, k) { return s + d.quizBest[k].score; }, 0);
    var quizTotal = quizSlugs.reduce(function (s, k) { return s + d.quizBest[k].total; }, 0);
    document.getElementById("stat-quizzes").textContent =
      quizSlugs.length ? quizSum + " / " + quizTotal + " câu đúng" : "Chưa làm";
    document.getElementById("bar-quizzes").style.width =
      quizTotal ? (quizSum / quizTotal) * 100 + "%" : "0%";

    var attempts = d.examAttempts;
    var best = attempts.reduce(function (m, a) { return Math.max(m, a.scaled || 0); }, 0);
    document.getElementById("stat-exams").textContent =
      attempts.length ? attempts.length + " lượt · " + best + "/1000" : "Chưa thi";
    document.getElementById("bar-exams").style.width = (best / 1000) * 100 + "%";

    var next = lessons.filter(function (l) { return !d.lessonsDone[l.slug]; })[0];
    var btn = document.getElementById("continue-btn");
    if (next) {
      btn.href = "bai-hoc/" + next.slug + ".html";
      btn.textContent = (doneCount ? "Học tiếp: " : "Bắt đầu học: ") + next.title + " →";
    } else if (lessons.length) {
      btn.href = "de-thi/index.html";
      btn.textContent = "Đã học hết 21 bài — vào luyện đề →";
    }

    document.getElementById("reset-progress").addEventListener("click", function () {
      if (confirm("Xóa toàn bộ tiến độ đã lưu trên trình duyệt này (bài đã học, điểm quiz, lịch sử thi)?")) {
        try { localStorage.removeItem(KEY); } catch (e) {}
        location.reload();
      }
    });
  }

  /* ---------------- Mục lục bài học ---------------- */
  function initLessonsIndex() {
    var d = load();
    document.querySelectorAll("[data-state-for]").forEach(function (el) {
      var slug = el.getAttribute("data-state-for");
      var parts = [];
      if (d.lessonsDone[slug]) parts.push('<span class="done">✔ Đã học</span>');
      var qb = d.quizBest[slug];
      if (qb) parts.push("Quiz cao nhất: " + qb.score + "/" + qb.total);
      el.innerHTML = parts.join(" · ");
    });
    var input = document.getElementById("lesson-search");
    if (input) {
      input.addEventListener("input", function () {
        var q = input.value.trim().toLowerCase();
        document.querySelectorAll(".lesson-card").forEach(function (card) {
          var t = (card.getAttribute("data-title") || "");
          card.style.display = (!q || t.indexOf(q) !== -1) ? "" : "none";
        });
      });
    }
  }

  /* ---------------- Mục lục đề thi ---------------- */
  function initExamIndex() {
    var d = load();
    document.querySelectorAll("[data-exam-state-for]").forEach(function (el) {
      var set = el.getAttribute("data-exam-state-for");
      var mine = d.examAttempts.filter(function (a) { return String(a.set) === set; });
      if (mine.length) {
        var best = mine.reduce(function (m, a) { return Math.max(m, a.scaled || 0); }, 0);
        el.textContent = "Đã làm " + mine.length + " lượt · điểm cao nhất " + best + "/1000";
      } else {
        el.textContent = "Chưa làm bộ này";
      }
    });
    var box = document.getElementById("exam-history");
    if (box && d.examAttempts.length) {
      var rows = d.examAttempts.slice().reverse().map(function (a) {
        return "<tr><td>" + fmtDate(a.at) + "</td><td>Bộ 0" + a.set + "</td><td>" +
          a.correct + "/" + a.total + " câu đúng</td><td><strong>" + a.scaled + "</strong>/1000</td><td>" +
          (a.pass ? '<span class="pass-tag">ĐẠT</span>' : '<span class="fail-tag">Chưa đạt</span>') + "</td></tr>";
      }).join("");
      box.innerHTML = '<table class="history-table"><thead><tr><th>Thời gian</th><th>Bộ đề</th><th>Kết quả</th><th>Điểm quy đổi</th><th>Đánh giá</th></tr></thead><tbody>' + rows + "</tbody></table>";
    }
  }

  document.addEventListener("DOMContentLoaded", function () {
    var init = window.PAGE_INIT;
    if (init === "dashboard") initDashboard();
    else if (init === "lessons-index") initLessonsIndex();
    else if (init === "exam-index") initExamIndex();
    /* 'exam-run' do exam.js tự xử lý */
  });
})();
