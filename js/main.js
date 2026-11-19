/* ECOLOCO corporate — 共通スクリプト（素のJS／ビルド不要） */
(function () {
  var CFG = window.ECO_CONFIG || {}, C = window.ECO_CONTENT || {};
  var html = document.documentElement;
  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }

  /* イントロ（初回のみ）→ 幕が上がってヒーロー文字が現れる */
  function startHero() { $$("[data-hero]").forEach(function (e) { e.classList.add("ch-on", "in"); }); }
  if (html.classList.contains("intro") && !reduce) {
    setTimeout(function () { html.classList.add("intro-out"); }, 900);
    setTimeout(function () { startHero(); }, 1500);
    setTimeout(function () { html.classList.remove("intro", "intro-out"); try { sessionStorage.eco_i = 1; } catch (e) {} }, 2600);
  } else { html.classList.remove("intro"); setTimeout(startHero, 80); }

  /* ページ遷移（緑の幕） */
  window.addEventListener("pageshow", function (e) { document.body.classList.remove("is-leaving"); });
  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest("a[href]");
    if (!a || reduce || a.target === "_blank" || e.metaKey || e.ctrlKey || e.shiftKey) return;
    var u = new URL(a.href, location.href);
    if (u.origin !== location.origin || /^(mailto|tel):/.test(a.getAttribute("href"))) return;
    if (u.pathname === location.pathname) return;
    e.preventDefault(); document.body.classList.add("is-leaving");
    setTimeout(function () { location.href = a.href; }, 700);
  });

  /* 購入導線：すべて楽天市場ショップへ */
  var links = null;
  function shopUrl(key) {
    if (links && key && links.brands && links.brands[key]) return links.brands[key].url;
    return CFG.RAKUTEN_SHOP_URL || "https://www.rakuten.co.jp/auc-ecoloco/";
  }
  function applyShopLinks() {
    $$("a[data-shop]").forEach(function (a) {
      var k = a.getAttribute("data-shop"); a.href = shopUrl(k === "shop" ? "" : k); a.target = "_blank"; a.rel = "noopener";
    });
    $$("a[data-yahoo]").forEach(function (a) { if (CFG.YAHOO_SHOP_URL) { a.href = CFG.YAHOO_SHOP_URL; a.target = "_blank"; a.rel = "noopener"; a.hidden = false; } });
  }

  /* コンテンツ描画 */
  function renderContent() {
    var el;
    if ((el = $("#company-table"))) el.innerHTML = (C.company || []).map(function (r) { return "<tr><th scope='row'>" + esc(r[0]) + "</th><td>" + esc(r[1]) + "</td></tr>"; }).join("");
    if ((el = $("#values"))) el.innerHTML = (C.values || []).map(function (v, i) {
      return "<article class='val'><div class='no rv' aria-hidden='true'>" + v.no + "</div><div class='rv' style='--d:.1s'><span class='e'>" + esc(v.en) + "</span><h3 data-split>" + esc(v.title) + "</h3><p>" + esc(v.body) + "</p></div>" +
        "<div class='ph ir zm' style='--d:.2s'><img src='" + v.img + "' alt='" + esc(v.alt) + "' loading='lazy' width='700' height='840'></div></article>";
    }).join("");
    if ((el = $("#brands"))) {
      var limit = parseInt(el.getAttribute("data-limit") || "99", 10);
      el.innerHTML = (C.brands || []).slice(0, limit).map(function (b, i) {
        var im = b.img ? "<div class='im" + (b.fit ? " fit" : "") + "'><img src='" + b.img + "' alt='" + esc(b.alt || b.name) + "' loading='lazy' width='600' height='800'></div>"
          : "<div class='im t'><span class='bn'>" + esc(b.name) + "</span></div>";
        return "<a class='bc rv" + (i % 2 ? " alt" : "") + "' style='--d:" + (i % 4) * 0.1 + "s' data-shop='" + esc(b.linkKey) + "' href='#'>" + im +
          "<span class='no'>" + ("0" + (i + 1)).slice(-2) + "</span><h3>" + esc(b.name) + "</h3><p>" + esc(b.note || "商品の詳細は、楽天市場のショップページでご覧いただけます。") + "</p><span class='go'>楽天市場で見る</span></a>";
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
    $$("a[data-job]").forEach(function (a) { a.addEventListener("click", function () { var s = $("select[name=job]"); if (s) s.value = a.getAttribute("data-job"); }); });
    splitText(); initReveal(); applyShopLinks(); initDrag();
  }

  /* 文字を1字ずつ浮かせる */
  function splitText() {
    $$("[data-split]:not([data-done])").forEach(function (el) {
      el.setAttribute("data-done", 1); var i = 0;
      (function walk(n) {
        Array.prototype.slice.call(n.childNodes).forEach(function (c) {
          if (c.nodeType === 3) {
            var f = document.createDocumentFragment();
            c.textContent.split("").forEach(function (ch) {
              if (ch === " " || ch === "\n") { f.appendChild(document.createTextNode(ch)); return; }
              var s = document.createElement("span"); s.className = "ch"; s.style.setProperty("--i", i++); s.textContent = ch; s.setAttribute("aria-hidden", "true"); f.appendChild(s);
            });
            n.replaceChild(f, c);
          } else if (c.nodeType === 1 && c.tagName !== "BR") walk(c);
        });
      })(el);
      el.setAttribute("aria-label", el.textContent.replace(/\s+/g, " ").trim());
      if (el.hasAttribute("data-hero")) { /* 後でstartHero */ } else el.classList.add("rv-split");
    });
  }

  /* スクロールでふわっと */
  var io = null;
  function initReveal() {
    var els = $$(".rv:not(.in),.ir:not(.in),.rv-split:not(.in)");
    if (reduce || !("IntersectionObserver" in window)) { els.forEach(function (e) { e.classList.add("in"); }); return; }
    io = io || new IntersectionObserver(function (es) { es.forEach(function (x) { if (x.isIntersecting) { x.target.classList.add("in"); io.unobserve(x.target); } }); }, { threshold: .15, rootMargin: "0px 0px -6% 0px" });
    els.forEach(function (e) { io.observe(e); });
  }

  /* ヘッダー・メニュー */
  var hdr = $(".hdr");
  function onScroll() { if (hdr) hdr.classList.toggle("is-scrolled", window.scrollY > 40); }
  var mb = $(".menu-btn"), dr = $(".drawer");
  if (mb && dr) {
    mb.addEventListener("click", function () {
      var o = dr.classList.toggle("open"); mb.setAttribute("aria-expanded", o); mb.setAttribute("aria-label", o ? "メニューを閉じる" : "メニューを開く");
      document.body.style.overflow = o ? "hidden" : "";
    });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && dr.classList.contains("open")) mb.click(); });
  }

  /* パララックス（写真・透かしがゆっくり別速度で動く） */
  var px = [];
  function collectPx() { px = $$("[data-speed]"); }
  var ticking = false;
  function parallax() {
    ticking = false; onScroll();
    if (reduce) return;
    var vh = window.innerHeight;
    px.forEach(function (el) {
      var r = el.getBoundingClientRect(); if (r.bottom < -200 || r.top > vh + 200) return;
      var d = (r.top + r.height / 2 - vh / 2) * parseFloat(el.getAttribute("data-speed"));
      el.style.transform = "translate3d(0," + d.toFixed(1) + "px,0)";
    });
  }
  window.addEventListener("scroll", function () { if (!ticking) { ticking = true; requestAnimationFrame(parallax); } }, { passive: true });
  window.addEventListener("resize", parallax);

  /* 横スクロールのドラッグ */
  function initDrag() {
    $$(".hs").forEach(function (h) {
      if (h.getAttribute("data-d")) return; h.setAttribute("data-d", 1);
      var down = false, sx = 0, sl = 0, moved = false;
      h.addEventListener("mousedown", function (e) { down = true; moved = false; sx = e.pageX; sl = h.scrollLeft; });
      window.addEventListener("mouseup", function () { down = false; h.classList.remove("drag"); });
      h.addEventListener("mousemove", function (e) { if (!down) return; var dx = e.pageX - sx; if (Math.abs(dx) > 4) { moved = true; h.classList.add("drag"); } h.scrollLeft = sl - dx; });
      h.addEventListener("click", function (e) { if (moved) { e.preventDefault(); e.stopPropagation(); moved = false; } }, true);
    });
  }

  /* 花びら（数枚だけ） */
  if (!reduce) for (var i = 0; i < 5; i++) {
    var p = document.createElement("i"); p.className = "petal"; p.setAttribute("aria-hidden", "true");
    p.style.left = (8 + i * 21) + "%"; p.style.background = ["#ef9fa5","#e2a93b","#c4162a","#6f9bb5","#e8c9c0"][i]; p.style.animationDelay = (i * 4) + "s"; p.style.animationDuration = (15 + i * 2) + "s"; document.body.appendChild(p);
  }

  $$("[data-cfg=email]").forEach(function (a) { a.href = "mailto:" + CFG.NOTIFY_EMAIL; });

  splitText(); renderContent(); collectPx(); parallax();
  if (window.fetch) fetch((html.getAttribute("data-root") || "") + "assets/product-links.json").then(function (r) { return r.json(); }).then(function (j) { links = j; applyShopLinks(); }).catch(function () {});
})();
