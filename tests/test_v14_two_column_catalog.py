"""v1.4 regression: search defaults to responsive two-column catalog."""
from pathlib import Path
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]


def test_default_catalog_mode_on_both_entrypoints():
    for html in ('index.html','web/index.html'):
        soup=BeautifulSoup((ROOT/html).read_text(encoding='utf-8'),'html.parser')
        container=soup.select_one('#result-cards')
        assert container and 'is-large' not in container.get('class',[])
        assert soup.select_one('#nmk-view-grid')['aria-pressed']=='true'
        assert soup.select_one('#nmk-view-large')['aria-pressed']=='false'
        assert len([l for l in soup.select('link[rel="stylesheet"]') if 'number-card-catalog-v14.css?v=1.4.0' in l['href']])==1


def test_catalog_responsive_rules_and_dynamic_card_content():
    css=(ROOT/'web/number-card/number-card-catalog-v14.css').read_text()
    assert 'repeat(2,minmax(0,1fr))' in css
    assert 'max-width:819px' in css
    assert 'font-size:clamp(30px,9.15cqw,59px)' in css
    js=(ROOT/'web/app.js').read_text()
    assert "setCardView('grid');" in js
    assert "setCardView('large')" in js
    assert 'phone:row.number' in js and 'score:Math.round(row.fit_score)' in js and 'price:row.price' in js


def test_card_not_transformed_on_hover():
    css=(ROOT/'web/number-card/number-card-design-lock.css').read_text()
    assert '.nmk-card:hover' in css
    assert 'transform:none!important' in css
