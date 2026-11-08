/* Làm bài thi mô phỏng: đồng hồ 130 phút, lưới điều hướng câu hỏi,
   nộp bài -> điểm quy đổi /1000 (đạt 720), xem lại từng câu kèm giải thích,
   lưu lượt thi vào localStorage (qua AWSStudy). */
(function () {
  "use strict";

  function esc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }
  function pad(n) { return (n < 10 ? "0" : "") + n; }
  function fmtClock(sec) {
    sec = Math.max(0, sec);
    var h = Math.floor(sec / 3600), m = Math.floor((sec % 3600) / 60), s = sec % 60;
    return (h > 0 ? h + ":" + pad(m) : m) + ":" + pad(s);
  }

  document.addEventListener("DOMContentLoaded", function () {
    var root = document.getElementById("exam-root");
    if (!root || !window.EXAM_DATA) return;
    var setNo = root.getAttribute("data-set");
    var exam = window.EXAM_DATA[setNo];
    if (!exam) { root.innerHTML = '<p class="muted">Không tìm thấy dữ liệu bộ đề này.</p>'; return; }
    var questions = exam.questions;
    var total = questions.length;
    var totalSec = (exam.minutes || 130) * 60;

    var state = {
      started: false, finished: false,
      current: 0,
      answers: {},   // qi -> [letters]
      marked: {},    // qi -> true
      remain: totalSec,
      timerId: null,
      startedAt: null
    };

    function renderStart() {
      root.innerHTML =
        '<div class="exam-panel"><h2>Hướng dẫn làm bài</h2>' +
        "<p>Bộ đề gồm <strong>" + total + " câu</strong> tiếng Anh kiểu đề thi thật, thời gian <strong>" +
        (exam.minutes || 130) + " phút</strong>. Điểm đạt: <strong>" + exam.passScore + "/1000</strong>.</p>" +
        "<ul><li>Câu thường: chọn 1 đáp án. Câu ghi <em>Select TWO</em>: chọn đúng 2 đáp án (chỉ tính điểm khi chọn đúng cả 2).</li>" +
        "<li>Dùng lưới câu hỏi bên phải để di chuyển, xem câu nào đã làm / chưa làm, và đánh dấu ★ những câu muốn xem lại.</li>" +
        "<li>Hết giờ hệ thống tự nộp bài. Kết quả và lời giải thích tiếng Việt hiện ngay sau khi nộp, và lượt thi được lưu vào lịch sử trên trình duyệt này.</li></ul>" +
        '<button class="btn btn-primary" id="exam-start" type="button">▶ Bắt đầu làm bài</button></div>';
      document.getElementById("exam-start").addEventListener("click", startExam);
    }

    function startExam() {
      state.started = true;
      state.startedAt = Date.now();
      renderExam();
      state.timerId = setInterval(function () {
        state.remain--;
        var t = document.getElementById("exam-timer");
        if (t) {
          t.textContent = "⏱ " + fmtClock(state.remain);
          t.classList.toggle("low", state.remain <= 600);
        }
        if (state.remain <= 0) finishExam(true);
      }, 1000);
    }

    function answeredCount() { return Object.keys(state.answers).filter(function (k) { return state.answers[k].length; }).length; }

    function renderExam() {
      var q = questions[state.current];
      var html = "";
      html += '<div class="exam-topbar"><span class="timer" id="exam-timer">⏱ ' + fmtClock(state.remain) + "</span>" +
        '<span class="exam-progress">Đã làm <strong id="exam-done-count">' + answeredCount() + "</strong>/" + total + " câu</span>" +
        '<span style="flex:1"></span>' +
        '<button class="btn" id="exam-mark" type="button">' + (state.marked[state.current] ? "★ Đã đánh dấu" : "☆ Đánh dấu xem lại") + "</button>" +
        '<button class="btn btn-primary" id="exam-submit" type="button">Nộp bài</button></div>';

      html += '<div class="exam-layout"><div class="exam-panel" id="exam-qpanel">' + questionHtml(q, state.current) + "</div>";
      html += '<aside class="qnav"><h3>Danh sách câu hỏi</h3><div class="qnav-grid">';
      questions.forEach(function (_, i) {
        var cls = ["qnav-cell"];
        if (state.answers[i] && state.answers[i].length) cls.push("answered");
        if (i === state.current) cls.push("current");
        if (state.marked[i]) cls.push("marked");
        html += '<button type="button" class="' + cls.join(" ") + '" data-goto="' + i + '">' + (i + 1) + "</button>";
      });
      html += '</div><div class="qnav-legend">■ Đã trả lời · □ Chưa trả lời · ● Đánh dấu xem lại<br>Khung cam = câu đang mở</div></aside></div>';
      root.innerHTML = html;
      bindExamEvents();
      window.scrollTo({ top: 0 });
    }

    function questionHtml(q, qi) {
      var picked = state.answers[qi] || [];
      var html = '<div class="q-text">Câu ' + (qi + 1) + "/" + total + ". " + esc(q.text) + "</div>";
      if (q.multi) html += '<p class="q-multi-hint">⚠ Câu này chọn 2 đáp án (Select TWO).</p>';
      Object.keys(q.options).sort().forEach(function (letter) {
        var checked = picked.indexOf(letter) !== -1 ? " checked" : "";
        var sel = checked ? " selected" : "";
        var type = q.multi ? "checkbox" : "radio";
        html += '<label class="opt' + sel + '" data-letter="' + letter + '">' +
          '<input type="' + type + '" name="eq" value="' + letter + '"' + checked + ">" +
          '<span class="opt-letter">' + letter + ".</span><span>" + esc(q.options[letter]) + "</span></label>";
      });
      html += '<div class="exam-controls">' +
        '<button class="btn" id="exam-prev" type="button"' + (qi === 0 ? " disabled" : "") + ">← Câu trước</button>" +
        '<button class="btn" id="exam-next" type="button"' + (qi === total - 1 ? " disabled" : "") + ">Câu tiếp →</button></div>";
      return html;
    }

    function bindExamEvents() {
      root.querySelectorAll("#exam-qpanel .opt input").forEach(function (inp) {
        inp.addEventListener("change", function () {
          var q = questions[state.current];
          if (q.multi) {
            var checked = Array.prototype.map.call(
              root.querySelectorAll("#exam-qpanel .opt input:checked"), function (i) { return i.value; });
            if (checked.length > q.answers.length) {
              inp.checked = false;
              alert("Câu này chỉ chọn đúng " + q.answers.length + " đáp án. Bỏ chọn một đáp án khác trước nhé.");
              return;
            }
            state.answers[state.current] = checked;
          } else {
            state.answers[state.current] = [inp.value];
          }
          root.querySelectorAll("#exam-qpanel .opt").forEach(function (o) {
            var on = o.querySelector("input").checked;
            o.classList.toggle("selected", on);
          });
          var dc = document.getElementById("exam-done-count");
          if (dc) dc.textContent = answeredCount();
          var cell = root.querySelector('[data-goto="' + state.current + '"]');
          if (cell) cell.classList.toggle("answered", !!(state.answers[state.current] && state.answers[state.current].length));
        });
      });
      root.querySelectorAll("[data-goto]").forEach(function (cell) {
        cell.addEventListener("click", function () {
          state.current = parseInt(cell.getAttribute("data-goto"), 10);
          renderExam();
        });
      });
      var prev = document.getElementById("exam-prev");
      var next = document.getElementById("exam-next");
      if (prev) prev.addEventListener("click", function () { if (state.current > 0) { state.current--; renderExam(); } });
      if (next) next.addEventListener("click", function () { if (state.current < total - 1) { state.current++; renderExam(); } });
      document.getElementById("exam-mark").addEventListener("click", function () {
        state.marked[state.current] = !state.marked[state.current];
        renderExam();
      });
      document.getElementById("exam-submit").addEventListener("click", function () {
        var left = total - answeredCount();
        var msg = left > 0
          ? "Bạn còn " + left + " câu chưa trả lời. Nộp bài luôn nhé?"
          : "Nộp bài và xem kết quả?";
        if (confirm(msg)) finishExam(false);
      });
    }

    function finishExam(auto) {
      if (state.finished) return;
      state.finished = true;
      if (state.timerId) clearInterval(state.timerId);
      var correct = 0;
      var review = questions.map(function (q, qi) {
        var picked = (state.answers[qi] || []).slice().sort();
        var right = q.answers.slice().sort();
        var ok = picked.length === right.length && picked.every(function (v, i) { return v === right[i]; });
        if (ok) correct++;
        return { q: q, qi: qi, picked: picked, ok: ok };
      });
      var scaled = Math.round(100 + (correct / total) * 900);
      var pass = scaled >= exam.passScore;
      var usedSec = totalSec - Math.max(0, state.remain);

      if (window.AWSStudy) {
        window.AWSStudy.recordExam({
          set: setNo, correct: correct, total: total, scaled: scaled, pass: pass,
          at: new Date().toISOString(), durationSec: usedSec
        });
      }

      var html = '<div class="exam-result ' + (pass ? "pass" : "fail") + '">' +
        (auto ? "<p><strong>⏰ Hết giờ — bài đã được tự động nộp.</strong></p>" : "") +
        'Kết quả: <span class="big-score">' + scaled + "</span>/1000 · đúng " + correct + "/" + total + " câu · " +
        (pass ? "🎉 <strong>ĐẠT</strong> (mốc đạt " + exam.passScore + ")" : "Chưa đạt — mốc đạt là " + exam.passScore + ", ôn thêm rồi làm lại nhé") +
        "<br><span class='muted'>Thời gian làm bài: " + fmtClock(usedSec) + " · Điểm quy đổi là ước lượng theo tỉ lệ câu đúng.</span></div>";
      html += '<div class="exam-controls"><a class="btn" href="index.html">← Về trang Đề thi</a><a class="btn btn-primary" href="lam-bai-' + setNo + '.html">Làm lại bộ này</a></div>';
      html += "<h2>Xem lại từng câu</h2>";
      review.forEach(function (r) {
        var q = r.q;
        html += '<div class="exam-panel" style="margin-top:14px"><div class="q-text">Câu ' + (r.qi + 1) + ". " + esc(q.text) + "</div>";
        if (q.multi) html += '<p class="q-multi-hint">⚠ Chọn 2 đáp án.</p>';
        Object.keys(q.options).sort().forEach(function (letter) {
          var cls = "opt";
          var isRight = q.answers.indexOf(letter) !== -1;
          var isPicked = r.picked.indexOf(letter) !== -1;
          if (isRight && isPicked) cls += " correct";
          else if (isPicked) cls += " wrong";
          else if (isRight) cls += " missed";
          html += '<div class="' + cls + '"><span class="opt-letter">' + letter + '.</span><span>' + esc(q.options[letter]) + "</span></div>";
        });
        html += '<div class="q-explain show">' +
          (r.ok ? '<span class="verdict-ok">✔ Bạn trả lời đúng.</span>'
                : '<span class="verdict-bad">✘ Chưa đúng.</span> Bạn chọn: <strong>' + (r.picked.join(", ") || "—") +
                  "</strong> · Đáp án đúng: <strong>" + q.answers.join(", ") + "</strong>. ") +
          esc(q.explanation) +
          (q.keyword ? '<br><span class="q-keyword">Keyword: ' + esc(q.keyword) + "</span>" : "") +
          "</div></div>";
      });
      root.innerHTML = html;
      window.scrollTo({ top: 0 });
    }

    renderStart();
  });
})();
