# -*- coding: utf-8 -*-
"""HTML生成（共通ヘッダー/フッターを各ページに焼き込む）。実行: python tools/build.py
公開に必要なのは生成後の静的ファイルのみ。文言の差し替えは content/content.js を直接編集すればOK。"""
import os, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://livmakers.github.io/ecoloco-corp"  # 【要確認】独自ドメインにする場合は置換（sitemap/OGP/canonical）
FONTS = "https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;1,300;1,400;1,500&family=Klee+One&family=Shippori+Mincho:wght@400;500;700&family=Zen+Maru+Gothic:wght@400;500;700&display=swap"
NAV = [("index.html", "TOP"), ("about.html", "ABOUT US"), ("work-style.html", "WORK STYLE"), ("recruit.html", "RECRUIT"), ("original-brand.html", "ORIGINAL BRAND"), ("contact.html", "CONTACT")]

def head(file, title, desc, extra="", noindex=False):
    url = f"{SITE}/{'' if file == 'index.html' else file}"
    intro = '<script>try{if(!sessionStorage.eco_i)document.documentElement.classList.add("intro")}catch(e){}</script>' if file == "index.html" else ""
    return f"""<!doctype html>
<html lang="ja" data-root="">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
{'<meta name="robots" content="noindex">' if noindex else ''}
<link rel="canonical" href="{url}">
<meta property="og:type" content="website"><meta property="og:site_name" content="ECOLOCO（株式会社ワイズフリー）">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}"><meta property="og:image" content="{SITE}/assets/img/ogp.jpg"><meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#FBF8F3">
<link rel="icon" href="assets/img/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="css/style.css">
{intro}
{extra}
</head>
"""

def header(cur):
    nav = "".join(f'<a href="{h}"{" aria-current=page" if h == cur else ""}>{t}</a>' for h, t in NAV)
    dr = "".join(f'<a class="l" href="{h}">{t}</a>' for h, t in NAV)
    return f"""<body>
<a class="skip" href="#main">本文へスキップ</a>
<div class="curtain" aria-hidden="true"><span class="cw">ecoloco</span></div>
<header class="hdr"><div class="in">
  <a class="logo" href="index.html" aria-label="ecoloco エコロコ TOPへ"><img src="assets/img/logo.png" alt="ecoloco エコロコ" width="123" height="40"></a>
  <nav class="nav" aria-label="メインメニュー">{nav}</nav>
  <div class="hdr-r">
    <a class="btn sm fill" data-shop="shop" href="https://www.rakuten.co.jp/auc-ecoloco/" target="_blank" rel="noopener">ONLINE SHOP（楽天市場）</a>
    <button class="menu-btn" aria-expanded="false" aria-controls="drawer" aria-label="メニューを開く"><span></span></button>
  </div>
</div></header>
<div class="drawer" id="drawer">{dr}
  <a class="btn fill" data-shop="shop" href="https://www.rakuten.co.jp/auc-ecoloco/" target="_blank" rel="noopener">ONLINE SHOP（楽天市場）</a>
  <span class="shop-note" style="text-align:center">楽天市場のショップページへ移動します</span>
</div>
<main id="main">
"""

FOOTER = """</main>
<footer class="ftr"><div class="wrap">
  <div class="big" aria-hidden="true">ecoloco</div>
  <div class="g">
  <div><p style="font-size:13px;margin:0 0 18px">株式会社ワイズフリー<br>〒541-0056 大阪府大阪市中央区久太郎町3丁目5番5号 丸忠第一ビル5F<br>TEL 06-6281-0800（平日 10:00〜13:00）</p>
  <a class="btn" data-shop="shop" href="https://www.rakuten.co.jp/auc-ecoloco/" target="_blank" rel="noopener">ONLINE SHOP（楽天市場）</a>
  <span class="shop-note" style="color:#b8ad9d">楽天市場のショップページへ移動します</span>
  <a class="btn sm" data-yahoo href="#" hidden style="margin-top:10px">Yahoo!ショッピング</a></div>
  <div><h4>Menu</h4><ul><li><a href="index.html">TOP</a></li><li><a href="about.html">ABOUT US</a></li><li><a href="work-style.html">WORK STYLE</a></li><li><a href="recruit.html">RECRUIT</a></li><li><a href="original-brand.html">ORIGINAL BRAND</a></li></ul></div>
  <div><h4>Info</h4><ul><li><a href="contact.html">お問い合わせ</a></li><li><a href="privacy.html">プライバシーポリシー</a></li></ul></div>
</div><div class="cp">© ECOLOCO / 株式会社ワイズフリー</div></div></footer>
<script src="config.js"></script>
<script src="content/content.js"></script>
<script src="js/main.js"></script>
%s
</body></html>
"""

