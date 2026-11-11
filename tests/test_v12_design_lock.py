from pathlib import Path
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]

def test_both_entrypoints_load_design_lock():
    for file in (ROOT/'index.html',ROOT/'web/index.html'):
        doc=BeautifulSoup(file.read_text(encoding='utf-8'),'html.parser')
        sheets=[s.get('href','') for s in doc.select('link[rel="stylesheet"]')]
        assert any('number-card-design-lock.css?v=1.2.0' in s for s in sheets)
        scripts=[s.get('src','') for s in doc.select('script[src]')]
        assert any('number-card.js?v=1.2.0' in s for s in scripts)

def test_glow_is_css_and_data_remain_dynamic():
    css=(ROOT/'web/number-card/number-card-design-lock.css').read_text()
    app=(ROOT/'web/app.js').read_text()
    for key in ('nmk-card__phone','nmk-card__score-number','nmk-card__scorebar','nmk-card__cta','nmk-card__price'):
        assert key in css
    assert 'background-clip:text' in css
    assert 'transform:none!important' in css
    assert 'phone:row.number' in app
    assert 'score:Math.round(row.fit_score)' in app
    assert "catalogue:row.source" in app
    assert "numberCard.render(cardData,{assetBase})" in app

def test_phone_dash_and_accessibility():
    js=(ROOT/'web/number-card/number-card.js').read_text()
    assert 'nmk-card__phone-dash' in js
    assert 'nmk-card__score-number' in js
    assert 'nmk-card__score-total' in js
    assert 'aria-label="หมายเลขโทรศัพท์' in js
