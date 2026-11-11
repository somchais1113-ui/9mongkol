import json
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

from app.engine import analyze, normalize_number, config
from app import db
from app.main import app


def test_normalize_thai_digits_and_country_code():
    assert normalize_number('+66 89-123-4567') == '0891234567'
    assert normalize_number('๐๘๙-๑๒๓-๔๕๖๗') == '0891234567'
    for invalid in ('123','0012345678','0891234567<script>','0891234567890'):
        with pytest.raises(ValueError):
            normalize_number(invalid)


def test_8_digit_core_and_trace():
    data=analyze('0891424567')
    assert data['core']=='91424567'
    assert len(data['pairs'])==7
    assert data['pairs'][1]=='14'
    assert data['matched_count']>0
    assert data['rulebook_version']==config()[0]['version']
    assert len(data['careers'])==len(config()[1]['careers'])
    assert all(0 <= row['score'] <= 100 for row in data['careers'])
    assert data['careers']==sorted(data['careers'],key=lambda x:(-x['score'],x['career_id']))


def test_weight_integrity():
    rules,careers=config()
    assert len({rule['pair'] for rule in rules['rules']})==len(rules['rules'])
    assert all(sum(c['weights'].values())==100 for c in careers['careers'])


def test_import_dedupe_and_api(tmp_path,monkeypatch):
    monkeypatch.setattr(db,'DB_PATH',tmp_path/'test.sqlite3')
    db.initialize()
    rows_a=[(2,{'number':'0891424567','price':'2490','status':'unknown','external_id':'A-1'}),
            (3,{'number':'0897654321','price':'3500','status':'available','external_id':'A-2'})]
    rows_b=[(2,{'number':'0891424567','price':'1990','status':'unknown','external_id':'B-1'}),
            (3,{'number':'0897654321','price':'2500','status':'unknown','external_id':'B-2'})]
    assert db.add_offers(rows_a,'Partner A','partner','a.csv')['imported']==2
    assert db.add_offers(rows_b,'Partner B','partner','b.csv')['imported']==2
    assert db.metrics()['numbers']==2
    assert db.metrics()['offers']==4
    assert len(db.offer_detail('0891424567'))==2
    # Updated duplicate offers do not create duplicate numbers or seller listings.
    assert db.add_offers([(4,{'number':'0891424567','price':'1890','status':'reserved','external_id':'A-1'})],
                         'Partner A','partner','update.csv')['imported']==1
    assert db.metrics()['offers']==4
    # Bad source listing collision must not create orphan number.
    bad=db.add_offers([(5,{'number':'0891111111','price':'3900','status':'unknown','external_id':'A-1'})],
                      'Partner A','partner','bad.csv')
    assert bad['rejected']==1
    assert db.metrics()['numbers']==2
    with TestClient(app) as client:
        result=client.post('/api/search',json={'career_id':'designer','page_size':10})
        assert result.status_code==200,result.text
        payload=result.json()
        assert payload['total']==2
        assert len(payload['items'])==2
        ana=client.post('/api/analyze',json={'number':'+66 89 142 4567'})
        assert ana.status_code==200
        assert len(ana.json()['offers'])==2
        fil=client.post('/api/search',json={'career_id':'designer','sequence':'14'})
        assert fil.status_code==200
        assert fil.json()['total']==1
        assert client.post('/api/search',json={'career_id':'nope'}).status_code==422
        paste=client.post('/api/import/text',json={'text':'089-456-1456\n+66 89 678 9123',
                           'source':'Authorized demo importer','permission_basis':'owned'})
        assert paste.status_code==200,paste.text
        assert paste.json()['imported']==2
        assert db.metrics()['numbers']==4
        assert client.post('/api/import/text',json={'text':'0891111111','source':'Unauthorized','permission_basis':'illegal'}).status_code==422
        upload=client.post('/api/import',data={'source':'Trusted CSV','permission_basis':'partner'},
                           files={'file':('in.csv',b'number,price,status,external_id\n0891122334,1500,unknown,X-1\n', 'text/csv')})
        assert upload.status_code==200,upload.text
        assert upload.json()['imported']==1
