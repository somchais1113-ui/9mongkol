from pathlib import Path
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]

def test_motion_assets_are_linked_to_both_modes():
    for p in [ROOT/'index.html',ROOT/'web/index.html']:
        doc=BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser')
        assert doc.select_one('link[href*="nine-motion.css?v=0.9.2"]')
        assert doc.select_one('script[src*="nine-motion.js?v=1.0.0"]')
    doc=BeautifulSoup((ROOT/'index.html').read_text(encoding='utf-8'),'html.parser')
    scripts=[s.get('src') for s in doc.select('script[src]')]
    assert scripts.index('web/offline-data.js?v=0.7.0') < scripts.index('web/offline-bridge.js?v=0.7.0') < scripts.index('web/app.js?v=1.0.0')

def test_reduced_motion_and_text_clarity():
    css=(ROOT/'web/nine-motion.css').read_text()
    assert 'prefers-reduced-motion:reduce' in css
    assert 'nine-brand-banner' in css
    assert 'nm-motion-off' in css
    assert 'filter:blur(' not in css

def test_motion_does_not_change_numerology_rules():
    js=(ROOT/'web/nine-motion.js').read_text()
    assert '/api/' not in js
    assert 'setView(' not in js
    assert 'NI_OFFLINE_DATA' not in js
