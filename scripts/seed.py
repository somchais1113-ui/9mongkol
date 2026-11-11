"""Generate purely synthetic listings; NOT real seller stock or bookable numbers."""
import csv
import random
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT))
from app.db import initialize, add_offers

random.seed(20261111)
path=ROOT/'sample_data'/'synthetic_offers.csv'
rows=[]
nums=set()
while len(nums)<420:
    nums.add('09'+''.join(str(random.randint(0,9)) for _ in range(8)))
nums=list(sorted(nums))
for i, num in enumerate(nums):
    # Simulated catalogue statuses are not checked with any provider.
    rows.append({'number':num,'source':'DEMO — Catalogue A','price':random.choice([990,1290,1890,2490,3900,5900]),
                 'status':random.choices(['unknown','available','reserved'],weights=[6,3,1])[0],
                 'external_id':'A-'+str(i+1),'url':''})
    if i%5==0:
        rows.append({'number':num,'source':'DEMO — Catalogue B','price':random.choice([1190,1490,2790,4990]),
                     'status':'unknown','external_id':'B-'+str(i+1),'url':''})
    if i%11==0:
        rows.append({'number':num,'source':'DEMO — Catalogue C','price':random.choice([990,2990,6990]),
                     'status':'unknown','external_id':'C-'+str(i+1),'url':''})
with path.open('w',newline='',encoding='utf-8-sig') as handle:
    writer=csv.DictWriter(handle,fieldnames=['number','source','price','status','external_id','url'])
    writer.writeheader();writer.writerows(rows)
initialize()
for source in sorted({r['source'] for r in rows}):
    group=[(i+2,r) for i,r in enumerate(rows) if r['source']==source]
    result=add_offers(group,source,'demo',path.name,is_demo=True)
    print(source,result['imported'],'offers; rejected',result['rejected'])
print('Synthetic CSV:',path)
