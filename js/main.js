/* ECOLOCO corporate — 共通スクリプト（素のJS／ビルド不要） */
(function () {
  var CFG = window.ECO_CONFIG || {}, C = window.ECO_CONTENT || {};
  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }

  /* ページ表示フェード */
  requestAnimationFrame(function () { document.body.classList.add("is-in"); });
  window.addEventListener("pageshow", function (e) { if (e.persisted) document.body.classList.add("is-in"); document.body.classList.remove("is-leaving"); });
  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest("a[href]");
    if (!a || reduce || a.target === "_blank" || e.metaKey || e.ctrlKey || e.shiftKey) return;
    var u = new URL(a.href, location.href);
    if (u.origin !== location.origin || u.pathname === location.pathname || /^(mailto|tel):/.test(a.getAttribute("href"))) return;
    e.preventDefault(); document.body.classList.add("is-leaving");
    setTimeout(function () { location.href = a.href; }, 380);
  });

  /* 購入導線：すべて楽天市場ショップへ（URLは config.js と assets/product-links.json で一元管理） */
  var links = null;
  function shopUrl(key) {
    if (links && key && links.brands && links.brands[key]) return links.brands[key].url;
    return CFG.RAKUTEN_SHOP_URL || "https://www.rakuten.co.jp/auc-ecoloco/";
  }
  function applyShopLinks() {
    $$("a[data-shop]").forEach(function (a) {
      a.href = shopUrl(a.getAttribute("data-shop") === "shop" ? "" : a.getAttribute("data-shop"));
      a.target = "_blank"; a.rel = "noopener";
    });
    $$("a[data-yahoo]").forEach(function (a) {
      if (CFG.YAHOO_SHOP_URL) { a.href = CFG.YAHOO_SHOP_URL; a.target = "_blank"; a.rel = "noopener"; a.hidden = false; }
    });
  }

  /* コンテンツ描画（content/content.js） */
  function renderContent() {
    var el;
    if ((el = $("#company-table"))) el.innerHTML = (C.company || []).map(function (r) { return "<tr><th scope='row'>" + esc(r[0]) + "</th><td>" + esc(r[1]) + "</td></tr>"; }).join("");
    if ((el = $("#values"))) el.innerHTML = (C.values || []).map(function (v, i) {
      return "<article class='val rv'><div class='no' aria-hidden='true'>" + v.no + "</div><div><span class='e'>" + esc(v.en) + "</span><h3>" + esc(v.title) + "</h3><p>" + esc(v.body) + "</p></div></article>";
    }).join("");
    if ((el = $("#brands"))) {
      var limit = parseInt(el.getAttribute("data-limit") || "99", 10);
      el.innerHTML = (C.brands || []).slice(0, limit).map(function (b, i) {
        var im = b.img ? "<div class='im'><img src='" + b.img + "' alt='" + esc(b.alt || b.name) + "' loading='lazy' width='800' height='450'></div>"
          : "<div class='im ph-leaf'><span class='bn'>" + esc(b.name) + "</span></div>";
        return "<article class='card rv' style='--d:" + (i % 3) * 0.12 + "s'>" + im + "<div class='bd'><h3>" + esc(b.name) + "</h3><p>" + esc(b.note || "商品の詳細は、楽天市場のショップページでご覧いただけます。") + "</p>" +
          "<a class='btn sm' data-shop='" + esc(b.linkKey) + "' href='#'>楽天市場で見る</a></div></article>";
      }).join("");
    }
    if ((el = $("#jobs"))) el.innerHTML = (C.jobs || []).map(function (j) {
      return "<details class='acc rv' id='job-" + j.id + "'><summary><span>" + esc(j.title) + "</span><span class='st'>" + esc(j.status) + "</span></summary><div class='body'><dl>" +
        "<dt>仕事内容</dt><dd>" + esc(j.work) + "</dd><dt>求める資質</dt><dd>" + esc(j.quality) + "</dd>" +
        "<dt>雇用形態</dt><dd><ul>" + j.type.map(function (t) { return "<li>" + esc(t) + "</li>"; }).join("") + "</ul></dd>" +
        "<dt>勤務時間の目安</dt><dd>" + esc(j.time) + "</dd><dt>給与</dt><dd>勤務条件・経験によります。お問い合わせください。</dd></dl>" +
        "<a class='btn sm apply' href='#apply' data-job='" + esc(j.title) + "'>この職種に応募する</a></div></details>";
    }).join("");
    if ((el = $("select[name=job]"))) el.innerHTML = "<option value=''>選択してください</option>" + (C.jobs || []).map(function (j) { return "<option>" + esc(j.title) + "</option>"; }).join("");
    $$("a[data-job]").forEach(function (a) {
      a.addEventListener("click", function () { var s = $("select[name=job]"); if (s) s.value = a.getAttribute("data-job"); });
    });
    initReveal(); applyShopLinks();
  }

  /* スクロールでふわっと */
  var io = null;
  function initReveal() {
    var els = $$(".rv:not(.in)");
    if (reduce || !("IntersectionObserver" in window)) { els.forEach(function (e) { e.classList.add("in"); }); return; }
    io = io || new IntersectionObserver(function (es) { es.forEach(function (x) { if (x.isIntersecting) { x.target.classList.add("in"); io.unobserve(x.target); } }); }, { threshold: .12, rootMargin: "0px 0px -6% 0px" });
    els.forEach(function (e) { io.observe(e); });
  }

  /* メニュー */
  var mb = $(".menu-btn"), dr = $(".drawer");
  if (mb && dr) {
    mb.addEventListener("click", function () {
      var o = dr.classList.toggle("open"); mb.setAttribute("aria-expanded", o); mb.setAttribute("aria-label", o ? "メニューを閉じる" : "メニューを開く");
      document.body.style.overflow = o ? "hidden" : "";
    });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && dr.classList.contains("open")) mb.click(); });
  }

  /* 花びら（数枚だけ） */
  if (!reduce) for (var i = 0; i < 4; i++) {
    var p = document.createElement("i"); p.className = "petal"; p.setAttribute("aria-hidden", "true");
    p.style.left = (12 + i * 24) + "%"; p.style.animationDelay = (i * 4.5) + "s"; p.style.animationDuration = (15 + i * 2) + "s";
    document.body.appendChild(p);
  }

  /* config.js の値をページに反映 */
  $$("[data-cfg=email]").forEach(function (a) { a.href = "mailto:" + CFG.NOTIFY_EMAIL; a.textContent = a.textContent || CFG.NOTIFY_EMAIL; });

  /* product-links.json を読み込んでから描画（file:// では読めないためショップTOPにフォールバック） */
  renderContent();
  if (window.fetch) fetch((document.documentElement.getAttribute("data-root") || "") + "assets/product-links.json").then(function (r) { return r.json(); })
    .then(function (j) { links = j; applyShopLinks(); }).catch(function () {});
})();
