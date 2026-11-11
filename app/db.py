from __future__ import annotations
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
import json
import os
import sqlite3
from .engine import analyze, config

DB_PATH = Path(os.getenv('NI_DB_PATH', Path(__file__).resolve().parent.parent / 'ni.sqlite3'))

def now_iso():
    return datetime.now(timezone.utc).isoformat(timespec='seconds')

@contextmanager
def connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB_PATH, timeout=30)
    con.row_factory = sqlite3.Row
    con.execute('PRAGMA foreign_keys = ON')
    con.execute('PRAGMA busy_timeout = 30000')
    try:
        yield con
        con.commit()
    except Exception:
        con.rollback()
        raise
    finally:
        con.close()

def initialize():
    with connection() as con:
        con.executescript('''
        PRAGMA journal_mode=WAL;
        CREATE TABLE IF NOT EXISTS numbers(
          id INTEGER PRIMARY KEY,
          number TEXT NOT NULL UNIQUE,
          core TEXT NOT NULL,
          traits_json TEXT NOT NULL,
          matches_json TEXT NOT NULL,
          rulebook_version TEXT NOT NULL,
          created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS career_scores(
          number_id INTEGER NOT NULL REFERENCES numbers(id) ON DELETE CASCADE,
          career_id TEXT NOT NULL,
          score INTEGER NOT NULL,
          PRIMARY KEY(number_id,career_id)
        );
        CREATE INDEX IF NOT EXISTS idx_career_scores_ranking ON career_scores(career_id,score DESC,number_id);
        CREATE TABLE IF NOT EXISTS offers(
          id INTEGER PRIMARY KEY,
          number_id INTEGER NOT NULL REFERENCES numbers(id) ON DELETE CASCADE,
          source TEXT NOT NULL,
          external_id TEXT NOT NULL,
          price INTEGER,
          status TEXT NOT NULL DEFAULT 'unknown',
          url TEXT,
          permission_basis TEXT NOT NULL,
          is_demo INTEGER NOT NULL DEFAULT 0,
          last_seen TEXT NOT NULL,
          UNIQUE(source,external_id)
        );
        CREATE INDEX IF NOT EXISTS idx_offers_number ON offers(number_id);
        CREATE INDEX IF NOT EXISTS idx_offers_source_status_price ON offers(source,status,price);
        CREATE TABLE IF NOT EXISTS import_logs(
          id INTEGER PRIMARY KEY,
          source TEXT NOT NULL,
          permission_basis TEXT NOT NULL,
          filename TEXT NOT NULL,
          imported INTEGER NOT NULL,
          rejected INTEGER NOT NULL,
          created_at TEXT NOT NULL
        );
        ''')

