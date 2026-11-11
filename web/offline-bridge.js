/* Offline browser demo. Uses the same rulebook and seeded inventory as the FastAPI app.
   Changes in this mode are intentionally in-memory only and are NOT a backend replacement. */
(function(){
'use strict';
const snapshot = window.NI_OFFLINE_DATA;
if (!snapshot) throw new Error('ไม่พบ offline-data.js');
const meta = snapshot.meta;
const numbers = new Map(snapshot.numbers.map(row=>[row.number,row]));
const importLogs = snapshot.recent_imports.slice();
const rules = new Map(meta.rules.map(x=>[x.pair,x]));
const validCareers = new Set(meta.careers.map(x=>x.id));
const statusOrder = {available:0,unknown:1,reserved:2,sold:2,unavailable:2};
const apiError = (message,status=422)=>({error:String(message),status});
function normalize(value){
  const val=String(value??'').trim().replace(/[๐-๙]/g,ch=>String('๐๑๒๓๔๕๖๗๘๙'.indexOf(ch)));
  if (!/^[+\d\s.()\-]+$/.test(val)) throw apiError('หมายเลขมีอักขระที่ไม่รองรับ');
  let digits=val.replace(/\D/g,'');
  if (digits.startsWith('66') && digits.length===11) digits='0'+digits.slice(2);
  if (!/^0[689]\d{8}$/.test(digits)) throw apiError('รองรับเบอร์มือถือไทย 10 หลักที่ขึ้นต้นด้วย 06, 08 หรือ 09');
  return digits;
}
function analyze(input){
  const num=normalize(input),core=num.slice(2),scores=Object.fromEntries(meta.attributes.map(a=>[a.id,meta.baseline])),matches=[];
  for(let i=0;i<7;i++){
    const pair=core.slice(i,i+2),rule=rules.get(pair);
    if(!rule)continue;
    for(const [k,d] of Object.entries(rule.deltas))scores[k]+=d;
    matches.push({pair,position:i+1,theme:rule.theme,reason:rule.reason,deltas:rule.deltas});
  }
  for(const k in scores)scores[k]=Math.max(0,Math.min(100,Math.round(scores[k])));
  const careers=meta.careers.map(c=>({career_id:c.id,name:c.name,group:c.group,score:Math.round(Object.entries(c.weights).reduce((s,[k,w])=>s+scores[k]*w,0)/100)}));
  careers.sort((a,b)=>b.score-a.score||a.career_id.localeCompare(b.career_id));
  const record=numbers.get(num);
  const offers=(record?.offers||[]).map(o=>({...o})).sort((a,b)=>(a.status==='available'?0:1)-(b.status==='available'?0:1)||((a.price??Infinity)-(b.price??Infinity)));
  return {number:num,formatted:`${num.slice(0,3)}-${num.slice(3,6)}-${num.slice(6)}`,core,
    pairs:Array.from({length:7},(_,i)=>core.slice(i,i+2)),matched_rules:matches,matched_count:matches.length,
    trait_scores:scores,careers,offers,rulebook_version:meta.version,
    disclaimer:'คะแนนเชิงกฎจำลองตามความเชื่อ ไม่ใช่โอกาสสำเร็จหรือการพิสูจน์คุณสมบัติของบุคคล'};
}
function statistics(){
  const sources=new Map();let offerCount=0,available=0,demo=0;
  numbers.forEach(row=>row.offers.forEach(offer=>{
    offerCount++;
    if(offer.status==='available')available++;
    if(offer.is_demo)demo++;
    sources.set(offer.source,(sources.get(offer.source)||0)+1);
  }));
  return {numbers:numbers.size,offers:offerCount,available_offers:available,demo_offers:demo,
    sources:[...sources.entries()].map(([source,count])=>({source,count})).sort((a,b)=>a.source.localeCompare(b.source)),
    recent_imports:importLogs.slice(0,5)};
}
function search(p){
  const careerId=p.career_id||'designer';
  if(!validCareers.has(careerId))throw apiError('อาชีพไม่ถูกต้อง');
  const status=p.status||'all',sort=p.sort||'fit';
  if(!['all','available','reserved','sold','unknown','unavailable'].includes(status))throw apiError('สถานะไม่ถูกต้อง');
  if(!['fit','price_low','price_high','recent'].includes(sort))throw apiError('รูปแบบการเรียงไม่ถูกต้อง');
  const onlyDigits=['query','sequence','required_digits','excluded_digits'];
  for(const name of onlyDigits)if(p[name]&&!/^\d+$/.test(p[name]))throw apiError(name+' ต้องเป็นตัวเลขเท่านั้น');
  if(p.position_pattern&&!/^[0-9_]{10}$/.test(p.position_pattern))throw apiError('ตำแหน่งเลขต้องเป็นตัวเลขหรือ _ รวม 10 ตำแหน่ง');
  const items=[];
  for(const row of numbers.values()){
    if(p.query&&!row.number.includes(p.query))continue;
    if(p.sequence&&!row.core.includes(p.sequence))continue;
    if(p.position_pattern&&![...row.number].every((digit,i)=>p.position_pattern[i]==='_'||p.position_pattern[i]===digit))continue;
    if(p.required_digits&&![...p.required_digits].every(d=>row.core.includes(d)))continue;
    if(p.excluded_digits&&[...p.excluded_digits].some(d=>row.core.includes(d)))continue;
    const eligible=row.offers.filter(o=>(!p.source||o.source===p.source)&&(status==='all'||o.status===status)&&
      (p.min_price==null||o.price!=null&&o.price>=p.min_price)&&(p.max_price==null||o.price!=null&&o.price<=p.max_price));
    if(!eligible.length)continue;
    eligible.sort((a,b)=>(statusOrder[a.status]??2)-(statusOrder[b.status]??2)|| (a.price==null)-(b.price==null)|| (a.price??Infinity)-(b.price??Infinity));
    const selected=eligible[0];
    items.push({number:row.number,core:row.core,fit_score:row.scores[careerId]??analyze(row.number).careers.find(c=>c.career_id===careerId).score,
      source:selected.source,price:selected.price,status:selected.status,url:selected.url,last_seen:selected.last_seen,
      is_demo:selected.is_demo,offer_count:eligible.length});
  }
  const priceLow=(a,b)=>(a.price==null)-(b.price==null)||(a.price??Infinity)-(b.price??Infinity);
  const priceHigh=(a,b)=>(a.price==null)-(b.price==null)||(b.price??-Infinity)-(a.price??-Infinity);
  items.sort((a,b)=>sort==='price_low'?priceLow(a,b)||b.fit_score-a.fit_score:sort==='price_high'?priceHigh(a,b)||b.fit_score-a.fit_score:
    sort==='recent'?String(b.last_seen||'').localeCompare(String(a.last_seen||''))||b.fit_score-a.fit_score:
    b.fit_score-a.fit_score||priceLow(a,b));
  const page=Math.max(1,Number(p.page)||1),pageSize=Math.min(50,Math.max(1,Number(p.page_size)||20));
  return {total:items.length,page,page_size:pageSize,items:items.slice((page-1)*pageSize,page*pageSize),career_id:careerId};
}
function addOffers(rows,source,permission,filename){
  if(!['owned','partner','licensed'].includes(permission))throw apiError('ต้องระบุสิทธิ์ของข้อมูล');
  if(String(source||'').trim().length<2)throw apiError('กรุณาระบุชื่อแหล่งข้อมูลอย่างน้อย 2 ตัวอักษร');
  let imported=0;const errors=[];
  for(let i=0;i<rows.length;i++){
    const r=rows[i];
    try{
      const number=normalize(r.number),priceRaw=String(r.price??'').trim(),price=priceRaw?Number(priceRaw.replaceAll(',','')):null;
      if(price!==null&&(!Number.isSafeInteger(price)||price<0||price>100000000))throw apiError('ราคานอกช่วงที่รองรับ');
      const status=String(r.status||'unknown').trim().toLowerCase();
      if(!['available','unknown','reserved','sold','unavailable'].includes(status))throw apiError('สถานะไม่ถูกต้อง');
      const externalId=String(r.external_id||number),url=String(r.url||'').trim();
      if(url&&!/^https?:\/\//i.test(url))throw apiError('URL ต้องเป็น http(s)');
      let record=numbers.get(number);
      const conflict=[...numbers.values()].some(n=>n.number!==number&&n.offers.some(o=>o.source===source&&o.external_id===externalId));
      if(conflict)throw apiError('external_id ของผู้ขายซ้ำกับหมายเลขอื่น');
      if(!record){const result=analyze(number);record={number,core:number.slice(2),scores:Object.fromEntries(result.careers.map(c=>[c.career_id,c.score])),offers:[]};numbers.set(number,record)}
      const offer={source,external_id:externalId,price,status,url:url||null,last_seen:new Date().toISOString(),is_demo:0,permission_basis:permission};
      const idx=record.offers.findIndex(o=>o.source===source&&o.external_id===externalId);
      if(idx>=0)record.offers[idx]=offer;else record.offers.push(offer);
      imported++;
    }catch(e){errors.push({line:r.__line||i+2,error:e.error||e.message||String(e)})}
  }
  importLogs.unshift({source,imported,rejected:errors.length,created_at:new Date().toISOString()});
  return {imported,rejected:errors.length,errors:errors.slice(0,15),source};
}
function parseCSV(txt){
  const parsed=[];let line=[],cell='',quoted=false;
  txt=txt.replace(/^\uFEFF/,'');
  for(let i=0;i<txt.length;i++){
    const c=txt[i];
    if(c==='"'){if(quoted&&txt[i+1]==='"'){cell+='"';i++}else quoted=!quoted}
    else if(c===','&&!quoted){line.push(cell);cell=''}
    else if((c==='\n'||c==='\r')&&!quoted){if(c==='\r'&&txt[i+1]==='\n')i++;line.push(cell);if(line.some(x=>x.trim()))parsed.push(line);line=[];cell=''}
    else cell+=c;
  }
  if(quoted)throw apiError('รูปแบบ CSV ไม่ถูกต้อง: เครื่องหมายอัญประกาศไม่ครบ');
  line.push(cell);if(line.some(x=>x.trim()))parsed.push(line);
  if(!parsed.length)throw apiError('ไม่พบข้อมูล CSV');
  const names=parsed.shift().map(x=>x.trim());
  if(!names.includes('number'))throw apiError('CSV ต้องมีคอลัมน์ number');
  return parsed.map((row,i)=>Object.fromEntries([...names.map((key,j)=>[key,row[j]||'']),['__line',i+2]]));
}
async function route(path,options){
  if(path==='/api/meta')return meta;
  if(path==='/api/stats')return statistics();
  if(path==='/api/analyze'){const p=JSON.parse(options.body||'{}');const result=analyze(p.number);if(p.career_id)result.selected_career=result.careers.find(c=>c.career_id===p.career_id)||null;return result}
  if(path==='/api/search')return search(JSON.parse(options.body||'{}'));
  if(path==='/api/import/text'){
    const p=JSON.parse(options.body||'{}');const found=String(p.text||'').match(/(?<!\d)(?:\+?66[\s.\-]*[689]|0[689])(?:[\s.\-]*\d){8}(?!\d)/g)||[];
    if(!found.length)throw apiError('ไม่พบหมายเลขมือถือไทย 10 หลักในข้อความ');
    if(found.length>10000)throw apiError('วางเบอร์ได้สูงสุด 10,000 รายการต่อครั้ง',413);
    const response=addOffers(found.map((v,i)=>({number:v,__line:i+1,status:'unknown'})),p.source,p.permission_basis,'bulk-paste.txt');
    response.found=found.length;response.unique_found=new Set(found.map(v=>normalize(v))).size;
    return response;
  }
  if(path==='/api/import'){
    const form=options.body,file=form.get('file');if(!file)throw apiError('กรุณาเลือก CSV');
    if(!String(file.name||'').toLowerCase().endsWith('.csv'))throw apiError('รองรับไฟล์ .csv เท่านั้น');
    if(file.size>10000000)throw apiError('ขนาด CSV ต้องไม่เกิน 10 MB',413);
    const rows=parseCSV(await file.text());if(rows.length>100000)throw apiError('CSV เกิน 100,000 แถวต่อครั้ง',413);
    return addOffers(rows,form.get('source'),form.get('permission_basis'),file.name);
  }
  throw apiError('Endpoint นี้ไม่มีในโหมด Offline',404);
}
const originalFetch=window.fetch.bind(window);
window.fetch=async function(input,options={}){
  const path=typeof input==='string'?input:(input?.url||'');
  if(typeof path!=='string'||!path.startsWith('/api/'))return originalFetch(input,options);
  try{return new Response(JSON.stringify(await route(path,options)),{status:200,headers:{'Content-Type':'application/json'}})}
  catch(e){return new Response(JSON.stringify({detail:e.error||e.message||String(e)}),{status:e.status||422,headers:{'Content-Type':'application/json'}})}
};
})();
