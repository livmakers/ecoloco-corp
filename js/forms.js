/* フォーム送信：Google Apps Script（無料）へ送信 → スプレッドシート記録＋メール通知＋自動返信
   迷惑対策：ハニーポット／表示から最短秒数／連続送信の間隔制限 */
(function () {
  var CFG = window.ECO_CONFIG || {};
  var form = document.querySelector("form[data-form]");
  if (!form) return;
  var kind = form.getAttribute("data-form"); // "contact" | "recruit"
  var loadedAt = Date.now();
  var msg = form.querySelector(".msg");
  var btn = form.querySelector("button[type=submit]");
  var KEY = "eco_last_submit";

  function show(t, ng) { msg.textContent = t; msg.className = "msg show" + (ng ? " ng" : ""); msg.scrollIntoView({ block: "center", behavior: "smooth" }); }
  function validate() {
    var ok = true;
    Array.prototype.forEach.call(form.querySelectorAll("[data-required]"), function (f) {
      var wrap = f.closest(".field") || f.closest("fieldset");
      var v = f.type === "checkbox" ? f.checked : (f.value || "").trim();
      var bad = !v;
      if (!bad && f.type === "email") bad = !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v);
      if (!bad && f.type === "url" && v) bad = !/^https?:\/\//.test(v);
      wrap.classList.toggle("bad", bad); if (bad) ok = false;
    });
    return ok;
  }
  form.addEventListener("input", function (e) { var w = e.target.closest(".field"); if (w) w.classList.remove("bad"); });

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    msg.className = "msg";
    if (form.elements["website"] && form.elements["website"].value) { return; }          // ハニーポット（ボットは黙って無視）
    if (!validate()) { show("未入力または形式の違う項目があります。赤く表示された項目をご確認ください。", true); var b = form.querySelector(".bad"); if (b) b.scrollIntoView({ block: "center" }); return; }
    if ((Date.now() - loadedAt) / 1000 < (CFG.MIN_FILL_SECONDS || 4)) { show("送信を少しだけお待ちください。もう一度ボタンを押してください。", true); return; }
    try { var last = +localStorage.getItem(KEY) || 0; if ((Date.now() - last) / 1000 < (CFG.SUBMIT_INTERVAL_SECONDS || 60)) { show("続けての送信はご遠慮いただいております。しばらくしてからお試しください。", true); return; } } catch (x) {}

    var data = { kind: kind, page: location.href, sentAt: new Date().toISOString() };
    Array.prototype.forEach.call(form.elements, function (f) {
      if (!f.name || f.name === "website" || f.type === "submit" || f.type === "button") return;
      if (f.type === "checkbox") data[f.name] = f.checked ? "同意" : "";
      else if (f.type === "radio") { if (f.checked) data[f.name] = f.value; }
      else data[f.name] = (f.value || "").trim();
    });
    btn.disabled = true; btn.textContent = "送信中…";

    function done() { try { localStorage.setItem(KEY, Date.now()); } catch (x) {} location.href = "thanks.html?type=" + kind; }
    if (!CFG.GAS_ENDPOINT) { /* 未設定時：ローカル確認用。実際には送信されません */
      try { localStorage.setItem("eco_last_payload", JSON.stringify(data)); } catch (x) {}
      console.info("[ECOLOCO] GAS_ENDPOINT未設定のため送信していません（テストモード）", data); done(); return;
    }
    // text/plain で送るとCORSプリフライトが不要（GASの標準的な受け方）
    fetch(CFG.GAS_ENDPOINT, { method: "POST", headers: { "Content-Type": "text/plain;charset=utf-8" }, body: JSON.stringify(data), redirect: "follow" })
      .then(function (r) { return r.json(); })
      .then(function (j) { if (j && j.ok) done(); else throw new Error((j && j.error) || "error"); })
      .catch(function () {
        btn.disabled = false; btn.textContent = "送信する";
        show("申し訳ありません、送信できませんでした。お手数ですが、時間をおいて再度お試しいただくか、メール（" + (CFG.NOTIFY_EMAIL || "") + "）またはお電話（06-6281-0800／平日10:00〜13:00）でご連絡ください。", true);
      });
  });
})();
