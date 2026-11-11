/* 9MONGKOL Number Card V1 | vanilla JS | no dependencies | file:// compatible.
   Browser API: NineMongkolNumberCard.mount(element, data, options)
                NineMongkolNumberCard.render(data, options) -> HTML string
                NineMongkolNumberCard.defaults
*/
(function (global) {
  'use strict';
  const defaults = Object.freeze({
    id: '005', phone: '0965692970', status: 'ยังไม่ยืนยัน', verified: false,
    profession: 'Designer / Creative', score: 72, totalScore: 100,
    price: 3900, currency: 'THB', catalogue: 'DEMO — Catalogue A · 1',
    seller: 'แหล่งเสนอขาย · DEMO', buttonLabel: 'ดูรายละเอียด',
    detailUrl: '#number-details'
  });
  const esc = (s) => String(s ?? '').replace(/[&<>"']/g, m => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]));
  const cleanUrl = (url) => {
    const s = String(url || '').trim();
    return /^(https?:\/\/|\/|#|\.\/|\.\.\/)/i.test(s) ? esc(s) : '#number-details';
  };
  function formatPhone(s) {
    const val = String(s || '').trim();
    const digits = val.replace(/\D/g, '');
    return digits.length === 10 ? `${digits.slice(0,3)}-${digits.slice(3,6)}-${digits.slice(6)}` : val;
  }
  // Render a telephone number as fixed, visually distinct 3–3–4 groups.
  // Each group stays together, while the complete value remains available to screen readers.
  function phoneMarkup(value) {
    const digits = String(value || '').replace(/\D/g,'');
    if (digits.length !== 10) return esc(formatPhone(value));
    return [digits.slice(0,3), digits.slice(3,6), digits.slice(6)]
      .map(group => `<span class="nmk-card__phone-group">${esc(group)}</span>`)
      .join('<span class="nmk-card__phone-dash" aria-hidden="true">-</span>');
  }
  function formatMoney(value, currency='THB') {
    const number = Number(value);
    if (!Number.isFinite(number)) return String(value);
    return new Intl.NumberFormat('th-TH',{style:'currency',currency,maximumFractionDigits:0}).format(number).replace('฿\u00a0','฿');
  }
  function render(data={}, options={}) {
    const d = {...defaults,...data};
    const base = String(options.assetBase || 'assets/icons').replace(/\/$/,'');
    const score = Math.max(0,Math.min(Number(d.totalScore)||100,Number(d.score)||0));
    const totalScore = Number(d.totalScore)||100;
    const image = (name, alt='', cls='') => `<img src="${esc(base)}/${name}.svg" alt="${esc(alt)}" class="${cls}" loading="eager">`;
    return `
<article class="nmk-card" aria-label="เบอร์มงคล ${esc(formatPhone(d.phone))}">
  <div class="nmk-card__inner">
    <header class="nmk-card__top">
      <span class="nmk-card__id">NUMBER / ${esc(d.id)}</span>
      <span class="nmk-card__status${d.verified?' nmk-card__status--verified':''}">${esc(d.status)}</span>
    </header>
    <div class="nmk-card__phone-wrap">
      <h2 class="nmk-card__phone" aria-label="หมายเลขโทรศัพท์ ${esc(formatPhone(d.phone))}">${phoneMarkup(d.phone)}</h2>
      <span class="nmk-card__phone-gleam" aria-hidden="true"></span>
    </div>
    <div class="nmk-card__fit"><span class="nmk-card__fit-label">ความสอดคล้องกับ</span><strong class="nmk-card__occupation">${esc(d.profession)}</strong></div>
    <section class="nmk-card__scorebar" aria-label="Career Fit Index ${score} จาก ${totalScore}">
      <div class="nmk-card__target" aria-hidden="true">${image('target','')}</div>
      <div class="nmk-card__score-caption"><div class="nmk-card__score-heading">Career Fit Index</div><div class="nmk-card__score-sub">คะแนนสาธิต</div></div>
      <div class="nmk-card__score-medallion" aria-label="${score} จาก ${totalScore}">
        ${image('laurel-left','','nmk-card__laurel')}
        <div class="nmk-card__score" role="img" aria-label="คะแนนความสอดคล้อง ${score} จาก ${totalScore}"><span class="nmk-card__score-number" aria-hidden="true">${esc(score)}</span> <span class="nmk-card__score-denom" aria-hidden="true"><span class="nmk-card__score-slash">/</span> <span class="nmk-card__score-total">${esc(totalScore)}</span></span></div>
        ${image('laurel-right','','nmk-card__laurel')}
      </div>
    </section>
    <footer class="nmk-card__bottom">
      <div class="nmk-card__price-group">
        <strong class="nmk-card__price">${esc(formatMoney(d.price,d.currency))}</strong>
        <div class="nmk-card__meta"><span class="nmk-card__meta-line">${esc(d.catalogue)}</span><span class="nmk-card__meta-line">${esc(d.seller)}</span></div>
      </div>
      <a class="nmk-card__cta" href="${cleanUrl(d.detailUrl)}"><span>${esc(d.buttonLabel)}</span>${image('arrow-up-right','','')}</a>
    </footer>
  </div>
</article>`;
  }
  function mount(target, data={}, options={}) {
    const el = typeof target === 'string' ? document.querySelector(target) : target;
    if (!el) throw new Error('9MONGKOL: mount target not found');
    el.innerHTML = render(data,options);
    return el.querySelector('.nmk-card');
  }
  global.NineMongkolNumberCard = {mount, render, defaults, formatPhone, formatMoney};
})(window);