def add_offers(rows, source, permission_basis, filename, is_demo=False):
    """Insert licensed listings atomically; a phone is canonical, while sources keep separate offers."""
    if permission_basis not in {'owned','partner','licensed','demo'}:
        raise ValueError('กรุณาระบุสิทธิ์ในการใช้ข้อมูล')
    source = source.strip()
    if not 2 <= len(source) <= 80:
        raise ValueError('ชื่อแหล่งข้อมูลต้องมี 2–80 ตัวอักษร')
    errors=[]; processed=0
    with connection() as con:
        for line, r in rows:
            con.execute('SAVEPOINT import_row')
            try:
                analysis = analyze(str(r.get('number','')))
                number = analysis['number']
                raw_price = str(r.get('price','')).strip()
                price = int(raw_price.replace(',','')) if raw_price else None
                if price is not None and not (0 <= price <= 100_000_000):
                    raise ValueError('ราคานอกช่วงที่รองรับ')
                status = str(r.get('status','unknown')).strip().lower() or 'unknown'
                if status not in {'available','reserved','sold','unavailable','unknown'}:
                    raise ValueError('สถานะไม่ถูกต้อง')
                url = str(r.get('url','')).strip()
                if url and (not url.startswith(('https://','http://')) or len(url)>2000):
                    raise ValueError('URL ไม่ถูกต้อง')
                external_id = str(r.get('external_id','')).strip() or number
                if len(external_id)>200:
                    raise ValueError('external_id ยาวเกินไป')
                timestamp=now_iso()
                con.execute('INSERT OR IGNORE INTO numbers(number,core,traits_json,matches_json,rulebook_version,created_at) VALUES(?,?,?,?,?,?)',
                           (number,analysis['core'],json.dumps(analysis['trait_scores'],ensure_ascii=False),json.dumps(analysis['matched_rules'],ensure_ascii=False),analysis['rulebook_version'],timestamp))
                number_id = con.execute('SELECT id FROM numbers WHERE number=?',(number,)).fetchone()['id']
                for career in analysis['careers']:
                    con.execute('INSERT INTO career_scores(number_id,career_id,score) VALUES(?,?,?) ON CONFLICT(number_id,career_id) DO UPDATE SET score=excluded.score',
                               (number_id,career['career_id'],career['score']))
                # Do not silently replace an existing seller listing with a DIFFERENT number.
                conflicting = con.execute('SELECT number_id FROM offers WHERE source=? AND external_id=?',(source,external_id)).fetchone()
                if conflicting and conflicting['number_id'] != number_id:
                    raise ValueError('external_id ของผู้ขายซ้ำกับหมายเลขอื่น')
                con.execute('''INSERT INTO offers(number_id,source,external_id,price,status,url,permission_basis,is_demo,last_seen)
                    VALUES(?,?,?,?,?,?,?,?,?) ON CONFLICT(source,external_id) DO UPDATE SET price=excluded.price,status=excluded.status,
                    url=excluded.url,permission_basis=excluded.permission_basis,is_demo=excluded.is_demo,last_seen=excluded.last_seen''',
                    (number_id,source,external_id,price,status,url or None,permission_basis,int(is_demo),timestamp))
                processed+=1
                con.execute('RELEASE SAVEPOINT import_row')
            except (ValueError, TypeError, OverflowError, sqlite3.IntegrityError) as exc:
                con.execute('ROLLBACK TO SAVEPOINT import_row')
                con.execute('RELEASE SAVEPOINT import_row')
                errors.append({'line':line,'error':str(exc)})
        con.execute('INSERT INTO import_logs(source,permission_basis,filename,imported,rejected,created_at) VALUES(?,?,?,?,?,?)',
                    (source,permission_basis,filename,processed,len(errors),now_iso()))
    return {'imported':processed,'rejected':len(errors),'errors':errors[:15],'source':source}

def metrics():
    with connection() as con:
        number_count=con.execute('SELECT COUNT(*) AS n FROM numbers').fetchone()['n']
        offer_count=con.execute('SELECT COUNT(*) AS n FROM offers').fetchone()['n']
        available=con.execute("SELECT COUNT(*) AS n FROM offers WHERE status='available'").fetchone()['n']
        demo=con.execute('SELECT COUNT(*) AS n FROM offers WHERE is_demo=1').fetchone()['n']
        sources=[dict(row) for row in con.execute('SELECT source,COUNT(*) count FROM offers GROUP BY source ORDER BY source')]
        recent=[dict(row) for row in con.execute('SELECT source,imported,rejected,created_at FROM import_logs ORDER BY id DESC LIMIT 5')]
        return {'numbers':number_count,'offers':offer_count,'available_offers':available,'demo_offers':demo,
                'sources':sources,'recent_imports':recent}

def offer_detail(number):
    with connection() as con:
        return [dict(row) for row in con.execute('''SELECT source,price,status,url,last_seen,permission_basis,is_demo FROM offers
                JOIN numbers ON numbers.id=offers.number_id WHERE numbers.number=? ORDER BY CASE offers.status WHEN 'available' THEN 0 ELSE 1 END,price''',(number,))]

def reindex_all():
    """For controlled offline migration after edits to the rule or career JSON."""
    _,careers=config()
    with connection() as con:
        rows = con.execute('SELECT id,number FROM numbers').fetchall()
        for row in rows:
            outcome = analyze(row['number'])
            con.execute('UPDATE numbers SET traits_json=?,matches_json=?,rulebook_version=? WHERE id=?',
                        (json.dumps(outcome['trait_scores'],ensure_ascii=False),json.dumps(outcome['matched_rules'],ensure_ascii=False),outcome['rulebook_version'],row['id']))
            con.execute('DELETE FROM career_scores WHERE number_id=?',(row['id'],))
            con.executemany('INSERT INTO career_scores(number_id,career_id,score) VALUES(?,?,?)',
                            [(row['id'],c['career_id'],c['score']) for c in outcome['careers']])
    return len(rows)
