from pathlib import Path
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]

def test_both_entrypoints_have_refinement_stylesheet():
    for name in ('index.html','web/index.html'):
        doc=BeautifulSoup((ROOT/name).read_text(encoding='utf8'),'html.parser')
        hrefs=[x.get('href','') for x in doc.select('link[rel="stylesheet"]')]
        assert sum('number-card-refinement-v13.css?v=1.3.0' in h for h in hrefs)==1

def test_v13_preserves_dynamic_data_and_removes_diffuse_score_glow():
    css=(ROOT/'web/number-card/number-card-refinement-v13.css').read_text()
    js=(ROOT/'web/app.js').read_text()
    assert '.nmk-card__score-medallion::before' in css
    assert 'content:none!important' in css
    assert 'filter:drop-shadow(0 2px 0 #98500a) drop-shadow(0 4px 0 #542105)' in css
    assert 'phone:row.number' in js
    assert 'score:Math.round(row.fit_score)' in js
    assert 'price:row.price' in js

def test_gold_laurels_are_extended_vector_assets():
    for side in ('left','right'):
        svg=BeautifulSoup((ROOT/f'web/number-card/icons/laurel-{side}.svg').read_text(), 'xml')
        assert svg.svg['viewBox']=='0 0 120 220'
        assert len(svg.select('path'))>=18

def test_all_three_requested_elements_have_responsive_sizes():
    css=(ROOT/'web/number-card/number-card-refinement-v13.css').read_text()
    for name in ('.nmk-card__phone','.nmk-card__price','.nmk-card__laurel'):
        assert name in css
    assert '@media(max-width:650px)' in css
    assert '@media(max-width:360px)' in css