def sec_head(en, ja, c=False):
    return f'<div class="head{" c" if c else ""}"><span class="en rv">{en}</span><h2 data-split>{ja}</h2></div>'

# 下層ページの見出し：大きな欧文＋透かし写真（楽天ショップの画像）
GHOST = {
    "ABOUT US": ("assets/img/contents-260918-2.webp", "right:-8%;top:-10%;width:62%;height:120%"),
    "WORK STYLE": ("assets/img/sj7.webp", "right:-4%;top:-20%;width:44%;height:150%"),
    "ORIGINAL BRAND": ("assets/img/m12.webp", "right:-6%;top:-10%;width:48%;height:130%"),
    "RECRUIT": ("assets/img/m16.webp", "right:-6%;top:-10%;width:50%;height:130%"),
    "CONTACT": ("assets/img/m13.webp", "right:-6%;top:-10%;width:46%;height:130%"),
    "PRIVACY POLICY": ("assets/img/m14.webp", "right:-6%;top:-10%;width:46%;height:130%"),
}
def page_hero(en, ja):
    g = GHOST.get(en)
    gh = f'<div class="ghost" aria-hidden="true"><img src="{g[0]}" alt="" style="{g[1]}" data-speed=".05"></div>' if g else ""
    return f'<section class="ph-hero">{gh}<i class="wm tr" aria-hidden="true"></i><div class="wrap"><div class="big" data-hero data-split>{en}</div><h1 class="rv">{ja}</h1></div></section>'

def write(file, html):
    with open(os.path.join(ROOT, file), "w", encoding="utf-8", newline="\n") as f:
        f.write(html)

ORG = {"@context": "https://schema.org", "@type": "Organization", "name": "株式会社ワイズフリー", "alternateName": "ecoloco",
       "url": SITE + "/", "telephone": "+81-6-6281-0800", "email": "ecoloco-yahoo@ysfree.jp",
       "address": {"@type": "PostalAddress", "postalCode": "541-0056", "addressRegion": "大阪府", "addressLocality": "大阪市中央区", "streetAddress": "久太郎町3丁目5番5号 丸忠第一ビル5F", "addressCountry": "JP"}}
ORG_LD = '<script type="application/ld+json">' + json.dumps(ORG, ensure_ascii=False) + "</script>"

SHOP_BTN = '<a class="btn fill {cls}" data-shop="shop" href="https://www.rakuten.co.jp/auc-ecoloco/" target="_blank" rel="noopener">ONLINE SHOP（楽天市場）</a>'


# ---------------- TOP ----------------
MARQ = ('<span>ecoloco<em>/</em>natural clothes for grown-ups<em>/</em>linen &amp; cotton<em>/</em>着心地がいい。ちょうどいい。<em>/</em></span>') * 2
top = head("index.html", "ecoloco（エコロコ）｜株式会社ワイズフリー 公式コーポレートサイト",
           "大人のための、天然素材ナチュラル服 ecoloco（エコロコ）を運営する株式会社ワイズフリーのコーポレートサイト。会社概要・働き方・採用情報・オリジナルブランドをご紹介します。", ORG_LD)
