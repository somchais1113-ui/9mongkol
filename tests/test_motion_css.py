from pathlib import Path

def test_no_text_blur_in_motion_css():
    css = (Path(__file__).resolve().parent.parent / "web" / "celestial.css").read_text()
    assert "filter:blur(2px)" not in css
    assert ".hero-main h2,.hero-main p,.hero-primary-actions,.hero-small-note{filter:none!important}" in css

def test_offline_and_backend_index_versioned():
    root = Path(__file__).resolve().parent.parent
    for path in [root / "index.html", root / "web" / "index.html"]:
        assert "celestial.css?v=0.6.0" in path.read_text()
