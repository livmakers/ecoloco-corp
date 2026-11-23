#!/usr/bin/env python3
"""会社サイト（ysfree.co.jp 直下）の構造化データを付け直す。何度実行しても同じ結果になる。

- 全ページ（thanks.html 以外）：Organization（会社名・ロゴ・公式ショップ/SNS・住所・ブランド）
- トップ：WebSite
- 下層ページ：BreadcrumbList（TOP > ページ名）
電話番号は入れない方針。お問い合わせはフォームのページを contactPoint に指定する。
※ HTMLは tools/build.py 生成後に手直しが入っているため、build.py は再実行せずこのスクリプトで更新する。
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://ysfree.co.jp"
BRANDS = ["ecoloco", "earth_eco_loco", "SOCOCOTI", "SO", "sel", "nachukara", "DOVERS"]

ORG = {
    "@type": "Organization",
    "@id": SITE + "/#org",
    "name": "株式会社ワイズフリー",
    "alternateName": ["ecoloco", "エコロコ"],
    "url": SITE + "/",
    "logo": {"@type": "ImageObject", "url": SITE + "/assets/img/logo.png"},
    "image": SITE + "/assets/img/ogp.jpg",
    "description": "大人のための天然素材ナチュラル服「ecoloco（エコロコ）」を企画・販売する大阪市の会社。",
    "email": "ecoloco-yahoo@ysfree.jp",
    "address": {"@type": "PostalAddress", "postalCode": "541-0056", "addressRegion": "大阪府",
                "addressLocality": "大阪市中央区", "streetAddress": "久太郎町3丁目5番5号 丸忠第一ビル5F",
                "addressCountry": "JP"},
    "contactPoint": {"@type": "ContactPoint", "contactType": "customer support",
                     "url": SITE + "/contact.html", "availableLanguage": "ja"},
    "sameAs": ["https://www.rakuten.co.jp/auc-ecoloco/", "https://store.shopping.yahoo.co.jp/ecoloco/",
               "https://www.instagram.com/ecoloco.official/"],
    "brand": [{"@type": "Brand", "name": b} for b in BRANDS],
}
WEBSITE = {"@type": "WebSite", "@id": SITE + "/#website", "name": "ecoloco（エコロコ）｜株式会社ワイズフリー",
           "url": SITE + "/", "inLanguage": "ja", "publisher": {"@id": SITE + "/#org"}}

PAGES = {  # ファイル名: パンくずの名前（None はトップ）
    "index.html": None,
    "about.html": "会社概要（ABOUT US）",
    "work-style.html": "一緒に働きたい人（WORK STYLE）",
    "original-brand.html": "オリジナルブランド",
    "recruit.html": "採用情報",
    "contact.html": "お問い合わせ",
    "privacy.html": "プライバシーポリシー",
}

MARK = "<!--schema-->"
LD_RE = re.compile(r'\n?(?:<!--schema-->)?<script type="application/ld\+json">.*?</script>', re.S)


def crumbs(name, file):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "ecoloco TOP", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": name, "item": f"{SITE}/{file}"}]}


def main():
    for file, name in PAGES.items():
        p = ROOT / file
        s = p.read_text(encoding="utf-8")
        graph = [ORG, WEBSITE] if name is None else [ORG, crumbs(name, file)]
        ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False).replace("<", "\\u003c")
        s = LD_RE.sub("", s)
        s = s.replace("</head>", f'{MARK}<script type="application/ld+json">{ld}</script>\n</head>', 1)
        p.write_text(s, encoding="utf-8")
    print("schema updated:", ", ".join(PAGES))


if __name__ == "__main__":
    main()
