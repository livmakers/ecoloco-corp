# -*- coding: utf-8 -*-
"""バナー生成：config.js の ECOLOCO_URL を読み、画像を埋め込んだ貼るだけスニペット banner/snippet.html と preview.html を作る
   PNG書き出し（Playwright）: python banner/make.py png"""
import os, re, io, base64, sys
from PIL import Image
D = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(D)
url = re.search(r'ECOLOCO_URL:\s*"([^"]+)"', open(os.path.join(R, 'config.js'), encoding='utf-8').read()).group(1)

def uri(path, q=88, w=None):
    im = Image.open(path)
    if w and im.width > w:
        im = im.resize((w, int(im.height * w / im.width)), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, 'WEBP', quality=q)
    return "data:image/webp;base64," + base64.b64encode(b.getvalue()).decode()

logo = uri(os.path.join(R, 'assets/img/logo-banner.png'), q=90, w=700)
pa = uri(os.path.join(R, 'assets/img/bn-photo0.webp'), q=80, w=520)
pb = uri(os.path.join(R, 'assets/img/bn-photo1.webp'), q=80, w=520)
T = open(os.path.join(D, 'template.html'), encoding='utf-8').read()

def render(shape='auto'):
    return (T.replace('{{LOGO}}', logo).replace('{{PH_A}}', pa).replace('{{PH_B}}', pb)
             .replace('{{URL}}', url).replace('{{SHAPE}}', shape))

def page(body):
    return ('<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>ECOLOCO グループ参画バナー プレビュー</title><style>body{margin:0}</style></head><body>' + body + '</body></html>')

open(os.path.join(D, 'snippet.html'), 'w', encoding='utf-8').write(render())
H = '<h1 style="font:600 14px sans-serif;margin:0">%s</h1>'
open(os.path.join(D, 'preview.html'), 'w', encoding='utf-8').write(page(
    '<div style="padding:24px;background:#fff;display:grid;gap:28px;max-width:1260px;margin:auto">'
    + H % '横長（自動）' + render()
    + H % 'スマホ幅375px（自動で2:1）' + '<div style="width:375px">' + render() + '</div>'
    + H % '正方形 data-shape="square"' + '<div style="width:420px">' + render('square') + '</div>'
    + H % '細長 data-shape="leader"' + '<div style="width:728px">' + render('leader') + '</div></div>'))

if 'png' in sys.argv:
    from playwright.sync_api import sync_playwright
    out = os.path.join(D, 'png'); os.makedirs(out, exist_ok=True)
    jobs = [('ecoloco_group_1200x300', 1200, 300, 'auto'), ('ecoloco_group_600x600', 600, 600, 'square'), ('ecoloco_group_728x90', 728, 90, 'leader')]
    tmp = os.path.join(D, '_tmp.html')
    with sync_playwright() as p:
        b = p.chromium.launch()
        for name, w, h, shape in jobs:
            pg = b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=1, reduced_motion='reduce')
            html = page(render(shape)).replace('border-radius:16px', 'border-radius:0').replace('border-radius:10px', 'border-radius:0').replace('box-shadow:0 6px 24px rgba(60,50,40,.14)', 'box-shadow:none')
            open(tmp, 'w', encoding='utf-8').write(html)
            pg.goto('file:///' + tmp.replace('\\', '/')); pg.wait_for_timeout(1800)
            pg.screenshot(path=os.path.join(out, name + '.png'), clip={'x': 0, 'y': 0, 'width': w, 'height': h}); print(name)
        b.close()
    os.remove(tmp)
print('banner built; URL =', url)
