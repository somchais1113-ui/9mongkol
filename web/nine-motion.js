/* 9 มงคล — Sacred Luxury motion controls. Decorative only, no scoring changes. */
(()=>{
'use strict';
const media=window.matchMedia?.('(prefers-reduced-motion: reduce)');
const KEY='nine-mongkol-motion-v07';
let userOff=false;try{userOff=localStorage.getItem(KEY)==='off'}catch{}
const isOff=()=>userOff||!!media?.matches;
const save=()=>{try{localStorage.setItem(KEY,userOff?'off':'on')}catch{}};
const toggle=document.createElement('button');toggle.type='button';toggle.id='nine-motion-toggle';toggle.className='nm-motion-toggle';
toggle.setAttribute('aria-label','เปิดหรือปิดเอฟเฟกต์การเคลื่อนไหว');toggle.title='เปิดหรือปิดเอฟเฟกต์การเคลื่อนไหว';
const icon=document.createElement('span');icon.className='nm-toggle-icon';icon.setAttribute('aria-hidden','true');
const label=document.createElement('span');label.className='nm-toggle-label';toggle.append(icon,label);
function renderSetting(){const off=isOff();document.body.classList.toggle('nm-motion-off',off);toggle.setAttribute('aria-pressed',String(!off));icon.textContent=off?'◌':'✦';label.textContent=off?'เปิดเอฟเฟกต์':'ลดเอฟเฟกต์';toggle.disabled=!!media?.matches;toggle.title=media?.matches?'ลดการเคลื่อนไหวตามการตั้งค่าของอุปกรณ์':toggle.textContent}
toggle.addEventListener('click',()=>{userOff=!userOff;save();renderSetting()});
media?.addEventListener?.('change',renderSetting);
const actions=document.querySelector('.topbar-actions');if(actions)actions.prepend(toggle);renderSetting();
document.addEventListener('visibilitychange',()=>document.body.classList.toggle('nm-paused',document.hidden));
// Static deterministic positions: no image requests, no canvas and no background polling.
const points=[[12,16,3,8.4,0],[78,15,2,7.1,-2],[29,71,3,9.7,-3],[85,64,2,8.5,-1],[19,41,2,10.5,-5],[54,14,3,9.2,-4],[67,84,3,8.8,-6],[45,56,2,10.3,-2],[92,37,2,9.9,-8],[10,86,3,8.0,-5],[63,33,2,10.1,-7],[36,24,2,11.2,-3]];
for(const selector of ['.hero-main','.hero-widget']){
 const host=document.querySelector(selector);if(!host)continue;
 const dust=document.createElement('div');dust.className='nm-dust';dust.setAttribute('aria-hidden','true');
 points.forEach(([x,y,s,d,delay],index)=>{if(selector==='.hero-widget'&&index>6)return;const p=document.createElement('i');p.style.cssText=`--x:${x}%;--y:${y}%;--s:${s}px;--d:${d}s;--delay:${delay}s`;dust.appendChild(p)});
 host.prepend(dust);
}
// Observers trigger finite reveal animations. Content is visible without JavaScript or observers.
const entryIO=(!isOff()&&'IntersectionObserver'in window)?new IntersectionObserver(entries=>{for(const e of entries){if(e.isIntersecting){e.target.classList.add('nm-visible');entryIO.unobserve(e.target)}}},{threshold:.13,rootMargin:'0px 0px -6% 0px'}):null;
function markSections(){document.querySelectorAll('.view.active .service-card,.view.active .nine-deity-card,.view.active .stat-card,.view.active .nine-gallery-heading,.view.active .section-heading,.view.active .nine-quote,.view.active .workflow-item').forEach((el,i)=>{if(el.dataset.nmSeen)return;el.dataset.nmSeen='1';el.classList.add('nm-reveal');el.style.setProperty('--nm-delay',`${Math.min(i%4*80,240)}ms`);if(entryIO)entryIO.observe(el)})}
const watchView=new MutationObserver(()=>markSections());document.querySelectorAll('.view').forEach(v=>watchView.observe(v,{attributes:true,attributeFilter:['class']}));markSections();
function animateChildren(host,selector,classname){if(!host)return;const children=[...host.querySelectorAll(selector)];children.forEach((node,i)=>{node.classList.remove(classname);node.style.setProperty('--nm-delay',`${Math.min(i*55,320)}ms`);if(!isOff()){void node.offsetWidth;node.classList.add(classname)}})}
const cards=document.getElementById('result-cards');if(cards){const obs=new MutationObserver(()=>animateChildren(cards,'.number-card','nm-result-arrive'));obs.observe(cards,{childList:true});}
function animateReport(root){if(!root)return;root.querySelectorAll('.ni-report').forEach(report=>{report.classList.remove('nm-report-ready');if(isOff())return;report.querySelectorAll('.ni-report-card,.ni-advice,.ni-career-row').forEach((c,i)=>c.style.setProperty('--nm-delay',`${Math.min(100+i*70,480)}ms`));void report.offsetWidth;report.classList.add('nm-report-ready')})}
for(const id of ['analysis-output','detail-content']){const host=document.getElementById(id);if(host){new MutationObserver(()=>animateReport(host)).observe(host,{childList:true})}}
const chartHost=document.getElementById('ni-inventory-chart');if(chartHost){new MutationObserver(()=>animateChildren(chartHost,'.ni-source-bar','nm-stagger')).observe(chartHost,{childList:true});}
// Navigation feedback is handled by the existing app; never intercept submit or number logic.
})();
