# -*- coding: utf-8 -*-
"""自己検証：スクリーンショット／コンソールエラー／モバイル横スクロール／alt／内部リンク／フォーム送信テスト
   前提: ecoloco-corp で `python -m http.server 8765` を起動済み。 実行: python tools/verify.py"""
import os, re, json, sys, urllib.request
from playwright.sync_api import sync_playwright
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = "http://localhost:8765/"
PAGES = ["index", "about", "work-style", "original-brand", "recruit", "contact", "privacy", "thanks"]
out = os.path.join(R, "docs", "screens"); os.makedirs(out, exist_ok=True)
report = []
def log(s): print(s); report.append(s)

with sync_playwright() as p:
    br = p.chromium.launch()
    for dev, vp in (("pc", {"width": 1440, "height": 900}), ("sp", {"width": 390, "height": 844})):
        ctx = br.new_context(viewport=vp, reduced_motion="reduce", device_scale_factor=1, is_mobile=(dev == "sp"), has_touch=(dev == "sp"))
        for name in PAGES:
            pg = ctx.new_page(); errs = []
            pg.on("console", lambda m, e=errs: e.append(m.text) if m.type == "error" else None)
            pg.on("pageerror", lambda x, e=errs: e.append(str(x)))
            pg.on("requestfailed", lambda r, e=errs: e.append("REQFAIL " + r.url))
            pg.goto(B + name + ".html", wait_until="networkidle"); pg.wait_for_timeout(500)
            ov = pg.evaluate("document.documentElement.scrollWidth - window.innerWidth")
            noalt = pg.evaluate("[...document.images].filter(i=>!i.hasAttribute('alt')).length")
            small = pg.evaluate("[...document.querySelectorAll('a,button,input,select,textarea')].filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&r.height>0&&(r.height<44)&&!e.closest('.hp')&&e.type!=='checkbox'&&e.type!=='radio'&&getComputedStyle(e).display!=='none'&&!e.classList.contains('skip')}).map(e=>(e.textContent||e.name||'').trim().slice(0,20)+':'+Math.round(e.getBoundingClientRect().height))")
            log(f"[{dev}] {name}: 横はみ出し={ov}px alt無し={noalt} 高さ<44pxの操作要素={small} エラー={len(errs)}")
            for e in errs: log("   ! " + e[:160])
            pg.screenshot(path=os.path.join(out, f"{dev}-{name}.png"), full_page=True)
            pg.close()
        ctx.close()

    # フォーム送信テスト（GAS通信はモック）
    ctx = br.new_context(viewport={"width": 390, "height": 844}); pg = ctx.new_page()
    posted = []
    def fake(route):
        posted.append(json.loads(route.request.post_data)); route.fulfill(status=200, content_type="application/json", body='{"ok":true}',
            headers={"access-control-allow-origin": "*"})
    pg.route("https://script.google.com/**", fake)
    for kind, url in (("contact", "contact.html"), ("recruit", "recruit.html")):
        pg.goto(B + url, wait_until="networkidle")
        pg.evaluate("localStorage.clear(); window.ECO_CONFIG.GAS_ENDPOINT='https://script.google.com/macros/s/TEST/exec'")
        # 1) 空送信 → エラー表示
        pg.wait_for_timeout(4500); pg.click("button[type=submit]")
        log(f"[form:{kind}] 空送信→エラー表示: " + str(pg.evaluate("document.querySelectorAll('.field.bad').length") > 0))
        # 2) 入力 → 送信
        pg.fill("[name=name]", "テスト 太郎"); pg.fill("[name=email]", "test@example.com")
        if kind == "contact":
            pg.select_option("[name=type]", index=1); pg.fill("[name=body]", "テスト送信です")
        else:
            pg.fill("[name=kana]", "てすと たろう"); pg.fill("[name=tel]", "0600000000"); pg.select_option("[name=job]", index=1)
            pg.select_option("[name=employment]", index=1); pg.select_option("[name=prefecture]", label="大阪府"); pg.fill("[name=pr]", "テスト")
        pg.check("[name=agree]"); pg.click("button[type=submit]")
        pg.wait_for_url("**/thanks.html*", timeout=5000)
        log(f"[form:{kind}] 送信→サンクスページ遷移: {pg.url}  / GASへのPOST内容キー: {sorted(posted[-1].keys())}")
        # 3) 連続送信制限
        pg.goto(B + url, wait_until="networkidle"); pg.evaluate("window.ECO_CONFIG.GAS_ENDPOINT='https://script.google.com/macros/s/TEST/exec'")
        pg.fill("[name=name]", "a"); pg.fill("[name=email]", "a@example.com")
        if kind == "contact": pg.select_option("[name=type]", index=1); pg.fill("[name=body]", "x")
        else:
            pg.fill("[name=kana]", "a"); pg.fill("[name=tel]", "1"); pg.select_option("[name=job]", index=1); pg.select_option("[name=employment]", index=1); pg.select_option("[name=prefecture]", index=1)
        pg.check("[name=agree]"); pg.wait_for_timeout(4500); pg.click("button[type=submit]"); pg.wait_for_timeout(300)
        log(f"[form:{kind}] 連続送信制限メッセージ: {pg.inner_text('.msg')[:30]}")
        # 4) ハニーポット
        n = len(posted); pg.evaluate("localStorage.clear()"); pg.evaluate("document.querySelector('[name=website]').value='spam'"); pg.click("button[type=submit]"); pg.wait_for_timeout(400)
        log(f"[form:{kind}] ハニーポット入力時は送信されない: {len(posted) == n}")
    # 5) 送信失敗時のやさしい文言
    pg.route("https://script.google.com/**", lambda r: r.abort())
    pg.goto(B + "contact.html", wait_until="networkidle"); pg.evaluate("localStorage.clear(); window.ECO_CONFIG.GAS_ENDPOINT='https://script.google.com/macros/s/TEST/exec'")
    pg.fill("[name=name]", "a"); pg.fill("[name=email]", "a@example.com"); pg.select_option("[name=type]", index=1); pg.fill("[name=body]", "x"); pg.check("[name=agree]")
    pg.wait_for_timeout(4500); pg.click("button[type=submit]"); pg.wait_for_timeout(800)
    log("[form:error] 通信失敗時の文言: " + pg.inner_text(".msg")[:60])
    ctx.close(); br.close()

# 内部リンク／アセット
bad = []
for f in os.listdir(R):
    if f.endswith(".html"):
        s = open(os.path.join(R, f), encoding="utf-8").read()
        for h in re.findall(r'(?:href|src)="([^"#?]+)', s):
            if re.match(r"(https?:|mailto:|tel:|data:|//)", h): continue
            if not os.path.exists(os.path.join(R, h)): bad.append((f, h))
log("内部リンク/アセット切れ: " + (str(bad) if bad else "なし"))
# 外部リンクの到達性
ext = set()
for f in os.listdir(R):
    if f.endswith(".html"):
        ext |= set(re.findall(r'href="(https?://[^"]+)"', open(os.path.join(R, f), encoding="utf-8").read()))
ext |= set(u["url"] for u in json.load(open(os.path.join(R, "assets/product-links.json"), encoding="utf-8"))["brands"].values())
for u in sorted(ext):
    if "fonts.g" in u or "google.com/maps" in u: continue
    try:
        r = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"}), timeout=20); log(f"外部 {r.status} {u}")
    except Exception as e: log(f"外部 NG({e}) {u}")
open(os.path.join(R, "docs", "verify-log.txt"), "w", encoding="utf-8").write("\n".join(report))
