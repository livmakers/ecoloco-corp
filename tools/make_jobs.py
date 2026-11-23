#!/usr/bin/env python3
"""採用サイトの求人詳細ページ（1職種1ページ）と JobPosting 構造化データを生成する。

元データは recruit/app.js の JOBS 配列。職種を直したら app.js を直してから
  python3 tools/make_jobs.py
を実行すると recruit/jobs/*.html と sitemap.xml の求人URLが更新される。
Googleのしごと検索は「1ページ1求人」の詳細ページを推奨しているため、
一覧ページ（recruit/index.html）には JobPosting を置かない。
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REC = ROOT / "recruit"
BASE = "https://ysfree.co.jp"
DATE_POSTED = "2026-11-21"
VALID_THROUGH = "2027-05-31T23:59:59+09:00"
ADDRESS = {
    "@type": "PostalAddress",
    "postalCode": "541-0056",
    "addressRegion": "大阪府",
    "addressLocality": "大阪市中央区",
    "streetAddress": "久太郎町3丁目5番5号 丸忠第一ビル5F",
    "addressCountry": "JP",
}
ORG = {
    "@type": "Organization",
    "name": "株式会社ワイズフリー",
    "alternateName": "ecoloco（エコロコ）",
    "sameAs": ["https://www.rakuten.co.jp/auc-ecoloco/", "https://store.shopping.yahoo.co.jp/ecoloco/", "https://www.instagram.com/ecoloco.official/"],
    "url": "https://ysfree.co.jp/",
    "logo": "https://ysfree.co.jp/assets/img/logo.png",
}
HOURS = "9:30〜18:30の間（職種・雇用形態により異なります）"
PAY = "月給26万円〜（ご経験・能力により決定）。雇用形態はご希望の働き方をふまえ、面接でご相談のうえ決定します。"


def load_jobs():
    src = (REC / "app.js").read_text(encoding="utf-8")
    block = re.search(r"var JOBS = \[(.*?)\n  \];", src, re.S).group(1)
    jobs = []
    for m in re.finditer(r"\{ id: (.*?)\] \}", block, re.S):
        obj = "{ id: " + m.group(1) + "] }"
        obj = re.sub(r"(\{|,)\s*([a-z]+):", r'\1 "\2":', obj)
        jobs.append(json.loads(obj))
    assert len(jobs) >= 1, "JOBS が読めません"
    return jobs


def e(s):
    return html.escape(s, quote=True)


def ul(items):
    return "<ul>" + "".join(f"<li>{e(x)}</li>" for x in items) + "</ul>"


def posting(j):
    title = j["title"] + ("（未経験歓迎）" if j["tag"] == "未経験OK" else "（経験者）")
    desc = (
        f"<p>{e(j['catch'])}</p>"
        f"<p><b>仕事内容</b></p>{ul(j['work'])}"
        f"<p><b>必須</b></p>{ul(j['must'])}"
        f"<p><b>歓迎</b></p>{ul(j['want'])}"
        "<p><b>雇用形態</b></p><p>正社員・契約社員・アルバイト・業務委託から、ご経験とご希望に応じて決定します。</p>"
        f"<p><b>給与</b></p><p>{PAY}</p>"
        f"<p><b>就業時間</b></p><p>{HOURS}</p>"
        "<p><b>応募方法</b></p><p>採用サイトの応募フォームから（お電話での受付は行っていません）</p>"
    )
    data = {
        "@context": "https://schema.org",
        "@type": "JobPosting",
        "title": title,
        "description": desc,
        "identifier": {"@type": "PropertyValue", "name": "株式会社ワイズフリー", "value": "ysf-" + j["id"]},
        "datePosted": DATE_POSTED,
        "validThrough": VALID_THROUGH,
        "employmentType": ["FULL_TIME", "PART_TIME", "CONTRACTOR"],
        "hiringOrganization": ORG,
        "jobLocation": {"@type": "Place", "address": ADDRESS},
        "url": f"{BASE}/recruit/jobs/{j['id']}.html",
        "directApply": True,
        "industry": "アパレルEC",
        "baseSalary": {"@type": "MonetaryAmount", "currency": "JPY",
                       "value": {"@type": "QuantitativeValue", "minValue": 260000, "unitText": "MONTH"}},
        "occupationalCategory": j["title"],
    }
    if j["tag"] == "未経験OK":
        data["experienceRequirements"] = "no requirements"
    # "</" をHTML内で閉じタグにしないようにエスケープ
    return title, json.dumps(data, ensure_ascii=False).replace("<", "\\u003c")


PAGE = """<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}｜ecoloco 採用サイト｜株式会社ワイズフリー</title>
<meta name="description" content="{metadesc}">
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self'; style-src 'self' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; img-src 'self' data:; base-uri 'self'; form-action 'self'; object-src 'none'">
<meta name="referrer" content="strict-origin-when-cross-origin">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="format-detection" content="telephone=no">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="ecoloco 採用サイト（株式会社ワイズフリー）">
<meta property="og:title" content="{title}｜ecoloco 採用">
<meta property="og:description" content="{catch}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{image}">
<meta name="twitter:card" content="summary_large_image">
<meta property="og:locale" content="ja_JP">
<script type="application/ld+json">{ld}</script>
<script type="application/ld+json">{crumbs}</script>
<link rel="icon" href="../../assets/img/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;1,400;1,500&family=Shippori+Mincho:wght@500;700;800&family=Zen+Kaku+Gothic+New:wght@400;500;700;900&display=swap">
<link rel="stylesheet" href="../style.css">
<link rel="stylesheet" href="../fx.css">
<link rel="stylesheet" href="jobs.css">
</head>
<body class="jobpage past-hero">
<a class="skip" href="#main">本文へスキップ</a>
<header class="hdr sc" id="top"><div class="in">
  <a class="logo" href="../" aria-label="ecoloco 採用サイト TOPへ"><img src="../../assets/img/logo.png" alt="ecoloco" width="123" height="40"><span>RECRUIT</span></a>
  <nav class="nav" aria-label="メニュー"><a href="../#positions">募集職種一覧</a><a href="../#conditions">募集要項</a><a href="../#flow">選考の流れ</a><a href="../#faq">FAQ</a></nav>
  <a class="btn sm fill" href="{apply}">応募する</a>
