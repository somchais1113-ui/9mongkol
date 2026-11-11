from __future__ import annotations
from contextlib import asynccontextmanager
import csv
from io import StringIO
import os
from pathlib import Path
import re
import sqlite3
from fastapi import FastAPI, File, Form, Header, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from .db import initialize, connection, metrics, add_offers, offer_detail
from .engine import analyze, normalize_number, config

BASE = Path(__file__).resolve().parent.parent
@asynccontextmanager
async def lifespan(app):
    initialize()
    config()
    yield

app = FastAPI(title='9MONGKOL — Number Intelligence Engine', version='0.8.0', docs_url='/api/docs', lifespan=lifespan)
app.mount('/assets', StaticFiles(directory=BASE/'web'), name='assets')

@app.get('/')
def home():
    return FileResponse(BASE/'web'/'index.html')

@app.get('/api/health')
def health():
    return {'ok':True,'version':'0.8.0','mode':'MVP (non-scientific interpretation)'}

@app.get('/api/meta')
def meta():
    rules, careers = config()
    return {'version':rules['version'],'career_version':careers['version'],
            'attributes':careers['attributes'],'careers':careers['careers'],
            'rules':rules['rules'],'disclaimer':rules['description']}

@app.get('/api/stats')
def stats():
    result=metrics()
    result['rules']=len(config()[0]['rules'])
    result['careers']=len(config()[1]['careers'])
    return result

class AnalysisInput(BaseModel):
    number: str = Field(min_length=1,max_length=64)
    career_id: str | None = None

@app.post('/api/analyze')
def analyze_number(payload:AnalysisInput):
    try:
        result=analyze(payload.number)
    except ValueError as exc:
        raise HTTPException(status_code=422,detail=str(exc))
    result['offers']=offer_detail(result['number'])
    if payload.career_id:
        result['selected_career']=next((c for c in result['careers'] if c['career_id']==payload.career_id), None)
    return result

class SearchInput(BaseModel):
    career_id: str = 'designer'
    query: str = Field(default='', max_length=32)
    sequence: str = Field(default='', max_length=10)
    position_pattern: str = Field(default='',max_length=10)
    required_digits: str = Field(default='', max_length=10)
    excluded_digits: str = Field(default='', max_length=10)
    source: str = Field(default='',max_length=80)
    status: str = 'all'
    min_price: int | None = Field(default=None,ge=0,le=100_000_000)
    max_price: int | None = Field(default=None,ge=0,le=100_000_000)
    sort: str = 'fit'
    page: int = Field(default=1,ge=1,le=100_000)
    page_size: int = Field(default=20,ge=1,le=50)

@app.post('/api/search')
def search(payload:SearchInput):
    valid_careers={c['id'] for c in config()[1]['careers']}
    if payload.career_id not in valid_careers:
        raise HTTPException(422,'อาชีพไม่ถูกต้อง')
    if payload.sort not in {'fit','price_low','price_high','recent'}:
        raise HTTPException(422,'รูปแบบการเรียงไม่ถูกต้อง')
    if payload.status not in {'all','available','unknown','reserved','sold','unavailable'}:
        raise HTTPException(422,'สถานะไม่ถูกต้อง')
    for field in ('query','sequence','required_digits','excluded_digits'):
        val=getattr(payload,field)
        if val and not re.fullmatch(r'[0-9]+',val):
            raise HTTPException(422,f'{field} ต้องเป็นตัวเลขเท่านั้น')
    if payload.position_pattern and not re.fullmatch(r'[0-9_]{10}',payload.position_pattern):
        raise HTTPException(422,'ตำแหน่งเลขต้องเป็นตัวเลขหรือ _ รวม 10 ตำแหน่ง')
    if payload.min_price is not None and payload.max_price is not None and payload.min_price>payload.max_price:
        raise HTTPException(422,'ราคาขั้นต่ำเกินราคาสูงสุด')
    cond=[]; args=[payload.career_id]
    if payload.position_pattern:
        cond.append('n.number LIKE ?');args.append(payload.position_pattern)
    if payload.query:
        cond.append('n.number LIKE ?'); args.append('%'+payload.query+'%')
    if payload.sequence:
        cond.append('n.core LIKE ?'); args.append('%'+payload.sequence+'%')
    for digit in set(payload.required_digits):
        cond.append('n.core LIKE ?'); args.append('%'+digit+'%')
    for digit in set(payload.excluded_digits):
        cond.append('n.core NOT LIKE ?'); args.append('%'+digit+'%')
    if payload.source:
        cond.append('o.source=?');args.append(payload.source)
    if payload.status!='all':
        cond.append('o.status=?');args.append(payload.status)
    if payload.min_price is not None:
        cond.append('o.price>=?');args.append(payload.min_price)
    if payload.max_price is not None:
        cond.append('o.price<=?');args.append(payload.max_price)
    where=' WHERE '+' AND '.join(cond) if cond else ''
    base=' FROM numbers n JOIN career_scores cs ON cs.number_id=n.id AND cs.career_id=? JOIN offers o ON o.number_id=n.id '+where
    sort={'fit':'fit_score DESC, CASE WHEN price IS NULL THEN 1 ELSE 0 END,price ASC',
          'price_low':'CASE WHEN price IS NULL THEN 1 ELSE 0 END,price ASC,fit_score DESC',
          'price_high':'CASE WHEN price IS NULL THEN 1 ELSE 0 END,price DESC,fit_score DESC',
          'recent':'last_seen DESC,fit_score DESC'}[payload.sort]
    # Use the same eligible offer pool for both totals and ranked results.
    with connection() as con:
        total=con.execute('SELECT COUNT(DISTINCT n.id) as n'+base,args).fetchone()['n']
        sql=f'''WITH eligible AS (
          SELECT n.id number_id,n.number,n.core,cs.score fit_score,o.source,o.price,o.status,o.url,o.last_seen,o.is_demo,
            COUNT(*) OVER (PARTITION BY n.id) AS offer_count,
            ROW_NUMBER() OVER (PARTITION BY n.id ORDER BY CASE o.status WHEN 'available' THEN 0 WHEN 'unknown' THEN 1 ELSE 2 END,
              CASE WHEN o.price IS NULL THEN 1 ELSE 0 END,o.price ASC,o.id ASC) AS rn
          {base}
        ) SELECT number,core,fit_score,source,price,status,url,last_seen,is_demo,offer_count FROM eligible
          WHERE rn=1 ORDER BY {sort} LIMIT ? OFFSET ?'''
        rows=[dict(row) for row in con.execute(sql,args+[payload.page_size,(payload.page-1)*payload.page_size])]
    return {'total':total,'page':payload.page,'page_size':payload.page_size,'items':rows,'career_id':payload.career_id}