top += header("index.html") + f"""
<section class="hero">
  <div class="bgtext" aria-hidden="true" data-speed="-.06">natural</div>
  <i class="wm tr" aria-hidden="true"></i><i class="wm flower bl" aria-hidden="true"></i>
  <div class="hero-in">
    <div class="copy">
      <div class="mark" data-hero data-split>ecoloco</div><span class="kana rv">エコロコ</span>
      <h1 data-hero data-split style="--d:.5s">みんなが待ってた、<br>ほんとうに使える欲しい服。</h1>
      <p class="sub rv" style="--d:.9s">着心地がいい。ちょうどいい。ちょっとたのしく、気持ちよく。</p>
      <div class="rv" style="--d:1.1s;display:flex;flex-wrap:wrap;gap:22px;align-items:center">{SHOP_BTN.format(cls="lg")}<a class="tlink" href="about.html">About us</a></div>
      <span class="shop-note rv" style="--d:1.2s">楽天市場のショップページへ移動します</span>
      <a class="btn sm" data-yahoo href="#" hidden style="margin-top:12px">Yahoo!ショッピング</a>
    </div>
    <div class="stage" aria-hidden="false">
      <div class="fr a" data-speed=".04"><img src="assets/img/m9.webp" alt="編み込みの髪で後ろ姿を見せるモデル。ライトグレーのトップス" width="700" height="780" fetchpriority="high"><img src="assets/img/m6.webp" alt="白いトップスを着たモデル" width="700" height="780"></div>
      <div class="fr b" data-speed="-.05"><img src="assets/img/m10.webp" alt="ネイビーのベストを着たモデル" width="700" height="780"><img src="assets/img/m11.webp" alt="グリーンのカーディガンを着たモデル" width="700" height="780"></div>
      <div class="fr c" data-speed=".08"><img src="assets/img/m15.webp" alt="袖を広げて着心地を見せるモデル" width="700" height="700"><img src="assets/img/m12.webp" alt="ブラウンのトップスの襟元のアップ" width="700" height="700"></div>
      <a class="badge" data-shop="shop" href="https://www.rakuten.co.jp/auc-ecoloco/" target="_blank" rel="noopener" aria-label="ONLINE SHOP 楽天市場で見る"><i></i>
        <svg viewBox="0 0 120 120" aria-hidden="true"><defs><path id="cp" d="M60 60m-47 0a47 47 0 1 1 94 0a47 47 0 1 1-94 0"/></defs><text><textPath href="#cp">online shop · 楽天市場 · online shop · 楽天市場 ·</textPath></text></svg><b>SHOP</b></a>
    </div>
  </div>
  <div class="vtag vt" aria-hidden="true">大人のための、天然素材ナチュラル服</div>
  <div class="scroll" aria-hidden="true">Scroll</div>
</section>
<div class="marq" aria-hidden="true"><div class="tr">{MARQ}{MARQ}</div></div>

<section class="sec about" id="about">
  <div class="ghost" aria-hidden="true"><img src="assets/img/m12.webp" alt="" style="right:-8%;top:-10%;width:52%;height:120%" data-speed=".05"></div>
  <i class="wm tl" aria-hidden="true"></i>
  <div class="wrap"><div class="split">
    <div class="pw"><div class="ph ir"><img src="assets/img/m11.webp" alt="グリーンのカーディガンを着たモデル" loading="lazy" width="700" height="780" data-speed=".03"></div>
    <div class="ph2 ir" style="--d:.3s"><img src="assets/img/sj5.webp" alt="縫製工場のミシンとスレッド" loading="lazy" width="1000" height="1350"></div></div>
    <div class="tx">
      <span class="idx rv" aria-hidden="true">01</span>
      <div class="head" style="margin-top:12px"><span class="en rv">About ecoloco</span><h2 data-split>天然素材で、<br>毎日をととのえる。</h2></div>
      <p class="lead rv">ecolocoは、リネンやコットンなど天然素材を中心にした、大人の女性のためのナチュラル服ブランドです。</p>
      <p class="rv" style="--d:.1s">私たちはレディースファッションのEC運営と、オリジナルブランドの企画をしています。毎日のなかで本当に使える一着を、ていねいにお届けしたいと考えています。</p>
      <a class="tlink rv" href="about.html" style="--d:.2s">Company profile</a>
    </div>
  </div></div>
</section>

<section class="sec tint prom">
  <i class="wm br" aria-hidden="true"></i>
  <div class="wrap">
    {sec_head("Our promise", "ブランドの約束")}
    <div>
      <div class="row rv"><span class="n">01</span><h3>着心地がいい。</h3><p>肌にふれるものだから、素材のやさしさを大切にしています。</p><div class="th ir zm"><img src="assets/img/m14.webp" alt="袖口のステッチのアップ" loading="lazy" width="700" height="700"></div></div>
      <div class="row rv"><span class="n">02</span><h3>ちょうどいい。</h3><p>がんばりすぎず、毎日にちょうどいい服を。</p><div class="th ir zm"><img src="assets/img/m15.webp" alt="袖を広げて着心地を見せるモデル" loading="lazy" width="700" height="700"></div></div>
      <div class="row rv"><span class="n">03</span><h3>ちょっとたのしく、<br>気持ちよく。</h3><p>着るたびに、すこし気分が上がるように。</p><div class="th ir zm"><img src="assets/img/m10.webp" alt="ネイビーのベストを着たモデル" loading="lazy" width="700" height="780"></div></div>
    </div>
  </div>
</section>

<section class="sec">
  <i class="wm flower tr" aria-hidden="true"></i>
  <div class="wrap">
    <div style="display:flex;justify-content:space-between;align-items:flex-end;flex-wrap:wrap;gap:20px">{sec_head("Original brand", "オリジナルブランド")}<a class="tlink rv" href="original-brand.html" style="margin-bottom:clamp(36px,6vw,72px)">View all</a></div>
    <div class="hs" id="brands" role="list"></div>
    <span class="shop-note">商品の購入は、楽天市場のショップページで承っています。</span>
  </div>
</section>

<section class="sec paper">
  <div class="ghost" aria-hidden="true"><img src="assets/img/sj7.webp" alt="" style="left:-8%;top:-20%;width:46%;height:150%" data-speed="-.05"></div>
  <div class="wrap"><div class="split rev">
    <div class="tx" style="position:relative">
      <span class="idx rv" aria-hidden="true">02</span>
      <div class="head" style="margin-top:12px"><span class="en rv">Work style</span><h2 data-split>一緒に働きたい人の、<br>5つの言葉。</h2></div>
      <p class="rv">どのポジションでも、仕事の取り組み方に共感してくださる方と働きたいと考えています。</p>
      <a class="tlink rv" href="work-style.html">Read more</a>
    </div>
    <nav class="words" aria-label="一緒に働きたい人物像">
      <a class="rv" href="work-style.html"><span>01</span><b>職人的マインド</b></a>
      <a class="rv" style="--d:.08s" href="work-style.html"><span>02</span><b>バランス感覚</b></a>
      <a class="rv" style="--d:.16s" href="work-style.html"><span>03</span><b>「そもそも」を考える</b></a>
      <a class="rv" style="--d:.24s" href="work-style.html"><span>04</span><b>チームワーク</b></a>
      <a class="rv" style="--d:.32s" href="work-style.html"><span>05</span><b>生産性</b></a>
    </nav>
  </div></div>
</section>

<section class="band">
  <img src="assets/img/m16.webp" alt="" data-speed=".08" loading="lazy">
  <div class="wrap"><span class="en">Recruit</span>
  <h2 data-split>あなたの「ちょうどいい」を、<br>ここでかたちに。</h2>
  <p class="rv">カメラマン・スタイリスト・モデル・カスタマーサービス・デザイナー・ライター・コーダー・Webディレクターを募集しています。</p>
  <a class="btn rv" href="recruit.html">採用情報を見る</a></div>
</section>

<section class="sec" style="text-align:center">
  <i class="wm flower bl" aria-hidden="true"></i>
  <div class="narrow">
    {sec_head("Contact", "お問い合わせ", True)}
    <p class="rv">お取引・メディア掲載・その他のご相談は、お問い合わせフォームからご連絡ください。</p>
    <a class="btn rv" href="contact.html">お問い合わせフォーム</a>
  </div>
</section>
""" + FOOTER % ""
write("index.html", top)

