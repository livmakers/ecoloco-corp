import sys
from playwright.sync_api import sync_playwright
pages=sys.argv[1].split(',');dev=sys.argv[2] if len(sys.argv)>2 else 'pc'
vp={'pc':{'width':1440,'height':900},'sp':{'width':390,'height':844}}[dev]
with sync_playwright() as p:
    b=p.chromium.launch();c=b.new_context(viewport=vp,is_mobile=(dev=='sp'));
    for n in pages:
        pg=c.new_page();errs=[];pg.on('console',lambda m:errs.append(m.text) if m.type=='error' else None);pg.on('pageerror',lambda e:errs.append(str(e)))
        pg.goto(f'http://localhost:8765/{n}.html',wait_until='networkidle');pg.wait_for_timeout(3200)
        h=pg.evaluate('document.documentElement.scrollHeight')
        for y in range(0,h,500): pg.evaluate(f'window.scrollTo(0,{y})');pg.wait_for_timeout(140)
        pg.wait_for_timeout(1800);pg.evaluate('window.scrollTo(0,0)');pg.wait_for_timeout(600)
        pg.screenshot(path=f'docs/screens/{dev}-{n}.png',full_page=True);print(n,dev,'h',h,'errs',errs[:3]);pg.close()
    b.close()
