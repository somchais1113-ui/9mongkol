from pathlib import Path
root=Path(__file__).resolve().parents[1]

def test_readability_css_loaded_in_both_modes():
    assert 'nine-readable.css?v=0.8.0' in (root/'web/index.html').read_text('utf-8')
    assert 'web/nine-readable.css?v=0.8.0' in (root/'index.html').read_text('utf-8')

def test_readability_tokens_and_reduced_motion_remain():
    css=(root/'web/nine-readable.css').read_text('utf-8')
    assert '--nm-body:17px' in css
    assert 'font-size:16px' in css
    assert 'min-height:44px' in css
    assert 'prefers-reduced-motion:reduce' in css
    assert (root/'web/nine-motion.js').exists()
