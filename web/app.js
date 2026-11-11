'use strict';
/** UI for a deterministic, non-scientific demonstration. No real-time inventory verification. */
const $=id=>document.getElementById(id);
const state={meta:null,stats:null,view:'overview',page:1,pageSize:20,searchTotal:0,requestSerial:0,selectedCareer:'designer',importMode:'csv'};
const attrNames={communication:'การสื่อสาร',negotiation:'การเจรจา',relationships:'มนุษยสัมพันธ์',leadership:'ภาวะผู้นำ',creativity:'ความคิดสร้างสรรค์',analysis:'การวิเคราะห์'};
const statusText={available:'ผู้ขายระบุว่าพร้อมขาย',unknown:'ยังไม่ยืนยัน',reserved:'ถูกจอง',sold:'ขายแล้ว',unavailable:'ไม่พร้อมขาย'};
const money=n=>n===null||n===undefined?'ไม่ระบุ':'฿'+Number(n).toLocaleString('th-TH');
const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const fmt=n=>Number(n||0).toLocaleString('en-US');
const prettyNum=n=>n?`${n.slice(0,3)}-${n.slice(3,6)}-${n.slice(6)}`:'—';
const motionEnabled=!(window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches);
let revealObserver;
function toast(message){const node=$('toast');node.textContent=message;node.classList.add('show');clearTimeout(toast.timer);toast.timer=setTimeout(()=>node.classList.remove('show'),3700)}
function markLoadingCounters(){['metric-numbers','metric-offers','metric-careers','metric-rules'].forEach(id=>$(id)?.classList.add('loading-shimmer'))}
function animateCount(node,target,{duration=1400,suffix=''}={}){if(!node)return;node.classList.remove('loading-shimmer');const end=Number(target||0);if(!motionEnabled){node.textContent=fmt(end)+suffix;return}const start=node.dataset.counted?Number(node.dataset.value||0):0;const t0=performance.now();node.dataset.value=String(end);function frame(now){const p=Math.min((now-t0)/duration,1);const eased=1-Math.pow(1-p,3);node.textContent=fmt(Math.round(start+(end-start)*eased))+suffix;if(p<1)requestAnimationFrame(frame);else node.dataset.counted='1'}requestAnimationFrame(frame)}
function applyRevealTargets(scope=document){const selectors=['.page-heading','.hero-widget','.celestial-categories','.celestial-quote','.service-card','.stat-card','.panel','.rule-card','.career-panel','.workflow-item','.source-card','.source-row','.import-row','.search-panel','.table-toolbar','.number-card'];selectors.forEach(selector=>{scope.querySelectorAll(selector).forEach((node,index)=>{if(node.dataset.motionReady)return;node.dataset.motionReady='1';node.style.transitionDelay=`${Math.min(index*55,280)}ms`;if(revealObserver)revealObserver.observe(node);else node.classList.add('in-view')})})}
function setupRevealObserver(){if(!motionEnabled||!('IntersectionObserver' in window)){document.querySelectorAll('.page-heading,.hero-widget,.celestial-categories,.celestial-quote,.service-card,.stat-card,.panel,.rule-card,.career-panel,.workflow-item,.source-card,.source-row,.import-row,.search-panel,.table-toolbar,.number-card').forEach(n=>n.classList.add('in-view'));return}revealObserver=new IntersectionObserver(entries=>{entries.forEach(entry=>{if(entry.isIntersecting){entry.target.classList.add('in-view');revealObserver.unobserve(entry.target)}})},{threshold:.14,rootMargin:'0px 0px -8% 0px'})}
function animateResultCards(){document.querySelectorAll('.number-card').forEach((card,index)=>{card.style.transitionDelay=`${Math.min(index*45,220)}ms`;if(!motionEnabled){card.classList.add('in-view');return}requestAnimationFrame(()=>card.classList.add('in-view'))})}
function setupHeroParallax(){const hero=document.querySelector('.celestial-hero');if(!hero||!motionEnabled)return;const medallion=hero.querySelector('.celestial-medallion');const widget=hero.querySelector('.hero-widget');let raf=0;hero.addEventListener('pointermove',event=>{const rect=hero.getBoundingClientRect();const mx=(event.clientX-rect.left)/rect.width-.5;const my=(event.clientY-rect.top)/rect.height-.5;if(raf)cancelAnimationFrame(raf);raf=requestAnimationFrame(()=>{if(medallion)medallion.style.transform=`translate(${mx*10}px,${my*10-2}px)`;if(widget)widget.style.transform=`translate(${mx*-8}px,${my*-6}px)`})});hero.addEventListener('pointerleave',()=>{if(medallion)medallion.style.transform='';if(widget)widget.style.transform=''})}
async function request(path,options={}){
 const resp=await fetch(path,options);let data;
 try{data=await resp.json()}catch{data={detail:'เซิร์ฟเวอร์ส่งข้อมูลไม่ถูกต้อง'}}
 if(!resp.ok){let msg=data.detail||'ไม่สามารถประมวลผลได้';if(Array.isArray(msg))msg=msg.map(x=>x.msg).join(', ');throw new Error(String(msg))}
 return data;
}
async function postJSON(path,payload){return request(path,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)})}
function setView(view){
 if(!$("view-"+view))return;
 state.view=view;
 document.querySelectorAll('.view').forEach(n=>n.classList.toggle('active',n.id==='view-'+view));
 document.querySelectorAll('.nav-item').forEach(n=>n.classList.toggle('active',n.dataset.view===view));
 const title={overview:'Overview',explorer:'Number Explorer',analyze:'Analyze Number',careers:'Career Matrix',rules:'Rule Library',sources:'Data Sources'};
 $('breadcrumb-active').textContent=title[view]||view;
 $('sidebar').classList.remove('open');
 if(location.hash!=='#'+view)history.replaceState(null,'','#'+view);
 window.scrollTo({top:0,behavior:'instant'});
 if(view==='explorer')loadResults();
 if(view==='sources')renderSources();
}
function careerOptions(){return state.meta.careers.map(c=>`<option value="${esc(c.id)}">${esc(c.name)}</option>`).join('')}
function setupMeta(){
 const opts=careerOptions();['home-career','filter-career','analyze-career'].forEach(id=>{const node=$(id);node.innerHTML=opts;node.value=state.selectedCareer});
 $('version-text').textContent='RULEBOOK · '+state.meta.version;
 $('rules-version').textContent='RULEBOOK · '+state.meta.version;
 $('career-version').textContent='MODEL · '+state.meta.career_version;
 animateCount($('metric-careers'),state.meta.careers.length,{duration:1200});
 animateCount($('metric-rules'),state.meta.rules.length,{duration:1400});
 $('careers-total').textContent=state.meta.careers.length;
 renderCareerMatrix();renderRules();
}
async function reloadStats(){
 state.stats=await request('/api/stats');
 animateCount($('metric-numbers'),state.stats.numbers,{duration:1600});
 animateCount($('metric-offers'),state.stats.offers,{duration:1700});
 const source=$('filter-source');const existing=source.value;
 source.innerHTML='<option value="">ทุกแหล่ง</option>'+state.stats.sources.map(x=>`<option value="${esc(x.source)}">${esc(x.source)} (${x.count})</option>`).join('');
 if([...source.options].some(x=>x.value===existing))source.value=existing;
 renderSources();applyRevealTargets(document);window.NIInsights?.renderInventoryStats(state.stats);
}
function renderSources(){if(!state.stats)return;
 $('sources-list').innerHTML=state.stats.sources.length?state.stats.sources.map(s=>`<div class="source-row"><div><strong>${esc(s.source)}</strong><p>${s.source.startsWith('DEMO')?'ข้อมูลสังเคราะห์เพื่อทดสอบ':'รายการจากการนำเข้า CSV'}</p></div><span>${fmt(s.count)} offers</span></div>`).join(''):'<p>ยังไม่มีข้อมูล กรุณานำเข้า CSV</p>';
 $('imports-list').innerHTML=state.stats.recent_imports.length?state.stats.recent_imports.map(s=>`<div class="import-row"><div><strong>${esc(s.source)}</strong><p>${esc(s.created_at.replace('T',' ').slice(0,16))} UTC</p></div><span>+${fmt(s.imported)} / rejected ${fmt(s.rejected)}</span></div>`).join(''):'<p>ยังไม่มีประวัติการนำเข้า</p>';
}
function filterValues(){const input=id=>$(id).value.trim();const slots=[...document.querySelectorAll('.position-slot')];const mask=slots.map(i=>i.value.replace(/[^0-9]/g,'')||'_').join('');return {position_pattern:mask.slice(1).replace(/_/g,'')?mask:'',career_id:input('filter-career'),query:input('filter-query').replace(/[\s-]/g,''),sequence:input('filter-sequence'),required_digits:input('filter-required'),excluded_digits:input('filter-excluded'),source:input('filter-source'),status:input('filter-status'),max_price:input('filter-budget')===''?null:Number(input('filter-budget')),sort:input('filter-sort'),page:state.page,page_size:state.pageSize}}
async function loadResults(){
 const serial=++state.requestSerial;
 $('result-body').innerHTML='<tr><td colspan="6" class="empty-row">กำลังประมวลผลและจัดอันดับ...</td></tr>';
 $('result-cards').innerHTML='<div class="empty-results loading-shimmer">กำลังโหลดผลลัพธ์...</div>';
 try{
  const res=await postJSON('/api/search',filterValues());if(serial!==state.requestSerial)return;
  state.searchTotal=res.total;
  $('results-total').textContent=fmt(res.total);
  $('page-number').textContent=res.page;
  $('page-prev').disabled=res.page<=1;
  $('page-next').disabled=res.page*res.page_size>=res.total;
  $('page-summary').textContent=res.total?`แสดง ${fmt((res.page-1)*res.page_size+1)}–${fmt(Math.min(res.page*res.page_size,res.total))} จาก ${fmt(res.total)} เบอร์`:'ไม่มีผลลัพธ์';
  const currentCareer=state.meta.careers.find(c=>c.id===$('filter-career').value)?.name||'อาชีพที่เลือก';
  $('result-cards').innerHTML=res.items.length?res.items.map((row,index)=>`<article class="number-card">
    <div class="number-card-top"><span class="number-card-kicker">NUMBER / ${String((res.page-1)*res.page_size+index+1).padStart(3,'0')}</span><span class="number-card-status ${esc(row.status)}">${esc(statusText[row.status]||'ไม่ทราบสถานะ')}</span></div>
    <div class="number-card-number">${prettyNum(row.number)}</div>
    <div class="number-card-career">ความสอดคล้องกับ <b>${esc(currentCareer)}</b></div>
    <div class="number-card-fit"><span>Career Fit Index · คะแนนสาธิต</span><strong>${Math.round(row.fit_score)}<small>/100</small></strong></div>
    <div class="number-card-foot"><div><div class="number-card-price">${money(row.price)}</div><div class="number-card-supplier">${esc(row.source)} · ${row.offer_count} แหล่งเสนอขาย${row.is_demo?' · DEMO':''}</div></div><button type="button" data-detail="${esc(row.number)}">ดูรายละเอียด ↗</button></div>
  </article>`).join(''):'<div class="empty-results">ไม่พบหมายเลขตรงเงื่อนไข ลองปรับการเลือกตัวเลข หรือ Import เบอร์จากแหล่งข้อมูลที่ได้รับอนุญาต</div>';
  $('result-body').innerHTML=res.items.length?res.items.map(row=>`<tr><td><button class="phone-link" data-detail="${esc(row.number)}">${prettyNum(row.number)}</button><div class="subline">${row.is_demo?'DEMO / SYNTHETIC':'IMPORTED'}</div></td><td><div class="fit-score"><strong>${row.fit_score}<span style="font-size:10px;color:#799b8b">/100</span></strong><span class="mini-track"><span style="width:${row.fit_score}%"></span></span></div></td><td><strong>${money(row.price)}</strong><div class="subline">${esc(row.source)}</div></td><td><span class="status-label ${esc(row.status)}">${statusText[row.status]||'ไม่ทราบสถานะ'}</span></td><td><strong>${row.offer_count}</strong><div class="subline">seller listing(s)</div></td><td><button class="view-button" data-detail="${esc(row.number)}">View detail ↗</button></td></tr>`).join(''):'<tr><td colspan="6" class="empty-row">ไม่พบหมายเลขตรงเงื่อนไข ลองปรับตัวกรอง หรือ Import CSV เพิ่ม</td></tr>';
  applyRevealTargets($('view-explorer'));animateResultCards();
 }catch(e){if(serial===state.requestSerial){$('result-body').innerHTML=`<tr><td colspan="6" class="empty-row">${esc(e.message)}</td></tr>`;$('result-cards').innerHTML=`<div class="empty-results">${esc(e.message)}</div>`;toast(e.message)}}
}
function renderCareerMatrix(){
 const attrs=state.meta.attributes;
 $('matrix-table').querySelector('thead').innerHTML='<tr><th>CAREER / ROLE</th>'+attrs.map(a=>`<th title="${esc(a.description)}">${esc(a.name)}</th>`).join('')+'</tr>';
 $('matrix-table').querySelector('tbody').innerHTML=state.meta.careers.map(c=>'<tr><td>'+esc(c.name)+'<div class="subline">'+esc(c.group)+'</div></td>'+attrs.map(a=>{let v=c.weights[a.id]||0;return `<td class="weight ${v>=30?'strong':v>=20?'mid':''}">${v}%</td>`}).join('')+'</tr>').join('');
}
function rulePositive(rule){return Object.values(rule.deltas).reduce((a,b)=>a+b,0)>=0}
function renderRules(){const q=$('rule-query').value.trim().toLowerCase();const polarity=$('rule-polarity').value;
 const arr=state.meta.rules.filter(r=>(!q||r.pair.includes(q)||r.theme.toLowerCase().includes(q))&&(polarity==='all'||(polarity==='positive')===rulePositive(r)));
 $('rule-grid').innerHTML=arr.length?arr.map(r=>`<article class="rule-card"><div class="rule-card-top"><span class="rule-pair">${r.pair}</span><span class="rule-type ${rulePositive(r)?'':'negative'}">${rulePositive(r)?'POSITIVE':'CAUTION'}</span></div><h4>${esc(r.theme)}</h4><p>${esc(r.reason)}</p><div class="rule-deltas">${Object.entries(r.deltas).map(([k,v])=>`<span class="${v<0?'negative':''}">${esc(attrNames[k])} ${v>0?'+':''}${v}</span>`).join('')}</div></article>`).join(''):'<p>ไม่พบกฎที่ค้นหา</p>';
}
function scoreRow(label,value){return `<div class="score-row"><span>${esc(label)}</span><div class="score-track"><i style="width:${value}%"></i></div><b>${value}</b></div>`}
function renderAnalysisLegacy(res,containerId){
 const score=Math.round(res.careers.find(c=>c.career_id===$('analyze-career').value)?.score??res.careers[0]?.score??50);
 const selectedName=state.meta.careers.find(c=>c.id===$('analyze-career').value)?.name||'Top Career';
 const traits=state.meta.attributes.map(a=>scoreRow(a.name,res.trait_scores[a.id])).join('');
 const careerRank=res.careers.slice(0,6).map((c,i)=>`<div class="score-row"><span>${i+1}. ${esc(c.name)}</span><div class="score-track"><i style="width:${c.score}%"></i></div><b>${c.score}</b></div>`).join('');
 const pairs=res.pairs.map((p,i)=>`<span class="pair-tag ${res.matched_rules.some(m=>m.position===i+1)?'matched':''}" title="ตำแหน่ง ${i+1}">${p}</span>`).join('');
 const traces=res.matched_rules.length?res.matched_rules.map(r=>`<div class="trace-item"><span class="trace-code">${r.pair}</span><div><strong>${esc(r.theme)} · position ${r.position}</strong><p>${esc(r.reason)}</p><div>${Object.entries(r.deltas).map(([k,v])=>`<span class="delta-chip ${v<0?'minus':''}">${esc(attrNames[k])} ${v>0?'+':''}${v}</span>`).join('')}</div></div></div>`).join(''):'<p style="color:#8b9dab;font-size:12px">ไม่พบคู่เลขที่กำหนดไว้ในกฎสาธิต คะแนนแต่ละด้านจึงเริ่มจาก Baseline 50</p>';
 const offers=res.offers.length?res.offers.map(o=>`<div class="detail-offer-row"><div><strong>${esc(o.source)} ${o.is_demo?'· DEMO':''}</strong><small>${statusText[o.status]} · อัปเดต ${esc(o.last_seen.slice(0,10))}</small></div><div style="text-align:right"><div class="price">${money(o.price)}</div>${o.url?`<a href="${esc(o.url)}" target="_blank" rel="noopener noreferrer">ดูประกาศ ↗</a>`:''}</div></div>`).join(''):'<p style="font-size:11px;color:#8295a0">ไม่พบรายการจากผู้ขาย — นี่อาจเป็นเบอร์ที่ผู้ใช้กรอกเอง</p>';
 return `<div class="detail-summary"><div><div class="section-kicker">ANALYZED PHONE</div><div class="detail-number">${esc(res.formatted)}</div><div class="detail-note">8-digit core: ${esc(res.core)} · ${res.matched_count} matched rules · ${esc(res.rulebook_version)}</div></div><div class="detail-score">${score}<small>${esc(selectedName)} / 100</small></div></div>
 <div class="detail-section"><h3>Adjacent pairs — ซ้อนทับต่อเนื่อง 7 คู่</h3><div class="pair-list">${pairs}</div></div>
 <div class="detail-section"><h3>Attribute interpretation · Baseline 50</h3>${traits}</div>
 <div class="detail-section"><h3>Top career matches</h3>${careerRank}</div>
 <div class="detail-section"><h3>Explainable rule trace (${res.matched_rules.length})</h3>${traces}</div>
 <div class="detail-section"><h3>Seller offers (${res.offers.length})</h3>${offers}</div>
 <div class="detail-disclaimer">${esc(res.disclaimer)} · คะแนนไม่ใช่เปอร์เซ็นต์ความสำเร็จจริง และสถานะสินค้ายังไม่ได้ยืนยันแบบเรียลไทม์</div>`;
}
function renderAnalysis(res){return window.NIInsights?window.NIInsights.report(res,{careerId:$('analyze-career').value,meta:state.meta}):renderAnalysisLegacy(res)}
async function runAnalyze(number,careerId,detail=false){
 try{const res=await postJSON('/api/analyze',{number,career_id:careerId});
 if(detail){$('detail-content').innerHTML=renderAnalysis(res);$('detail-modal').hidden=false;document.body.style.overflow='hidden';applyRevealTargets($('detail-content'));window.NIInsights?.syncImages()}
 else{$('analysis-output').hidden=false;$('analysis-output').innerHTML=`<article class="panel" style="margin-top:19px">${renderAnalysis(res)}</article>`;$('analysis-placeholder').hidden=true;applyRevealTargets($('analysis-output'));window.NIInsights?.syncImages();toast('วิเคราะห์หมายเลขเรียบร้อยแล้ว')}
 }catch(e){toast(e.message)}
}
function closeModal(id){$(id).hidden=true;if($('import-modal').hidden && $('detail-modal').hidden)document.body.style.overflow=''}
function setImportMode(mode){
 state.importMode=mode;
 $('import-tab-csv').classList.toggle('active',mode==='csv');
 $('import-tab-paste').classList.toggle('active',mode==='paste');
 $('csv-input-field').hidden=mode!=='csv';
 $('paste-input-field').hidden=mode!=='paste';
 $('import-file').required=mode==='csv';
 $('import-paste').required=mode==='paste';
 $('import-subtitle').textContent=mode==='csv'?'นำเข้าเบอร์จากไฟล์ CSV ที่คุณมีสิทธิ์ใช้งาน รองรับสูงสุด 100,000 แถวและ 10 MB ต่อครั้ง':'วางรายชื่อเบอร์จำนวนมากที่คุณมีสิทธิ์ใช้งาน ระบบจะดึงเลขมือถือที่ครบ 10 หลักให้อัตโนมัติ (สูงสุด 10,000 รายการ)';
 $('import-result').hidden=true;
}
function openImport(mode='csv'){closeModal('detail-modal');setImportMode(mode);$('import-modal').hidden=false;$('import-result').hidden=true;document.body.style.overflow='hidden'}
async function runImport(e){e.preventDefault();if(!$('import-ack').checked){toast('กรุณายืนยันสิทธิ์ในการใช้ข้อมูล');return}
 const btn=$('import-submit');btn.disabled=true;btn.textContent='Importing...';
 try{const headers={};if($('import-token').value)headers['X-Admin-Token']=$('import-token').value;
  let result;
  if(state.importMode==='paste'){
    if(!$('import-paste').value.trim())throw new Error('กรุณาวางหมายเลขโทรศัพท์');
    result=await request('/api/import/text',{method:'POST',headers:{...headers,'Content-Type':'application/json'},body:JSON.stringify({text:$('import-paste').value,source:$('import-source').value.trim(),permission_basis:$('import-permission').value})});
  }else{
    const data=new FormData();data.append('file',$('import-file').files[0]);data.append('source',$('import-source').value.trim());data.append('permission_basis',$('import-permission').value);
    result=await request('/api/import',{method:'POST',body:data,headers});
  }
  $('import-result').hidden=false;
  $('import-result').innerHTML=`นำเข้าสำเร็จ <strong>${fmt(result.imported)}</strong> รายการ · ปฏิเสธ <strong>${fmt(result.rejected)}</strong> รายการ${result.errors.length?'<div style="margin-top:5px">ตัวอย่างข้อผิดพลาด: '+result.errors.map(x=>`บรรทัด ${x.line}: ${esc(x.error)}`).join(' / ')+'</div>':''}`;
  await reloadStats();if(state.view==='explorer')loadResults();toast('Import CSV เสร็จสิ้น');
 }catch(err){toast(err.message)}finally{btn.disabled=false;btn.textContent='Import & analyze →'}
}
function renderDigitKeypads(){
 for(const [target,inputId,excluded] of [['keypad-required','filter-required',false],['keypad-excluded','filter-excluded',true]]){
  const node=$(target);
  node.innerHTML=Array.from({length:10},(_,i)=>`<button type="button" class="digit-key ${excluded?'excluded':''}" aria-label="เลข ${i}" aria-pressed="false" data-digit="${i}" data-target="${inputId}">${i}</button>`).join('');
  node.addEventListener('click',event=>{const btn=event.target.closest('button[data-digit]');if(!btn)return;const input=$(inputId);let value=input.value.replace(/[^0-9]/g,'');const digit=btn.dataset.digit;value=value.includes(digit)?value.replaceAll(digit,''):value+digit;input.value=value.slice(0,8);updateDigitButtons();state.page=1;loadResults()});
  $(inputId).addEventListener('input',()=>{const input=$(inputId);input.value=input.value.replace(/[^0-9]/g,'');updateDigitButtons()});
 }
 updateDigitButtons();
}
function updateDigitButtons(){for(const btn of document.querySelectorAll('.digit-key')){const selected=$(btn.dataset.target).value.includes(btn.dataset.digit);btn.classList.toggle('selected',selected);btn.setAttribute('aria-pressed',String(selected))}}
function buildPositionInputs(){
 const target=$('position-grid');
 target.innerHTML=Array.from({length:10},(_,i)=>`<input class="position-slot" maxlength="1" inputmode="numeric" pattern="[0-9]" aria-label="ตำแหน่งเลข ${i+1}" title="ตำแหน่งที่ ${i+1}" ${i===0?'value="0" disabled':''} placeholder="${i===0?'0':'–'}" />`).join('');
 target.addEventListener('input',e=>{const input=e.target;if(!input.classList.contains('position-slot'))return;input.value=input.value.replace(/[^0-9]/g,'').slice(-1);if(input.value){const next=input.nextElementSibling;if(next)next.focus()}});
 target.addEventListener('keydown',e=>{if(!e.target.classList.contains('position-slot'))return;if(e.key==='Backspace'&&!e.target.value){const prev=e.target.previousElementSibling;if(prev&&!prev.disabled)prev.focus()}});
 $('clear-position').addEventListener('click',()=>{target.querySelectorAll('input:not(:disabled)').forEach(n=>n.value='');state.page=1;loadResults()});
}
function bindUI(){
 setupRevealObserver();applyRevealTargets(document);setupHeroParallax();window.NIInsights?.bindImageEditor();
 document.querySelectorAll('[data-view]').forEach(b=>b.addEventListener('click',()=>setView(b.dataset.view)));
 document.querySelectorAll('[data-jump]').forEach(b=>b.addEventListener('click',()=>setView(b.dataset.jump)));
 $('mobile-menu').addEventListener('click',()=> $('sidebar').classList.toggle('open'));
 renderDigitKeypads();buildPositionInputs();
 $('hero-analyze-form').addEventListener('submit',e=>{e.preventDefault();const number=$('hero-analyze-number').value;$('analyze-number').value=number;setView('analyze');runAnalyze(number,$('analyze-career').value)});
 $('result-cards').addEventListener('click',e=>{const b=e.target.closest('[data-detail]');if(b){$('analyze-career').value=$('filter-career').value;runAnalyze(b.dataset.detail,$('filter-career').value,true)}});
 $('quick-search').addEventListener('click',()=>{state.selectedCareer=$('home-career').value;$('filter-career').value=state.selectedCareer;$('analyze-career').value=state.selectedCareer;$('filter-budget').value=$('home-budget').value;state.page=1;setView('explorer')});
 $('filter-apply').addEventListener('click',()=>{state.page=1;loadResults()});
 $('filter-reset').addEventListener('click',()=>{['filter-query','filter-sequence','filter-required','filter-excluded','filter-budget'].forEach(id=>$(id).value='');document.querySelectorAll('.position-slot:not(:disabled)').forEach(n=>n.value='');updateDigitButtons();$('filter-source').value='';$('filter-status').value='all';$('filter-sort').value='fit';state.page=1;loadResults()});
 $('filter-career').addEventListener('change',()=>{state.selectedCareer=$('filter-career').value;$('home-career').value=state.selectedCareer;$('analyze-career').value=state.selectedCareer;state.page=1;loadResults()});
 $('filter-sort').addEventListener('change',()=>{state.page=1;loadResults()});
 $('page-prev').addEventListener('click',()=>{if(state.page>1){state.page--;loadResults()}});
 $('page-next').addEventListener('click',()=>{if(state.page*state.pageSize<state.searchTotal){state.page++;loadResults()}});
 ['filter-query','filter-sequence','filter-required','filter-excluded','filter-budget'].forEach(id=>$(id).addEventListener('keydown',e=>{if(e.key==='Enter'){state.page=1;loadResults()}}));
 $('result-body').addEventListener('click',e=>{const btn=e.target.closest('[data-detail]');if(btn){$('analyze-career').value=$('filter-career').value;runAnalyze(btn.dataset.detail,$('filter-career').value,true)}});
 $('analyzer-form').addEventListener('submit',e=>{e.preventDefault();runAnalyze($('analyze-number').value,$('analyze-career').value)});
 ['rule-query','rule-polarity'].forEach(id=>$(id).addEventListener('input',renderRules));
 ['header-import','explorer-import','sources-import'].forEach(id=>$(id).addEventListener('click',()=>openImport('csv')));
 ['explorer-paste','sources-paste'].forEach(id=>$(id).addEventListener('click',()=>openImport('paste')));
 $('import-tab-csv').addEventListener('click',()=>setImportMode('csv'));
 $('import-tab-paste').addEventListener('click',()=>setImportMode('paste'));
 ['import-close','import-cancel'].forEach(id=>$(id).addEventListener('click',()=>closeModal('import-modal')));
 $('detail-close').addEventListener('click',()=>closeModal('detail-modal'));
 $('import-form').addEventListener('submit',runImport);
 document.querySelectorAll('.modal-backdrop').forEach(back=>back.addEventListener('click',e=>{if(e.target===back)closeModal(back.id)}));
 document.addEventListener('keydown',e=>{if(e.key==='Escape'){closeModal('import-modal');closeModal('detail-modal')}});
 window.addEventListener('hashchange',()=>{const requested=location.hash.slice(1);if(requested&&requested!==state.view)setView(requested)})
}
(async function init(){try{
 markLoadingCounters();
 const [meta]=await Promise.all([request('/api/meta')]);state.meta=meta;setupMeta();bindUI();await reloadStats();setView(location.hash.slice(1)||'overview');applyRevealTargets(document);
}catch(e){$('global-message').hidden=false;$('global-message').textContent='ไม่สามารถเชื่อมต่อ Engine ได้: '+e.message+' — กรุณารันเซิร์ฟเวอร์ตาม README';}})();