</div></header>

<main id="main">
<nav class="crumb wrap" aria-label="パンくずリスト"><a href="../">採用サイトTOP</a><span>›</span><a href="../#positions">募集職種</a><span>›</span><span aria-current="page">{short}</span></nav>

<section class="jhero wrap">
  <div class="jhero-tx">
    <p class="en">{no} / {en}</p>
    <p class="jlabel">求人情報<em class="{tagcls}">{tag}</em></p>
    <h1>{short}</h1>
    <p class="jcatch">{catch}</p>
    <a class="btn fill" href="{apply}">この職種に応募する</a>
  </div>
  <figure class="jhero-ph"><img src="../{img}" alt="ecolocoの商品イメージ" width="720" height="900"></figure>
</section>

<section class="sec jdetail"><span class="wm" aria-hidden="true">{en_wm}</span>
  <div class="wrap narrow">
    <h2 class="c">募集内容</h2>
    <table class="terms">
      <tr><th scope="row">職種</th><td>{short}</td></tr>
      <tr><th scope="row">仕事内容</th><td>{work}<small>（変更の範囲：会社の定める業務）</small></td></tr>
      <tr><th scope="row">応募資格（必須）</th><td>{must}</td></tr>
      <tr><th scope="row">歓迎</th><td>{want}</td></tr>
      <tr><th scope="row">雇用形態・契約期間</th><td>正社員・契約社員・アルバイト・業務委託から、ご経験とご希望に応じて決定します。契約期間・更新の有無は、雇用形態に応じて内定前に書面でお知らせします。</td></tr>
      <tr><th scope="row">給与</th><td>{pay}</td></tr>
      <tr><th scope="row">就業場所</th><td>大阪府大阪市中央区久太郎町3丁目5番5号 丸忠第一ビル5F<br><small>（変更の範囲：会社の定める場所）</small></td></tr>
      <tr><th scope="row">就業時間</th><td>{hours}</td></tr>
      <tr><th scope="row">試用期間・休憩・休日・時間外労働・社会保険・受動喫煙対策</th><td>職種・雇用形態により異なるため、面接時にご説明し、内定前に労働条件通知書（書面）で明示します。</td></tr>
      <tr><th scope="row">募集者</th><td>株式会社ワイズフリー（ecoloco）</td></tr>
      <tr><th scope="row">応募方法</th><td>採用サイトの <a href="{apply}">応募フォーム</a> から（お電話での受付は行っていません）</td></tr>
    </table>
    <div class="jcta">
      <a class="btn fill" href="{apply}">この職種に応募する</a>
      <a class="btn" href="../#positions">ほかの職種を見る</a>
    </div>
  </div>
</section>

