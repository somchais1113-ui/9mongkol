"""Build a browser-openable, entirely offline snapshot of the existing app.
The backend is still the production-of-the-MVP code path, not this static snapshot.
"""
from __future__ import annotations
import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WEB = ROOT / 'web'
meta_rules = json.loads((ROOT/'app'/'rulebook.json').read_text('utf-8'))
meta_careers = json.loads((ROOT/'app'/'careers.json').read_text('utf-8'))
con = sqlite3.connect(ROOT/'ni.sqlite3')
con.row_factory = sqlite3.Row
rows = [dict(r) for r in con.execute('SELECT n.number,n.core FROM numbers n ORDER BY n.number')]
by_number = {r['number']:r for r in rows}
for row in rows:
    row['scores']={}
    row['offers']=[]
for r in con.execute('SELECT n.number,c.career_id,c.score FROM numbers n JOIN career_scores c ON c.number_id=n.id'):
    by_number[r['number']]['scores'][r['career_id']]=r['score']
for r in con.execute('SELECT n.number,o.source,o.external_id,o.price,o.status,o.url,o.last_seen,o.is_demo,o.permission_basis FROM numbers n JOIN offers o ON o.number_id=n.id'):
    o=dict(r);by_number[o.pop('number')]['offers'].append(o)
imports=[dict(r) for r in con.execute('SELECT source,imported,rejected,created_at FROM import_logs ORDER BY id DESC LIMIT 5')]
con.close()
blob = {
 'meta':{
  'version':meta_rules['version'], 'career_version':meta_careers['version'],
  'attributes':meta_careers['attributes'],'careers':meta_careers['careers'],
  'rules':meta_rules['rules'],'disclaimer':meta_rules['description'],
  'baseline':meta_rules['baseline'],
 },
 'numbers':rows,
 'recent_imports':imports,
}
(WEB/'offline-data.js').write_text('/* Generated snapshot; synthetic demo data, no live data. */\nwindow.NI_OFFLINE_DATA='+json.dumps(blob,ensure_ascii=False,separators=(',',':'))+';\n',encoding='utf-8')
# same markup as server version, with only asset paths changed and offline bridge injected
html=(WEB/'index.html').read_text('utf-8')
for f in ('styles.css','storefront.css','celestial.css','insights.css','nine-mongkol.css','insights.js','app.js'):
    html=html.replace('/assets/'+f+'?v=0.6.0','web/'+f+'?v=0.6.0')
html=html.replace('/assets/nine-mongkol.css?v=0.7.0','web/nine-mongkol.css?v=0.7.0')
html=html.replace('/assets/nine-motion.css?v=0.7.0','web/nine-motion.css?v=0.7.0')
html=html.replace('/assets/nine-readable.css?v=0.8.0','web/nine-readable.css?v=0.8.0')
html=html.replace('/assets/nine-polish.css?v=0.9.0','web/nine-polish.css?v=0.9.0')
html=html.replace('/assets/nine-motion.js?v=0.7.0','web/nine-motion.js?v=0.7.0')
html=html.replace('/assets/assets/number-visual.svg','web/assets/number-visual.svg')
html=html.replace('/assets/assets/9mongkol/','web/assets/9mongkol/')
html=html.replace('<script defer="" src="web/insights.js?v=0.6.0"></script>',
    '<script defer src="web/offline-data.js?v=0.7.0"></script>\n'
    '<script defer src="web/offline-bridge.js?v=0.7.0"></script>\n'
    '<script defer="" src="web/insights.js?v=0.6.0"></script>')
html=html.replace('<span class="status-chip">ข้อมูลสาธิต · LOCAL MVP</span>',
                  '<span class="status-chip">OFFLINE DEMO · ไม่มีการบันทึกถาวร</span>')
html=html.replace('<div class="global-message" hidden="" id="global-message"></div>',
                  '<div class="global-message" id="offline-message" style="background:#fff3de;border-color:#d9aa61;color:#683321;margin-bottom:14px">'
                  '<strong>โหมดเปิดจาก index.html:</strong> ทดลองค้นหาเบอร์ วิเคราะห์อาชีพ และนำเข้าข้อมูลได้ในหน้านี้โดยไม่ต้องติดตั้งโปรแกรม '
                  'แต่ข้อมูลที่นำเข้าในโหมดนี้จะหายเมื่อรีเฟรชหน้า · สำหรับฐานข้อมูลจริงและการบันทึกถาวร ให้เปิดผ่าน <code>START_MAC.command</code> หรือ <code>run.sh</code>'
                  '</div>\n<div class="global-message" hidden="" id="global-message"></div>')
(ROOT/'index.html').write_text(html,encoding='utf-8')
print(f'Generated root index.html and offline-data.js for {len(rows)} unique demo numbers')