class BulkPasteInput(BaseModel):
    text: str = Field(min_length=1,max_length=150_000)
    source: str = Field(min_length=2,max_length=80)
    permission_basis: str

@app.post('/api/import/text')
def import_pasted_numbers(payload:BulkPasteInput,x_admin_token:str|None=Header(default=None)):
    required_token=os.environ.get('NI_IMPORT_TOKEN','')
    if required_token and x_admin_token != required_token:
        raise HTTPException(401,'Admin token ไม่ถูกต้อง')
    if payload.permission_basis not in {'owned','partner','licensed'}:
        raise HTTPException(422,'ต้องระบุสิทธิ์ของข้อมูล: owned, partner หรือ licensed')
    # Only complete Thai mobile numbers; do not infer price/status from surrounding prose.
    pattern=re.compile(r'(?<!\d)(?:\+?66[\s.\-]*[689]|0[689])(?:[\s.\-]*\d){8}(?!\d)')
    raw=pattern.findall(payload.text)
    if not raw:
        raise HTTPException(422,'ไม่พบหมายเลขมือถือไทย 10 หลักในข้อความ')
    if len(raw)>10000:
        raise HTTPException(413,'วางเบอร์ได้สูงสุด 10,000 รายการต่อครั้ง')
    rows=[]
    for i,raw_number in enumerate(raw,start=1):
        try:
            number=normalize_number(raw_number)
        except ValueError:
            continue
        rows.append((i,{'number':number,'price':'','status':'unknown','external_id':number}))
    if not rows:
        raise HTTPException(422,'ไม่พบหมายเลขที่รองรับ')
    response=add_offers(rows,payload.source,payload.permission_basis,'bulk-paste.txt')
    response['found']=len(raw)
    response['unique_found']=len({r[1]['number'] for r in rows})
    return response

@app.post('/api/import')
async def import_csv(file:UploadFile=File(...),source:str=Form(...),permission_basis:str=Form(...),
                     x_admin_token:str|None=Header(default=None)):
    required_token=os.environ.get('NI_IMPORT_TOKEN','')
    if required_token and x_admin_token != required_token:
        raise HTTPException(401,'Admin token ไม่ถูกต้อง')
    if permission_basis not in {'owned','partner','licensed'}:
        raise HTTPException(422,'ต้องระบุสิทธิ์ของข้อมูล: owned, partner หรือ licensed')
    if not file.filename or not file.filename.lower().endswith('.csv'):
        raise HTTPException(422,'รองรับไฟล์ .csv เท่านั้น')
    contents=await file.read(10_000_001)
    if len(contents)>10_000_000:
        raise HTTPException(413,'ขนาด CSV ต้องไม่เกิน 10 MB ต่อครั้ง')
    try:
        txt=contents.decode('utf-8-sig')
    except UnicodeDecodeError:
        raise HTTPException(422,'รองรับ CSV เข้ารหัส UTF-8 เท่านั้น')
    try:
        reader=csv.DictReader(StringIO(txt))
        if not reader.fieldnames or 'number' not in reader.fieldnames:
            raise HTTPException(422,'CSV ต้องมีคอลัมน์ number')
        rows=[]
        for line,row in enumerate(reader,start=2):
            if line>100_001:
                raise HTTPException(413,'CSV เกิน 100,000 แถวต่อครั้ง')
            rows.append((line,row))
        return add_offers(rows,source,permission_basis,file.filename)
    except csv.Error as exc:
        raise HTTPException(422,f'รูปแบบ CSV ไม่ถูกต้อง: {exc}')
