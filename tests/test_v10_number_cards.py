from pathlib import Path
from bs4 import BeautifulSoup

ROOT=Path(__file__).resolve().parents[1]
WEB=ROOT/'web'

def test_card_components_are_loaded_before_app_in_both_entrypoints():
    for filepath in (ROOT/'index.html', WEB/'index.html'):
        soup=BeautifulSoup(filepath.read_text('utf-8'),'html.parser')
        assert soup.select_one('#nmk-card-css')
        assert soup.select_one('link[href*="number-card-integration.css"]')
        scripts=[x.get('src') for x in soup.select('script[src]')]
        component=next(i for i,src in enumerate(scripts) if src and 'number-card.js?v=' in src)
        app=next(i for i,src in enumerate(scripts) if src and 'app.js?v=' in src)
        assert component<app
        assert soup.select_one('#nmk-view-grid')
        assert soup.select_one('#nmk-view-large')
        assert soup.select_one('#result-cards.nmk-results')

def test_kit_files_and_all_svg_icons_are_present():
    src=WEB/'number-card'
    assert (src/'number-card.js').is_file()
    assert (src/'number-card.css').is_file()
    assert (src/'number-card-integration.css').is_file()
    assert len(list((src/'icons').glob('*.svg')))>=9
    assert (ROOT/'reference-assets'/'number-card-html-kit-v1'/'docs'/'INTEGRATION.md').is_file()

def test_search_cards_use_result_data_and_preserve_detail_action():
    app=(WEB/'app.js').read_text('utf-8')
    assert "numberCard.render(cardData,{assetBase})" in app
    for field in ('phone:row.number','score:Math.round(row.fit_score)','row.price==null', 'catalogue:row.source','status:statusText[row.status]'):
        assert field in app
    assert 'data-detail=' in app
    assert 'e.preventDefault()' in app
    assert "document.querySelectorAll('.nmk-result-slot')" in app

def test_card_is_stationary_on_hover():
    css=(WEB/'number-card'/'number-card-integration.css').read_text('utf-8')
    assert '.nmk-card:hover' in css
    assert 'transform:none!important' in css
    assert '.nmk-results.is-large' in css
    assert '@media(max-width:650px)' in css
