/* ecoloco 採用サイト — 職種データ・フォーム送信（素のJS／ビルド不要）
   フォーム送信は FormSubmit（無料・継続課金なし）を使用。
   送信先は FORM_KEY で指定（有効化後はランダム文字列に差し替え、メールアドレスをページに出さない） */
(function () {
  "use strict";

  /* ===== 送信先 =====
     FORM_KEY：FormSubmit有効化メールに記載されるランダム文字列。
     未設定の間は、分割したアドレスを実行時に組み立てて使う（ソースにそのまま書かない） */
  var FORM_KEY = "";
  var A = ["satou", "nobuhiro", "bhd"], D = ["gmail", "com"];
  var target = FORM_KEY || (A.join(".") + "@" + D.join("."));
  var ENDPOINT = "https://formsubmit.co/ajax/" + target;

  /* ===== 募集職種 ===== */
  var JOBS = [
    { id: "mall", title: "ECモール運用", en: "EC MALL OPERATION", tag: "経験者", img: "../assets/img/tp-1104.webp",
      catch: "楽天市場を軸に、モール店舗の売上を伸ばす司令塔。",
      work: ["楽天市場などECモール店舗の運営全般（商品登録・ページ更新・在庫連動）", "スーパーSALE・お買い物マラソン等のイベント企画と販促設計", "RPPなどモール内広告の運用・改善", "アクセス・転換率・客単価の分析と改善施策の実行"],
      must: ["ECモール（楽天市場・Yahoo!ショッピング・Amazon等）での店舗運用経験"],
      want: ["アパレル・雑貨のモール運用経験", "モール広告の運用経験", "売上目標を持って改善を回した経験"] },
    { id: "own", title: "自社サイト運用", en: "D2C / OWN EC", tag: "経験者", img: "../assets/img/contents-260918-2.webp",
      catch: "ブランドの“本店”となる自社ECを育てる。",
      work: ["自社ECサイトの運営・更新・改善", "CRM（会員・メルマガ・LINE等）施策の企画と実行", "SEO・Web広告・LP改善による集客と転換率アップ", "モール・SNSと連動したキャンペーン設計"],
      must: ["自社ECサイト（Shopify・futureshop・MakeShop等）の運用経験"],
      want: ["Googleアナリティクス等での分析経験", "Web広告の運用経験", "HTML/CSSの基礎知識"] },
    { id: "md", title: "ECアパレルMD", en: "MERCHANDISER", tag: "経験者", img: "../assets/img/m13.webp",
      catch: "「何を・いつ・いくつ」売るかを決める、売上の設計者。",
      work: ["シーズンごとの商品構成・販売計画の立案", "仕入れ・生産数量の判断と在庫コントロール", "売れ筋・死に筋の分析と、値付け・追加・消化の判断", "撮影・ページ制作チームと連携した商品の打ち出し"],
      must: ["アパレルのMD・バイヤー・商品企画いずれかの経験"],
      want: ["EC中心のブランドでのMD経験", "ナチュラル素材（リネン・コットン・ウール）の知識", "Excel等での数値管理が得意な方"] },
    { id: "sns", title: "SNS運用", en: "SNS MARKETING", tag: "経験者", img: "../assets/img/contents-13623289.webp",
      catch: "ファンを増やし、SNSから売上をつくる。",
      work: ["公式Instagram（@ecoloco.official）等の企画・撮影・投稿", "リール・ストーリーズ・ライブ配信の企画運営", "インフルエンサー・UGCの活用", "フォロワー・保存数・EC送客などの分析と改善"],
      must: ["企業・ブランド・個人いずれかでのSNS運用経験"],
      want: ["アパレル・ライフスタイル系アカウントの運用経験", "スマホでの写真・動画撮影と編集", "SNS広告の運用経験"] },
    { id: "brand", title: "ブランド構築・商品開発", en: "BRANDING / PRODUCT", tag: "経験者", img: "../assets/img/sococoti-3.webp",
      catch: "オリジナルブランドの世界観と、看板商品をつくる。",
      work: ["オリジナルブランド（earth_eco_loco・SOCOCOTI・SO・sel・nachukara・DOVERS 等）のコンセプト設計・育成", "新商品・新シリーズの企画、素材・仕様の検討と取引先との調整", "ブランドの見せ方（ネーミング・ビジュアル・ページ・パッケージ）のディレクション", "新ブランドの立ち上げ"],
      must: ["ブランド構築、またはブランド商品（アパレル・雑貨等）の企画・開発経験"],
      want: ["仕入れ先・OEM先とのやりとり経験", "ブランドを立ち上げ・リブランディングした経験", "デザイナー・カメラマン等をディレクションした経験"] },
    { id: "will", title: "経験不問・やる気枠", en: "POTENTIAL", tag: "未経験OK", img: "../assets/img/m12.webp",
      catch: "経験より熱量。ガンガン挑戦したい人、大歓迎。",
      work: ["上記いずれかの職種のアシスタントからスタート", "商品登録・ページ更新・SNS投稿・データ集計など、EC運営の実務", "適性と希望に応じて、担当領域・責任範囲を広げていきます"],
      must: ["学ぶ意欲と行動量。指示待ちではなく、自分から動ける方"],
      want: ["ECや服が好きな方", "パソコンの基本操作（Excel・Googleスプレッドシート等）", "数字や成果にこだわれる方"] }
  ];

  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function li(a) { return "<ul>" + a.map(function (x) { return "<li>" + esc(x) + "</li>"; }).join("") + "</ul>"; }

  /* 職種カード */
  $("#jobs").innerHTML = JOBS.map(function (j, i) {
    return "<details class='job rv' id='job-" + j.id + "'><summary>" +
      "<span class='jimg'><img src='" + j.img + "' alt='' loading='lazy'></span>" +
      "<span class='jtx'><span class='jno'>0" + (i + 1) + " / " + esc(j.en) + "</span><span class='jt'>" + esc(j.title) + "<em class='" + (j.tag === "未経験OK" ? "ok" : "") + "'>" + esc(j.tag) + "</em></span><span class='jc'>" + esc(j.catch) + "</span></span>" +
      "<span class='pm' aria-hidden='true'></span></summary><div class='jbody'><dl>" +
      "<dt>仕事内容</dt><dd>" + li(j.work) + "</dd>" +
      "<dt>必須</dt><dd>" + li(j.must) + "</dd>" +
      "<dt>歓迎</dt><dd>" + li(j.want) + "</dd>" +
      "<dt>雇用形態・給与</dt><dd>ご経験・スキル・ご希望の働き方をふまえ、面接でご相談のうえ決定します。</dd>" +
      "<dt>勤務地</dt><dd>大阪府大阪市中央区久太郎町3丁目5番5号 丸忠第一ビル5F</dd>" +
      "</dl><a class='btn fill sm' href='#entry' data-job='" + esc(j.title) + "'>この職種に応募する</a></div></details>";
  }).join("");

  /* フォームの職種チップ・都道府県 */
  $("#job-chips").innerHTML = JOBS.map(function (j) {
    return "<label><input type='checkbox' name='希望職種' value='" + esc(j.title) + "'><span>" + esc(j.title) + "</span></label>";
  }).join("");
  var prefs = "北海道 青森県 岩手県 宮城県 秋田県 山形県 福島県 茨城県 栃木県 群馬県 埼玉県 千葉県 東京都 神奈川県 新潟県 富山県 石川県 福井県 山梨県 長野県 岐阜県 静岡県 愛知県 三重県 滋賀県 京都府 大阪府 兵庫県 奈良県 和歌山県 鳥取県 島根県 岡山県 広島県 山口県 徳島県 香川県 愛媛県 高知県 福岡県 佐賀県 長崎県 熊本県 大分県 宮崎県 鹿児島県 沖縄県 海外".split(" ");
  $("#f-pref").innerHTML = "<option value=''>選択してください</option>" + prefs.map(function (p) { return "<option>" + p + "</option>"; }).join("");

  $$("a[data-job]").forEach(function (a) {
    a.addEventListener("click", function () {
      var v = a.getAttribute("data-job");
      $$("#job-chips input").forEach(function (c) { if (c.value === v) c.checked = true; });
      var r = $("input[name='区分'][value='応募']"); if (r) r.checked = true; syncKind();
    });
  });

  /* 区分によって「経験・実績」の必須を切替 */
  function isApply() { var r = $("input[name='区分']:checked"); return !r || r.value === "応募"; }
  function syncKind() { $$("[data-apply-only]").forEach(function (e) { e.style.display = isApply() ? "" : "none"; }); }
  $$("input[name='区分']").forEach(function (r) { r.addEventListener("change", syncKind); });
  syncKind();

  /* メニュー */
  var mb = $(".menu-btn"), dr = $("#drawer");
  function setMenu(o) { document.body.classList.toggle("menu-open", o); mb.setAttribute("aria-expanded", o); mb.setAttribute("aria-label", o ? "メニューを閉じる" : "メニューを開く"); }
  mb.addEventListener("click", function () { setMenu(!document.body.classList.contains("menu-open")); });
  $$("a", dr).forEach(function (a) { a.addEventListener("click", function () { setMenu(false); }); });

  /* 見出しを1字ずつ分解 */
  $$("[data-split]").forEach(function (el) {
    var i = 0, label = el.textContent;
    (function walk(n) {
      Array.prototype.slice.call(n.childNodes).forEach(function (c) {
        if (c.nodeType === 3) {
          var f = document.createDocumentFragment();
          Array.from(c.textContent).forEach(function (ch) { var s = document.createElement("span"); s.className = "ch"; s.setAttribute("aria-hidden", "true"); s.style.setProperty("--i", i++); s.textContent = ch; f.appendChild(s); });
          c.parentNode.replaceChild(f, c);
        } else if (c.nodeType === 1 && c.tagName !== "BR") walk(c);
      });
    })(el);
    el.setAttribute("aria-label", label);
  });

  /* パララックス */
  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  var par = $$("[data-speed]"), ticking = false;
  function para() {
    ticking = false;
    var mobile = innerWidth < 960;
    par.forEach(function (e) {
      if (mobile && e.closest(".hero-ph")) { e.style.translate = ""; return; }
      var r = e.parentNode.getBoundingClientRect(), sp = parseFloat(e.getAttribute("data-speed"));
      e.style.translate = "0 " + ((r.top + r.height / 2 - innerHeight / 2) * -sp).toFixed(1) + "px";
    });
  }
  if (!reduce) { window.addEventListener("scroll", function () { if (!ticking) { ticking = true; requestAnimationFrame(para); } }, { passive: true }); para(); }
  setTimeout(function () { var c = $(".curtain"); if (c) c.classList.add("gone"); }, 2400);

  /* スクロール表示 */
  var hdr = $(".hdr");
  window.addEventListener("scroll", function () { hdr.classList.toggle("sc", window.scrollY > 40); document.body.classList.toggle("past-hero", window.scrollY > window.innerHeight * 0.8); }, { passive: true });
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } }); }, { rootMargin: "0px 0px -8% 0px" });
    $$(".rv,[data-split]").forEach(function (e) { io.observe(e); });
  } else { $$(".rv,[data-split]").forEach(function (e) { e.classList.add("in"); }); }

  /* ===== フォーム ===== */
  var form = $("#entry-form"), msg = $(".msg", form), btn = $(".submit", form), loadedAt = Date.now();
  function show(t, ng) { msg.textContent = t; msg.className = "msg show" + (ng ? " ng" : ""); msg.scrollIntoView({ block: "center", behavior: "smooth" }); }
  function mark(el, bad) { var w = el.closest(".field"); if (w) w.classList.toggle("bad", bad); return !bad; }

  function validate() {
    var ok = true;
    ok = mark($("#job-chips"), !$$("#job-chips input:checked").length) && ok;
    ["#f-name", "#f-kana", "#f-pref"].forEach(function (s) { ok = mark($(s), !$(s).value.trim()) && ok; });
    var em = $("#f-email").value.trim(); ok = mark($("#f-email"), !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(em)) && ok;
    ok = mark($("#f-career"), isApply() && !$("#f-career").value.trim()) && ok;
    var u = $("#f-url").value.trim(); ok = mark($("#f-url"), !!u && !/^https?:\/\/\S+$/.test(u)) && ok;
    ok = mark($("#f-agree"), !$("#f-agree").checked) && ok;
    return ok;
  }
  form.addEventListener("input", function (e) { var w = e.target.closest(".field"); if (w) w.classList.remove("bad"); });
  form.addEventListener("change", function (e) { var w = e.target.closest(".field"); if (w) w.classList.remove("bad"); });

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    msg.className = "msg";
    if (form.elements["_honey"].value) return;                       // ボット対策（黙って無視）
    if (!validate()) { show("未入力または形式の違う項目があります。赤く表示された項目をご確認ください。", true); return; }
    if ((Date.now() - loadedAt) / 1000 < 4) { show("送信を少しだけお待ちください。もう一度ボタンを押してください。", true); return; }
    try { var last = +localStorage.getItem("ecr_last") || 0; if (Date.now() - last < 60000) { show("続けての送信はご遠慮いただいております。1分ほどおいてお試しください。", true); return; } } catch (x) {}

    var jobs = $$("#job-chips input:checked").map(function (c) { return c.value; }).join("、");
    var kind = isApply() ? "応募" : "質問・相談";
    var name = $("#f-name").value.trim();
    var data = {
      "_subject": "【ecoloco採用サイト】" + kind + "：" + jobs + "（" + name + " 様）",
      "_template": "table",
      "_captcha": "false",
      "区分": kind,
      "希望職種": jobs,
      "お名前": name,
      "ふりがな": $("#f-kana").value.trim(),
      "email": $("#f-email").value.trim(),
      "年齢": $("#f-age").value.trim(),
      "お住まい": $("#f-pref").value,
      "希望の働き方": $("#f-style").value,
      "経験・実績": $("#f-career").value.trim(),
      "やりたいこと・意気込み": $("#f-will").value.trim(),
      "URL": $("#f-url").value.trim(),
      "送信日時": new Date().toLocaleString("ja-JP", { timeZone: "Asia/Tokyo" })
    };
    btn.disabled = true; btn.textContent = "送信中…";
    fetch(ENDPOINT, { method: "POST", headers: { "Content-Type": "application/json", "Accept": "application/json" }, body: JSON.stringify(data) })
      .then(function (r) { return r.json(); })
      .then(function (j) {
        if (!j || String(j.success) !== "true") throw new Error((j && j.message) || "error");
        try { localStorage.setItem("ecr_last", Date.now()); } catch (x) {}
        form.hidden = true; var d = $("#done"); d.hidden = false; d.focus(); d.scrollIntoView({ block: "center", behavior: "smooth" });
      })
      .catch(function () {
        btn.disabled = false; btn.textContent = "この内容で送信する";
        show("申し訳ありません、送信できませんでした。通信環境をご確認のうえ、時間をおいて再度お試しください。", true);
      });
  });
})();
