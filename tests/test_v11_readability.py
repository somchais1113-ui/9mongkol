from pathlib import Path
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]

def test_both_entrypoints_use_v12_card_assets():
    for entry in ('index.html','web/index.html'):
        soup=BeautifulSoup((ROOT/entry).read_text('utf-8'),'html.parser')
        srcs=[x['src'] for x in soup.select('script[src]')]
        hrefs=[x['href'] for x in soup.select('link[rel="stylesheet"]')]
        assert any('number-card.js?v=1.2.0' in s for s in srcs)
        assert any('number-card-integration.css?v=1.2.0' in x for x in hrefs)

def test_phone_is_grouped_for_scannability_and_accessibility():
    js=(ROOT/'web/number-card/number-card.js').read_text('utf-8')
    assert 'phoneMarkup(d.phone)' in js
    assert 'digits.slice(0,3)' in js and 'digits.slice(3,6)' in js
    assert 'nmk-card__phone-group' in js and 'nmk-card__phone-dash' in js
    assert 'aria-label="หมายเลขโทรศัพท์' in js

def test_score_presentation_separates_numerator_and_denominator():
    js=(ROOT/'web/number-card/number-card.js').read_text('utf-8')
    css=(ROOT/'web/number-card/number-card-integration.css').read_text('utf-8')
    assert 'nmk-card__score-number' in js and 'nmk-card__score-total' in js
    assert 'คะแนนความสอดคล้อง ${score} จาก ${totalScore}' in js
    assert '.nmk-card__score' in css and 'gap:12px' in css
    assert 'transform:none!important' in css
