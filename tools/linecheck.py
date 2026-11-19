# -*- coding: utf-8 -*-
"""改行チェック：複数行になった要素のうち、最終行が極端に短い（約2.6字未満）もの／ボタンが折り返しているものを列挙する"""
from playwright.sync_api import sync_playwright
JS = """()=>{const out=[];const els=[...document.querySelectorAll('h1,h2,h3,p,li,a,.btn,dt,dd,td,th,summary span,.note,.lead,b')];
for(const e of els){ if(e.closest('.curtain,.hp,.ftr .big,[aria-hidden=true]')) continue; if(e.querySelector('h1,h2,h3,p,li,div')) continue;
 const t=(e.innerText||'').trim(); if(t.length<2) continue; const cs=getComputedStyle(e); if(cs.display==='none'||cs.visibility==='hidden') continue;
 const r=document.createRange(); r.selectNodeContents(e); const rects=[...r.getClientRects()].filter(x=>x.width>1&&x.height>1);
 if(!rects.length) continue;
 const lines={}; rects.forEach(x=>{const k=Math.round(x.top/6);lines[k]=(lines[k]||0)+x.width});
 const ks=Object.keys(lines).map(Number).sort((a,b)=>a-b); if(ks.length<2) continue;
 const fs=parseFloat(cs.fontSize); const last=lines[ks[ks.length-1]];
 const isBtn=e.classList.contains('btn')||e.classList.contains('tlink')||e.classList.contains('ig-btn');
 if(isBtn||last<fs*2.6) out.push([e.tagName+'.'+e.className, ks.length, Math.round(last/fs*10)/10, t.slice(0,40)]);}
return out}"""
pages = ['index', 'about', 'work-style', 'original-brand', 'recruit', 'contact', 'privacy', 'thanks']
n = 0
with sync_playwright() as p:
    b = p.chromium.launch()
    for name, vp in (('pc', {'width': 1440, 'height': 900}), ('tab', {'width': 820, 'height': 1000}), ('sp', {'width': 390, 'height': 844}), ('sp320', {'width': 320, 'height': 700})):
        c = b.new_context(viewport=vp, reduced_motion='reduce')
        for pgn in pages:
            pg = c.new_page(); pg.goto(f'http://localhost:8765/{pgn}.html', wait_until='networkidle'); pg.wait_for_timeout(500)
            for r in pg.evaluate(JS):
                print(name, pgn, r); n += 1
            pg.close()
print('issues:', n)
