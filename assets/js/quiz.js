/* Quiz cuối bài học: render từ window.QUIZ_DATA, chấm điểm ngay, hiện giải thích,
   lưu điểm cao nhất vào localStorage (qua AWSStudy). */
(function () {
  "use strict";

  function esc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  document.addEventListener("DOMContentLoaded", function () {
    var slug = window.LESSON_SLUG;
    var quiz = window.QUIZ_DATA || [];
    var box = document.getElementById("quiz-box");
    if (!box) return;

    /* --- Checkbox "đã học xong" --- */
    var doneBox = document.getElementById("lesson-done");
    if (doneBox && window.AWSStudy) {
      doneBox.checked = window.AWSStudy.isLessonDone(slug);
      doneBox.addEventListener("change", function () {
        window.AWSStudy.setLessonDone(slug, doneBox.checked);
      });
    }

    if (!quiz.length) { box.style.display = "none"; return; }

    var html = "<h2>📝 Quiz cuối bài — " + quiz.length + " câu kiểu đề thi</h2>" +
      '<p class="muted">Chọn đáp án rồi bấm "Nộp bài quiz" để xem điểm và giải thích. Đáp án gốc nằm ở cuối file bài học.</p>';
    quiz.forEach(function (q, qi) {
      html += '<div class="q-block" data-q="' + qi + '">';
      html += '<div class="q-text">Câu ' + (qi + 1) + ". " + esc(q.text) + "</div>";
      Object.keys(q.options).sort().forEach(function (letter) {
        html += '<label class="opt" data-letter="' + letter + '">' +
          '<input type="radio" name="q' + qi + '" value="' + letter + '">' +
          '<span class="opt-letter">' + letter + ".</span><span>" + esc(q.options[letter]) + "</span></label>";
      });
      html += '<div class="q-explain" id="expl-' + qi + '"></div>';
      html += "</div>";
    });
    html += '<div class="exam-controls"><button class="btn btn-primary" id="quiz-submit" type="button">Nộp bài quiz</button>' +
      '<button class="btn" id="quiz-reset" type="button">Làm lại</button></div>' +
      '<div id="quiz-result"></div>';
    box.innerHTML = html;

    box.querySelectorAll(".opt input").forEach(function (inp) {
      inp.addEventListener("change", function () {
        var label = inp.closest(".opt");
        var block = inp.closest(".q-block");
        block.querySelectorAll(".opt").forEach(function (o) { o.classList.remove("selected"); });
        label.classList.add("selected");
      });
    });

    document.getElementById("quiz-submit").addEventListener("click", function () {
      var correct = 0;
      quiz.forEach(function (q, qi) {
        var block = box.querySelector('[data-q="' + qi + '"]');
        var picked = block.querySelector("input:checked");
        var pickedLetter = picked ? picked.value : null;
        var isRight = pickedLetter === q.answer;
        if (isRight) correct++;
        block.querySelectorAll(".opt").forEach(function (o) {
          var letter = o.getAttribute("data-letter");
          o.querySelector("input").disabled = true;
          o.classList.remove("selected");
          if (letter === q.answer) o.classList.add("correct");
          else if (letter === pickedLetter) o.classList.add("wrong");
        });
        var expl = document.getElementById("expl-" + qi);
        expl.innerHTML = (isRight
          ? '<span class="verdict-ok">✔ Đúng!</span>'
          : '<span class="verdict-bad">✘ Chưa đúng.</span> Đáp án đúng: <strong>' + q.answer + "</strong>. ") +
          esc(q.explanation);
        expl.classList.add("show");
      });
      var total = quiz.length;
      var pct = Math.round((correct / total) * 100);
      var passed = correct >= Math.ceil(total * 0.8);
      var res = document.getElementById("quiz-result");
      res.innerHTML = '<div class="quiz-result ' + (passed ? "pass" : "fail") + '">' +
        'Kết quả: <span class="big-score">' + correct + "/" + total + "</span> (" + pct + "%) — " +
        (passed ? "Tốt lắm! Bạn đã nắm chắc bài này." : "Hãy đọc lại phần lý thuyết rồi làm lại nhé.") + "</div>";
      if (window.AWSStudy) window.AWSStudy.recordQuiz(slug, correct, total);
      res.scrollIntoView({ behavior: "smooth", block: "center" });
    });

    document.getElementById("quiz-reset").addEventListener("click", function () {
      location.reload();
    });
  });
})();