# ---------------- ABOUT ----------------
ab = head("about.html", "ABOUT US｜会社概要｜ecoloco（株式会社ワイズフリー）", "ecoloco（エコロコ）を運営する株式会社ワイズフリーの考え方、事業内容、会社概要、アクセス（大阪市中央区久太郎町）をご紹介します。", ORG_LD)
ab += header("about.html") + page_hero("ABOUT US", "私たちについて") + f"""
<section class="sec about" style="padding-top:20px">
  <div class="wrap"><div class="split">
    <div class="ph ir"><img src="assets/img/m6.webp" alt="白いトップスを着たモデル" loading="lazy" width="700" height="780" data-speed=".03"></div>
    <div class="tx">
      <div class="head"><span class="en rv">Philosophy</span><h2 data-split>着心地がいい。<br>ちょうどいい。</h2></div>
      <p class="lead rv">ちょっとたのしく、気持ちよく。</p>
      <p class="rv">ecolocoは、「みんなが待ってた、ほんとうに使える欲しい服」を目指しています。リネンやコットンなど、ナチュラルな素材を中心に、大人の女性が毎日の暮らしのなかで心地よく着られる服を、私たちの目線で選び、企画しています。</p>
    </div>
  </div></div>
</section>
<section class="sec tint">
  <div class="ghost" aria-hidden="true"><img src="assets/img/sj8.webp" alt="" style="right:-6%;top:-20%;width:40%;height:150%" data-speed=".05"></div>
  <div class="narrow">
  {sec_head("Business", "事業内容")}
  <ul class="rv" style="padding-left:1.2em"><li>レディースファッション（リネン・コットン等ナチュラル素材中心）のEC運営</li><li>オリジナルブランドの企画<br><span style="font-size:14px;color:var(--ink-soft)">earth_eco_loco／SOCOCOTI／SO／sel／nachukara／DOVERS ほか</span></li></ul>
  <p style="margin-top:24px">{SHOP_BTN.format(cls="")}<span class="shop-note">楽天市場のショップページへ移動します</span></p>
</div></section>
<section class="sec"><div class="narrow">
  {sec_head("Company", "会社概要")}
  <table class="tbl rv"><tbody id="company-table"></tbody></table>
  <noscript><p>会社名：株式会社ワイズフリー／所在地：〒541-0056 大阪府大阪市中央区久太郎町3丁目5番5号 丸忠第一ビル5F／電話：06-6281-0800（平日10:00〜13:00）</p></noscript>
</div></section>
<section class="sec tint"><i class="wm tl" aria-hidden="true"></i><div class="narrow">
  {sec_head("Access", "アクセス")}
  <p class="rv">〒541-0056 大阪府大阪市中央区久太郎町3丁目5番5号 丸忠第一ビル5F</p>
  <div class="map rv"><iframe title="株式会社ワイズフリーの地図" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://www.google.com/maps?q=%E5%A4%A7%E9%98%AA%E5%BA%9C%E5%A4%A7%E9%98%AA%E5%B8%82%E4%B8%AD%E5%A4%AE%E5%8C%BA%E4%B9%85%E5%A4%AA%E9%83%8E%E7%94%BA3%E4%B8%81%E7%9B%AE5%E7%95%AA5%E5%8F%B7&output=embed"></iframe></div>
  <p style="margin-top:14px"><a href="https://www.google.com/maps/search/?api=1&query=%E5%A4%A7%E9%98%AA%E5%BA%9C%E5%A4%A7%E9%98%AA%E5%B8%82%E4%B8%AD%E5%A4%AE%E5%8C%BA%E4%B9%85%E5%A4%AA%E9%83%8E%E7%94%BA3%E4%B8%81%E7%9B%AE5%E7%95%AA5%E5%8F%B7" target="_blank" rel="noopener">Googleマップで開く</a></p>
</div></section>
""" + FOOTER % ""
write("about.html", ab)

