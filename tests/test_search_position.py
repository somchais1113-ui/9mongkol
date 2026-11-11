"""Search mask regression tests. Uses isolated SQLite; never mutates bundled demo data."""
from fastapi.testclient import TestClient
from app import db
from app.main import app


def test_position_pattern_is_an_exact_10_digit_phone_mask(monkeypatch, tmp_path):
    monkeypatch.setattr(db, 'DB_PATH', tmp_path / 'test.sqlite3')
    with TestClient(app) as client:
        db.add_offers([
            (2, {'number': '0891234567', 'status': 'unknown', 'price': '1200'}),
            (3, {'number': '0867654321', 'status': 'unknown', 'price': '2400'}),
        ], source='TEST', permission_basis='demo', filename='test.csv', is_demo=True)
        base = client.post('/api/search', json={'career_id': 'designer'}).json()
        assert base['total'] == 2
        filtered = client.post('/api/search', json={
            'career_id': 'designer', 'position_pattern': '089_______'
        }).json()
        assert filtered['total'] == 1
        assert filtered['items'][0]['number'] == '0891234567'
        filtered = client.post('/api/search', json={
            'career_id': 'designer', 'position_pattern': '08__6_____'
        }).json()
        assert filtered['total'] == 1
        assert filtered['items'][0]['number'] == '0867654321'
        for invalid in ['0_/%______', '089___', '089_______%', '089_______ OR 1=1']:
            response = client.post('/api/search', json={
                'career_id': 'designer', 'position_pattern': invalid
            })
            assert response.status_code == 422
