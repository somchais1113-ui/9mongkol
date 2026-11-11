(function(){
 'use strict';
 const frame=document.getElementById('live-preview');
 const area=document.querySelector('.preview-area');
 const $=id=>document.getElementById(id);
 const initial={phone:'096-569-2970',profession:'Designer / Creative',score:'72',price:'3900',id:'005',status:'ยังไม่ยืนยัน',catalogue:'DEMO — Catalogue A · 1',seller:'แหล่งเสนอขาย · DEMO',button:'ดูรายละเอียด',link:'#number-details'};
 const ids={phone:'phone',profession:'profession',score:'score',price:'price',id:'card-id',status:'status',catalogue:'catalogue',seller:'seller',button:'button',link:'link'};
 function getData(){return {phone:$('phone').value,profession:$('profession').value,score:Number($('score').value),price:Number($('price').value),id:$('card-id').value,status:$('status').value,verified:$('status').value==='ยืนยันแล้ว',catalogue:$('catalogue').value,seller:$('seller').value,buttonLabel:$('button').value,detailUrl:$('link').value};}
 function update(){if(frame.contentWindow)frame.contentWindow.postMessage({type:'9MONGKOL_UPDATE',data:getData()},'*');}
 Object.values(ids).forEach(id=>{ $(id).addEventListener('input',update);$(id).addEventListener('change',update);});
 $('reset').addEventListener('click',()=>{Object.keys(ids).forEach(key=>$(ids[key]).value=initial[key]);update();});
 frame.addEventListener('load',update);
 window.addEventListener('message',event=>{if(event.source!==frame.contentWindow)return;const msg=event.data;if(msg?.type==='9MONGKOL_HEIGHT'){frame.style.height=Math.max(320,Math.min(2100,msg.height+12))+'px';}});
 document.querySelectorAll('[data-device]').forEach(button=>{if(button.tagName!=='BUTTON')return;button.addEventListener('click',()=>{document.querySelectorAll('button[data-device]').forEach(x=>x.classList.toggle('selected',x===button));area.dataset.device=button.dataset.device;setTimeout(update,40);});});
})();
