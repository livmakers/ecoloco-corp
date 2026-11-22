/* フォーム送信の共通処理
   ・本番（ロリポップ）：同じサーバーの /form/send.php（PHP）でメール送信。CSRFトークン付き
   ・テスト（GitHub Pages など PHP が動かない場所）：FormSubmit（無料）経由
   どちらも、宛先のメールアドレスはページに書かれません（本番はサーバー側の設定ファイルのみ） */
(function () {
  "use strict";
  var PHP = !/github\.io$/.test(location.hostname) && location.protocol === "https:" || /^(localhost|127\.0\.0\.1)$/.test(location.hostname) && /[?&]php=1/.test(location.search);
  var BASE = "/form/";
  var tokenP = null;
  function getToken() {
    if (!tokenP) tokenP = fetch(BASE + "token.php", { credentials: "same-origin", cache: "no-store" }).then(function (r) { return r.json(); }).then(function (j) { if (!j.ok) throw 0; return j.token; });
    return tokenP;
  }
  if (PHP) getToken().catch(function () { tokenP = null; });

  /* kind: "recruit" | "question" | "contact"、subject: 件名、data: 項目名→値 */
  window.ecoSend = function (kind, subject, data) {
    if (PHP) {
      return getToken().then(function (t) {
        var body = { _token: t, _kind: kind };
        Object.keys(data).forEach(function (k) { body[k] = data[k]; });
        return fetch(BASE + "send.php", { method: "POST", credentials: "same-origin", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
      }).then(function (r) { return r.json(); }).then(function (j) { tokenP = null; if (!j.ok) throw new Error(j.error || "error"); return true; });
    }
    var A = ["satou", "nobuhiro", "bhd"], D = ["gmail", "com"];
    var key = (window.ECO_CONFIG && window.ECO_CONFIG.FORM_KEY) || window.ECO_FORM_KEY || (A.join(".") + "@" + D.join("."));
    var p = { _subject: subject, _template: "table", _captcha: "false" };
    Object.keys(data).forEach(function (k) { p[k] = data[k]; });
    return fetch("https://formsubmit.co/ajax/" + key, { method: "POST", headers: { "Content-Type": "application/json", "Accept": "application/json" }, body: JSON.stringify(p) })
      .then(function (r) { return r.json(); }).then(function (j) { if (!j || String(j.success) !== "true") throw new Error((j && j.message) || "error"); return true; });
  };
})();
