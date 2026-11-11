from pathlib import Path
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parent.parent
A=ROOT/'web/assets/9mongkol'

def test_new_lotus_logo_exists_and_is_used():
    assert (A/'logo-9mongkol-lotus-original.png').is_file()
    assert (A/'logo-9mongkol-lotus.webp').is_file()
    assert (A/'favicon-9mongkol-lotus.png').is_file()
    for page in (ROOT/'index.html',ROOT/'web/index.html'):
        soup=BeautifulSoup(page.read_text(encoding='utf-8'),'html.parser')
        assert 'lotus.webp' in soup.select_one('.nine-nav-logo')['src']
        assert 'lotus.webp' in soup.select_one('.nine-hero-badge')['src']
        assert 'lotus.webp' in soup.select_one('.nine-footer-logo')['src']
        assert 'favicon-9mongkol-lotus.png' in soup.select_one('link[rel=icon]')['href']
        assert soup.select_one('.nine-nav-copy') is None

def test_polish_loaded_in_both_modes():
    for p in (ROOT/'web/index.html',ROOT/'index.html'):
        src=p.read_text(encoding='utf-8')
        assert 'nine-polish.css?v=0.9.0' in src
        if p==ROOT/'index.html':assert 'web/nine-polish.css?v=0.9.0' in src
        else:assert '/assets/nine-polish.css?v=0.9.0' in src
    css=(ROOT/'web/nine-polish.css').read_text(encoding='utf-8')
    assert 'transform:none!important' in css
    assert 'nine-brand-shade' in css
    assert 'scale:1!important' in css
    js=(ROOT/'web/app.js').read_text(encoding='utf-8')
    assert 'setupHeroParallax();window.NIInsights?.bindImageEditor()' not in js
