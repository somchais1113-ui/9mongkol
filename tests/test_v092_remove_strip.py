from pathlib import Path
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]

def test_brand_banner_overlay_removed_from_both_entrypoints():
    for name in ('index.html', 'web/index.html'):
        doc=BeautifulSoup((ROOT/name).read_text(encoding='utf-8'),'html.parser')
        assert doc.select_one('.nine-brand-banner > img') is not None
        assert doc.select_one('.nine-brand-shade') is None
        assert 'PREMIUM NUMBER DISCOVERY' not in str(doc)
        assert 'ตีความอย่างมีเหตุผล · เลือกเบอร์อย่างมีข้อมูล' not in str(doc)
        assert doc.select_one('#no-legacy-banner-strip') is not None

def test_no_legacy_overlay_styles():
    for name in ('nine-mongkol.css','nine-readable.css','nine-motion.css'):
        assert '.nine-brand-shade' not in (ROOT/'web'/name).read_text(encoding='utf-8')