# ---------------- WORK STYLE ----------------
ws = head("work-style.html", "WORK STYLE｜一緒に働きたい人物像｜ecoloco（株式会社ワイズフリー）", "ecoloco（株式会社ワイズフリー）が一緒に働きたい人物像を5つの言葉でご紹介します。職人的マインド、バランス感覚、「そもそも」を考える、チームワーク、生産性。")
ws += header("work-style.html") + page_hero("WORK STYLE", "一緒に働きたい人") + """
<section class="sec" style="padding-top:20px"><i class="wm br" aria-hidden="true"></i><div class="wrap">
  <p class="lead rv" style="max-width:34em;margin-bottom:56px">どのポジションでも共通して、私たちは「仕事の取り組み方」に共感してくださる方と一緒に働きたいと考えています。</p>
  <div id="values"></div>
  <noscript><p>職人的マインド／バランス感覚／「そもそも」を考える／チームワーク／生産性（時短ではなく、やり方を更新する柔軟性）</p></noscript>
  <div style="margin-top:64px" class="rv"><a class="btn fill lg" href="recruit.html">採用情報を見る</a></div>
</div></section>
""" + FOOTER % ""
write("work-style.html", ws)

# ---------------- ORIGINAL BRAND ----------------
ob = head("original-brand.html", "ORIGINAL BRAND｜ecoloco（株式会社ワイズフリー）", "ecolocoのオリジナルブランド earth_eco_loco、SOCOCOTI、SO、sel、nachukara、DOVERS をご紹介。購入は楽天市場のショップページから。")
ob += header("original-brand.html") + page_hero("ORIGINAL BRAND", "オリジナルブランド") + f"""
<section class="sec" style="padding-top:20px"><i class="wm tl" aria-hidden="true"></i><div class="wrap">
  <p class="lead rv" style="max-width:34em;margin-bottom:56px">私たちが企画するオリジナルブランドです。商品のご購入は、楽天市場のショップページで承っています。</p>
  <div class="grid-b" id="brands"></div>
  <p style="margin-top:56px;text-align:center" class="rv">{SHOP_BTN.format(cls="lg")}<span class="shop-note">楽天市場のショップページへ移動します</span></p>
</div></section>
""" + FOOTER % ""
write("original-brand.html", ob)


