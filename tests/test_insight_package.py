from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent

def test_full_package_has_root_index_and_replaceable_image():
    index=(ROOT/'index.html').read_text(encoding='utf-8')
    server=(ROOT/'web'/'index.html').read_text(encoding='utf-8')
    for content in (index,server):
        assert 'ni-image-editor' in content
        assert 'ni-inventory-chart' in content
        assert 'data-ni-image' in content
        assert 'insights.js?v=0.6.0' in content
    assert (ROOT/'web'/'assets'/'number-visual.svg').is_file()
    assert (ROOT/'web'/'insights.css').is_file()

def test_report_has_explainability_components():
    script=(ROOT/'web'/'insights.js').read_text(encoding='utf-8')
    for feature in ('ni-radar','ni-career-row','ni-advice-grid','ni-trace-row','data-ni-search-pair','ni-img-zoom'):
        assert feature in script or feature in (ROOT/'web'/'index.html').read_text(encoding='utf-8')
