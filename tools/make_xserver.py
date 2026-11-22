# -*- coding: utf-8 -*-
"""Xサーバー本番用の納品フォルダとzipを作る。
使い方: python3 tools/make_xserver.py ドメイン名   例) python3 tools/make_xserver.py ecoloco.jp
・サイト内のURL（canonical / OGP / 構造化データ / sitemap / robots / llms.txt）を本番ドメインに一括置換
・PHPフォーム（form/）と .htaccess を同梱
・開発用ファイル（tools, docs, gas, banner など）は含めない"""
import os, re, shutil, sys, zipfile
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OLD = "https://livmakers.github.io/ecoloco-corp/"
if len(sys.argv) < 2 or not re.fullmatch(r"[a-z0-9.-]+\.[a-z]{2,}", sys.argv[1].lower()):
    sys.exit("ドメイン名を指定してください 例) python3 tools/make_xserver.py ecoloco.jp")
DOMAIN = sys.argv[1].lower().removeprefix("www.")
NEW = f"https://{DOMAIN}/"
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, "dist")
SITE = os.path.join(OUT, "public_html")
INCLUDE = ["index.html", "about.html", "work-style.html", "original-brand.html", "recruit.html", "contact.html",
           "privacy.html", "thanks.html", "robots.txt", "sitemap.xml", "llms.txt", "config.js", "assets", "css", "js", "content", "recruit"]
TEXT = (".html", ".js", ".css", ".txt", ".xml", ".json", ".php")
if os.path.exists(OUT): shutil.rmtree(OUT)
os.makedirs(SITE)
for name in INCLUDE:
    src = os.path.join(ROOT, name)
    dst = os.path.join(SITE, name)
    (shutil.copytree if os.path.isdir(src) else shutil.copy2)(src, dst)
shutil.copytree(os.path.join(ROOT, "deploy", "form"), os.path.join(SITE, "form"))
shutil.copy2(os.path.join(ROOT, "deploy", "htaccess.txt"), os.path.join(SITE, ".htaccess"))
shutil.move(os.path.join(SITE, "form", "htaccess.txt"), os.path.join(SITE, "form", ".htaccess"))
os.remove(os.path.join(SITE, "assets", "image-manifest.json")) if os.path.exists(os.path.join(SITE, "assets", "image-manifest.json")) else None
n = 0
for d, _, fs in os.walk(SITE):
    for f in fs:
        p = os.path.join(d, f)
        if not (f.endswith(TEXT) or f == ".htaccess"): continue
        s = open(p, encoding="utf-8").read()
        t = s.replace(OLD, NEW).replace("__DOMAIN__", DOMAIN)
        if f == "config.js": t = re.sub(r'ECOLOCO_URL: "[^"]*"', f'ECOLOCO_URL: "{NEW}"', t)
        if t != s: open(p, "w", encoding="utf-8").write(t); n += 1
left = [os.path.join(d, f) for d, _, fs in os.walk(SITE) for f in fs if f.endswith(TEXT) and OLD in open(os.path.join(d, f), encoding="utf-8").read()]
if left: sys.exit("置換漏れ: " + ", ".join(left))
z = os.path.join(OUT, f"ecoloco-xserver-{DOMAIN}.zip")
with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
    for d, _, fs in os.walk(SITE):
        for f in fs:
            p = os.path.join(d, f); zf.write(p, os.path.relpath(p, SITE))
print(f"OK: {n}ファイルのURLを {NEW} に置換 → {z}")