# ---------------- RECRUIT ----------------
def field_common(prefix=""):
    return ""
rc = head("recruit.html", "RECRUIT｜採用情報｜ecoloco（株式会社ワイズフリー）", "ecoloco（株式会社ワイズフリー）の採用情報。カメラマン・スタイリスト・モデル・カスタマーサービス・デザイナー・ライター・コーダー・Webディレクターを募集中。応募フォームはこちら。")
PREF = "北海道,青森県,岩手県,宮城県,秋田県,山形県,福島県,茨城県,栃木県,群馬県,埼玉県,千葉県,東京都,神奈川県,新潟県,富山県,石川県,福井県,山梨県,長野県,岐阜県,静岡県,愛知県,三重県,滋賀県,京都府,大阪府,兵庫県,奈良県,和歌山県,鳥取県,島根県,岡山県,広島県,山口県,徳島県,香川県,愛媛県,高知県,福岡県,佐賀県,長崎県,熊本県,大分県,宮崎県,鹿児島県,沖縄県,海外".split(",")
pref_opts = "<option value=''>選択してください</option>" + "".join(f"<option>{p}</option>" for p in PREF)
rc += header("recruit.html") + page_hero("RECRUIT", "採用情報") + f"""
<section class="sec" style="padding-top:20px"><i class="wm br" aria-hidden="true"></i><div class="narrow">
  <h2 class="rv" style="font-size:clamp(22px,3.6vw,30px);margin-bottom:18px">こんな方と一緒に働きたいです</h2>
  <p class="rv">どのポジションでも、私たちは「仕事の取り組み方」に共感してくださる方と一緒に働きたいと考えています。職人的マインド、バランス感覚、「そもそも」を考える、チームワーク、生産性——くわしくは <a href="work-style.html">WORK STYLE</a> をご覧ください。</p>
</div></section>
<section class="sec tint" id="jobs-sec"><div class="narrow">
  {sec_head("POSITIONS", "募集職種")}
  <div id="jobs"></div>
  <noscript><p>募集職種：カメラマン／スタイリスト／モデル／カスタマーサービス／デザイナー／ライター／コーダー／Webディレクター。詳細はお問い合わせください（06-6281-0800・ecoloco-yahoo@ysfree.jp）。</p></noscript>
  <p style="font-size:13px;color:var(--ink-soft)">給与：勤務条件・経験によります。お問い合わせください。</p>
</div></section>
<section class="sec" id="apply"><i class="wm tr" aria-hidden="true"></i><div class="narrow">
  {sec_head("APPLY", "応募フォーム")}
  <form class="form rv" data-form="recruit" novalidate>
    <div class="msg" role="alert"></div>
    <div class="field"><label for="name">お名前<span class="req">必須</span></label><input id="name" name="name" type="text" autocomplete="name" data-required><div class="err">お名前をご入力ください。</div></div>
    <div class="field"><label for="kana">ふりがな<span class="req">必須</span></label><input id="kana" name="kana" type="text" data-required><div class="err">ふりがなをご入力ください。</div></div>
    <div class="field"><label for="email">メールアドレス<span class="req">必須</span></label><input id="email" name="email" type="email" autocomplete="email" inputmode="email" data-required><div class="err">メールアドレスの形式をご確認ください。</div></div>
    <div class="field"><label for="tel">電話番号<span class="req">必須</span></label><input id="tel" name="tel" type="tel" autocomplete="tel" inputmode="tel" data-required><div class="err">電話番号をご入力ください。</div></div>
    <div class="field"><label for="job">希望職種<span class="req">必須</span></label><select id="job" name="job" data-required></select><div class="err">希望職種をお選びください。</div></div>
    <div class="field"><label for="emp">希望雇用形態<span class="req">必須</span></label><select id="emp" name="employment" data-required><option value="">選択してください</option><option>正社員</option><option>契約社員</option><option>アルバイト</option><option>外注</option></select><div class="err">希望雇用形態をお選びください。</div></div>
    <div class="field"><label for="pref">現在のお住まい（都道府県）<span class="req">必須</span></label><select id="pref" name="prefecture" autocomplete="address-level1" data-required>{pref_opts}</select><div class="err">都道府県をお選びください。</div></div>
    <div class="field"><label for="url">ポートフォリオURL<span class="opt">任意（デザイナー・カメラマン・コーダー等）</span></label><input id="url" name="portfolio" type="url" inputmode="url" placeholder="https://"></div>
    <div class="field"><label for="pr">経験・自己PR<span class="opt">任意</span></label><textarea id="pr" name="pr"></textarea></div>
    <fieldset><legend>希望の連絡方法<span class="opt">任意</span></legend>
      <label class="chk"><input type="radio" name="contact_method" value="メール" checked> メール</label>
      <label class="chk"><input type="radio" name="contact_method" value="電話"> 電話（平日 10:00〜13:00）</label></fieldset>
    <div class="hp" aria-hidden="true"><label>website<input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>
    <div class="field"><label class="chk"><input type="checkbox" name="agree" data-required><span><a href="privacy.html" target="_blank" rel="noopener">プライバシーポリシー</a>に同意します<span class="req">必須</span></span></label><div class="err">同意が必要です。</div></div>
    <button class="btn fill lg" type="submit">送信する</button>
  </form>
</div></section>
""" + FOOTER % '<script src="js/forms.js"></script><script src="js/jobposting.js"></script>'
write("recruit.html", rc)

