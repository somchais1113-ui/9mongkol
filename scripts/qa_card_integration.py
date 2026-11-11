"""9MONGKOL v1.0 delivery smoke check (no browser setup required).

Verifies that both entry points reference the supplied card assets and checks
that the original FastAPI search/analyze APIs still return real data. For the
visual layout see screenshots in previews/v10_cards and run pytest for all tests.
"""
from pathlib import Path
from html.parser import HTMLParser
from urllib.request import Request, urlopen
import json
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]

class Refs(HTMLParser):
    def __init__(self):
        super().__init__(); self.refs=[]
    def handle_starttag(self, name, attrs):
        d=dict(attrs)
        for attr in ('src','href'):
            if d.get(attr):self.refs.append(d[attr].split('?')[0])

def main():
    for entry in ('index.html','web/index.html'):
        parser=Refs(); parser.feed((ROOT/entry).read_text('utf-8'))
        prefix='web/' if entry=='index.html' else '/assets/'
        for path in (f'{prefix}number-card/number-card.js',f'{prefix}number-card/number-card.css',f'{prefix}number-card/number-card-integration.css'):
            assert path in parser.refs,(entry,path)
    assert len(list((ROOT/'web/number-card/icons').glob('*.svg')))>=9
    proc=subprocess.Popen(['python3','-m','uvicorn','app.main:app','--host','127.0.0.1','--port','8878'],cwd=ROOT,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    try:
        for i in range(35):
            try:
                with urlopen('http://127.0.0.1:8878/api/health',timeout=1) as resp:
                    assert resp.status==200;break
            except Exception:time.sleep(.15)
        else:raise RuntimeError('Server unavailable')
        request=Request('http://127.0.0.1:8878/api/search',data=b'{"career_id":"designer","page_size":5}',headers={'Content-Type':'application/json'})
        with urlopen(request,timeout=10) as response:data=json.load(response)
        assert data['items'] and 'fit_score' in data['items'][0]
        number=data['items'][0]['number']
        request=Request('http://127.0.0.1:8878/api/analyze',data=json.dumps({'number':number,'career_id':'designer'}).encode('utf-8'),headers={'Content-Type':'application/json'})
        with urlopen(request,timeout=10) as response:result=json.load(response)
        assert result['number']==number
        print(f'OK: Both HTML entry points, 9 SVG assets, API search and analyze. Number: {number}')
    finally:
        proc.terminate(); proc.wait(timeout=8)

if __name__=='__main__':main()
