from pathlib import Path
from bs4 import BeautifulSoup

ROOT=Path(__file__).resolve().parent.parent
WEB=ROOT/'web'

def test_brand_has_all_required_pages_and_assets():
    for page in [ROOT/'index.html',WEB/'index.html']:
        doc=BeautifulSoup(page.read_text(encoding='utf-8'),'html.parser')
        assert '9 มงคล' in doc.title.get_text()
        assert 'nine-mongkol.css?v=0.7.0' in str(doc)
        assert doc.select_one('.nine-brand-banner img')
        assert len(doc.select('.nine-deity-card img')) == 4
        assert doc.select_one('[data-ni-image]')
    assert (WEB/'assets/9mongkol/logo-9mongkol.png').is_file()
    assert (WEB/'assets/9mongkol/hero-group.png').is_file()
    assert (WEB/'assets/9mongkol/ganesha-hero.png').is_file()

def test_static_urls_work_in_both_modes():
    for page in [ROOT/'index.html',WEB/'index.html']:
        doc=BeautifulSoup(page.read_text(encoding='utf-8'),'html.parser')
        for item in doc.select('img[src], link[href], script[src]'):
            url=item.get('src') or item.get('href')
            if not url or url.startswith(('http:','https:','data:')):
                continue
            url=url.split('?',1)[0]
            path=(ROOT/url.lstrip('/')) if page==ROOT/'index.html' else ((WEB/url.removeprefix('/assets/')) if url.startswith('/assets/') else (WEB/url.lstrip('/')))
            assert path.is_file(),(page,item.name,url,path)


def test_nine_guide_and_original_kit():
    assert (ROOT/'brand_asset_kit/9MONGKOL_Web_Asset_Kit_v1_original.zip').is_file()
    assert '#7A0008' in (WEB/'nine-mongkol.css').read_text()
    assert '#D4AF37' in (WEB/'nine-mongkol.css').read_text()