# ---------------- CONTACT ----------------
ct = head("contact.html", "CONTACT｜お問い合わせ｜ecoloco（株式会社ワイズフリー）", "株式会社ワイズフリー（ecoloco）へのお取引・メディア掲載・その他のお問い合わせフォームです。")
ct += header("contact.html") + page_hero("CONTACT", "お問い合わせ") + """
<section class="sec" style="padding-top:20px"><i class="wm br" aria-hidden="true"></i><div class="narrow">
  <p class="rv">お取引・メディア掲載・その他のご相談を承っています。内容を確認のうえ、担当者よりご連絡いたします。<br>商品のご注文・配送などに関するお問い合わせは、ご購入された<a href="https://www.rakuten.co.jp/auc-ecoloco/" data-shop="shop" target="_blank" rel="noopener">楽天市場のショップページ</a>からお願いいたします。</p>
  <p class="rv" style="font-size:14px;color:var(--ink-soft)">お電話：06-6281-0800（平日 10:00〜13:00）</p>
  <p class="rv" style="font-size:14px;color:var(--ink-soft)">採用に関するお問い合わせは <a href="recruit.html#apply">RECRUIT の応募フォーム</a> からお願いします。</p>
  <div class="sp"></div>
  <form class="form rv" data-form="contact" novalidate>
    <div class="msg" role="alert"></div>
    <div class="field"><label for="name">お名前<span class="req">必須</span></label><input id="name" name="name" type="text" autocomplete="name" data-required><div class="err">お名前をご入力ください。</div></div>
    <div class="field"><label for="company">会社名<span class="opt">任意</span></label><input id="company" name="company" type="text" autocomplete="organization"></div>
    <div class="field"><label for="email">メールアドレス<span class="req">必須</span></label><input id="email" name="email" type="email" autocomplete="email" inputmode="email" data-required><div class="err">メールアドレスの形式をご確認ください。</div></div>
    <div class="field"><label for="tel">電話番号<span class="opt">任意</span></label><input id="tel" name="tel" type="tel" autocomplete="tel" inputmode="tel"></div>
    <div class="field"><label for="type">お問い合わせ種別<span class="req">必須</span></label><select id="type" name="type" data-required><option value="">選択してください</option><option>お取引について</option><option>メディア掲載・取材について</option><option>その他</option></select><div class="err">種別をお選びください。</div></div>
    <div class="field"><label for="body">お問い合わせ内容<span class="req">必須</span></label><textarea id="body" name="body" data-required></textarea><div class="err">内容をご入力ください。</div></div>
    <div class="hp" aria-hidden="true"><label>website<input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>
    <div class="field"><label class="chk"><input type="checkbox" name="agree" data-required><span><a href="privacy.html" target="_blank" rel="noopener">プライバシーポリシー</a>に同意します<span class="req">必須</span></span></label><div class="err">同意が必要です。</div></div>
    <button class="btn fill lg" type="submit">送信する</button>
  </form>
</div></section>
""" + FOOTER % '<script src="js/forms.js"></script>'
write("contact.html", ct)