<section class="sec jothers">
  <div class="wrap">
    <p class="en c">OTHER POSITIONS</p>
    <h2 class="c">ほかの募集職種</h2>
    <ul class="jlist">{others}</ul>
  </div>
</section>
</main>

<footer class="ftr"><div class="wrap">
  <div class="big" aria-hidden="true">ecoloco</div>
  <div class="ftr-g">
    <p>株式会社ワイズフリー（ecoloco）<br>〒541-0056 大阪府大阪市中央区久太郎町3丁目5番5号 丸忠第一ビル5F<br>採用に関するお問い合わせは <a href="../#entry">応募・お問い合わせフォーム</a> から</p>
    <ul>
      <li><a href="../">採用サイトTOP</a></li>
      <li><a href="../../">コーポレートサイト</a></li>
      <li><a href="https://www.rakuten.co.jp/auc-ecoloco/" target="_blank" rel="noopener">ONLINE SHOP（楽天市場）</a></li>
      <li><a href="https://www.instagram.com/ecoloco.official/" target="_blank" rel="noopener">Instagram @ecoloco.official</a></li>
      <li><a href="../../privacy.html">プライバシーポリシー</a></li>
    </ul>
  </div>
  <p class="cp">© ecoloco / 株式会社ワイズフリー</p>
</div></footer>
<a class="float-cta" href="{apply}">応募する</a>
</body>
</html>
"""


def main():
    jobs = load_jobs()
    out = REC / "jobs"
    out.mkdir(exist_ok=True)
    urls = []
    for i, j in enumerate(jobs):
        title, ld = posting(j)
        url = f"{BASE}/recruit/jobs/{j['id']}.html"
        urls.append(url)
        crumbs = json.dumps({
            "@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "ecoloco 採用サイト", "item": BASE + "/recruit/"},
                {"@type": "ListItem", "position": 2, "name": j["title"], "item": url},
            ]}, ensure_ascii=False)
        others = "".join(
            f"<li><a href=\"{o['id']}.html\"><span class=\"en\">{e(o['en'])}</span>{e(o['title'])}<em class=\"{'ok' if o['tag']=='未経験OK' else ''}\">{e(o['tag'])}</em></a></li>"
            for o in jobs if o["id"] != j["id"])
        page = PAGE.format(
            title=e(title), short=e(j["title"]), catch=e(j["catch"]), en=e(j["en"]),
            en_wm=e(j["en"].split(" ")[0].split("/")[0].title()),
            no=f"0{i+1}", tag=e(j["tag"]), tagcls="ok" if j["tag"] == "未経験OK" else "",
            metadesc=e(f"【{j['title']}】{j['catch']} 大阪市中央区・株式会社ワイズフリー（ecoloco）の求人。仕事内容・応募資格・募集要項はこちら。"),
            url=url, image=BASE + "/" + j["img"].replace("../", ""), img=e(j["img"]),
            apply=f"../?job={j['id']}#entry", ld=ld, crumbs=crumbs,
            work=ul(j["work"]), must=ul(j["must"]), want=ul(j["want"]),
            pay=PAY, hours=HOURS, others=others)
        (out / f"{j['id']}.html").write_text(page, encoding="utf-8")

    # 一覧ページから JobPosting を外し、詳細ページへの ItemList に置き換える
    idx = REC / "index.html"
    s = idx.read_text(encoding="utf-8")
    m = re.search(r'<script type="application/ld\+json">(.*?)</script>', s, re.S)
    data = json.loads(m.group(1))
    graph = [g for g in data["@graph"] if g.get("@type") not in ("JobPosting", "ItemList")]
    graph.insert(2, {"@type": "ItemList", "name": "募集職種",
                     "itemListElement": [{"@type": "ListItem", "position": k + 1, "url": u} for k, u in enumerate(urls)]})
    data["@graph"] = graph
    new = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")
    s = s[:m.start(1)] + new + s[m.end(1):]
    idx.write_text(s, encoding="utf-8")

    # sitemap に求人ページを追加
    sm = ROOT / "sitemap.xml"
    t = sm.read_text(encoding="utf-8")
    t = re.sub(r"  <url><loc>https://ysfree\.co\.jp/recruit/jobs/[^<]*</loc>[^\n]*\n", "", t)
    add = "".join(f"  <url><loc>{u}</loc><lastmod>2026-11-24</lastmod></url>\n" for u in urls)
    t = t.replace("</urlset>", add + "</urlset>")
    sm.write_text(t, encoding="utf-8")
    print("generated", len(urls), "job pages")


if __name__ == "__main__":
    main()