# ---------------- PRIVACY ----------------
pv = head("privacy.html", "プライバシーポリシー｜ecoloco（株式会社ワイズフリー）", "株式会社ワイズフリー（ecoloco）の個人情報の取扱いについて。")
pv += header("privacy.html") + page_hero("PRIVACY POLICY", "プライバシーポリシー") + """
<!-- 【要法務確認】以下は雛形です。公開前に必ず法務・顧問などの確認を受けてください。 -->
<section class="sec" style="padding-top:20px"><div class="narrow prose">
  <p>株式会社ワイズフリー（以下「当社」）は、当サイトでお預かりする個人情報を、以下の方針に従って適切に取り扱います。</p>
  <h2>1. 取得する情報</h2><p>お問い合わせ・採用応募フォームを通じて、お名前、ふりがな、会社名、メールアドレス、電話番号、お住まいの都道府県、ポートフォリオURL、お問い合わせ内容・自己PR等をご入力いただく場合があります。</p>
  <h2>2. 利用目的</h2><ul><li>お問い合わせへの回答・ご連絡のため</li><li>採用選考に関するご連絡・選考のため</li><li>取引に関するご連絡のため</li></ul>
  <h2>3. 第三者提供</h2><p>法令に基づく場合を除き、ご本人の同意なく第三者に個人情報を提供しません。</p>
  <h2>4. 業務委託・外部サービスの利用</h2><p>フォームの受信・記録・自動返信には、Google LLC が提供するサービス（Google Apps Script、Google スプレッドシート、Gmail）を利用します。【要法務確認】海外への情報移転に関する表記</p>
  <h2>5. 安全管理</h2><p>個人情報への不正アクセス、紛失、漏えい等を防ぐため、必要かつ適切な安全管理措置を講じます。</p>
  <h2>6. 保存期間</h2><p>【要法務確認】利用目的の達成に必要な期間保存し、不要となった情報は適切に削除します。</p>
  <h2>7. 開示・訂正・利用停止等のご請求</h2><p>ご本人からの開示・訂正・利用停止等のご請求は、下記の窓口までご連絡ください。</p>
  <h2>8. お問い合わせ窓口</h2><p>株式会社ワイズフリー<br>〒541-0056 大阪府大阪市中央区久太郎町3丁目5番5号 丸忠第一ビル5F<br>電話：06-6281-0800（平日 10:00〜13:00）<br>メール：<a data-cfg="email" href="mailto:ecoloco-yahoo@ysfree.jp">ecoloco-yahoo@ysfree.jp</a></p>
  <p style="color:var(--ink-soft);font-size:13px">【要確認】制定日・改定日を記載してください。</p>
</div></section>
""" + FOOTER % ""
write("privacy.html", pv)

# ---------------- THANKS ----------------
th = head("thanks.html", "送信完了｜ecoloco（株式会社ワイズフリー）", "お問い合わせ・応募の送信が完了しました。", noindex=True)
th += header("") + """
<section class="sec" style="min-height:70vh"><i class="wm tr" aria-hidden="true"></i><i class="wm flower bl" aria-hidden="true"></i><div class="narrow thanks">
  <img class="ic" src="assets/flower.svg" alt="" width="96" height="96">
  <h1 class="rv" style="font-size:clamp(22px,4vw,30px);margin-bottom:18px">送信が完了しました</h1>
  <p class="rv" id="t-msg">お問い合わせありがとうございます。内容を確認のうえ、担当者よりご連絡いたします。自動返信メールが届かない場合は、迷惑メールフォルダもご確認ください。</p>
  <p class="rv"><a class="btn" href="index.html">TOPへ戻る</a></p>
</div></section>
""" + FOOTER % """<script>(function(){var t=new URLSearchParams(location.search).get("type");if(t==="recruit"){document.getElementById("t-msg").textContent="ご応募ありがとうございます。内容を確認のうえ、担当者より、メールまたはお電話でご連絡いたします。自動返信メールが届かない場合は、迷惑メールフォルダもご確認ください。";}})();</script>"""
write("thanks.html", th)

# sitemap / robots
urls = ["", "about.html", "work-style.html", "original-brand.html", "recruit.html", "contact.html", "privacy.html"]
write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{SITE}/{u}</loc></url>\n" for u in urls) + "</urlset>\n")
write("robots.txt", f"User-agent: *\nAllow: /\nDisallow: /thanks.html\n\nSitemap: {SITE}/sitemap.xml\n")
print("built")
