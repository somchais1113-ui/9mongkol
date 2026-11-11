# 9มงคล — Number Card Design Lock v1.2

## Source of truth
- Reference: `reference-assets/USER_MASTER_NUMBER_CARD.jpg` เป็นภาพอ้างอิงที่ผู้ใช้ส่งมา
- Live component: `web/number-card/number-card.js`
- Base: `web/number-card/number-card.css`
- Two-column integration: `web/number-card/number-card-integration.css`
- **Visual master overrides:** `web/number-card/number-card-design-lock.css`
- Source SVG icons: `web/number-card/icons/`

## สิ่งที่ทำ
- วางองค์ประกอบตามภาพ: Number/ID และป้ายสถานะ, หมายเลข Ruby Red / Gold Edge แบบ 3–3–4, ข้อความสายอาชีพ,
  แถบคะแนน Crimson + Metallic Gold ขนาดใหญ่, ไอคอนเป้า + ใบลอเรล, ราคา + แหล่งขาย + ปุ่มแดงทอง
- เอฟเฟกต์แสงทองและเงาทำด้วย CSS เพื่อให้เปลี่ยนหมายเลขหรือคะแนนได้จริง
- มุมมอง **การ์ดใหญ่ตามต้นแบบ** เป็นค่าเริ่มต้น / ปุ่ม **สองคอลัมน์** ใช้สลับไปดูหลายเบอร์ได้
- ไม่ใช้ภาพหน้าการ์ดเป็นพื้นหลัง: เบอร์, ราคา, คะแนนและสถานะมาจาก API หรือ Offline demo
- Hover ไม่ยกการ์ด; รองรับ `prefers-reduced-motion`

## ฟอนต์
ไม่ได้รับไฟล์ `.ttf/.otf` ของภาพต้นแบบ จึงใช้ฟอนต์ fallback ใน Browser
(Thai: Noto Sans Thai / Tahoma; ตัวเลข: Arial Black / Arial)
รูปทรง Glyph อาจต่างจากภาพต้นแบบเล็กน้อย แต่สัดส่วนและ Effect ปรับจากต้นแบบแล้ว
หากมีฟอนต์ต้นฉบับในอนาคต ปรับ `font-family` ของ `number-card-design-lock.css` ได้โดยไม่แก้ Logic

## ขอบเขตความน่าเชื่อถือ
ตัวเลขคะแนน เป็น Career Fit ตาม rule-based prototype ของระบบเดิม ไม่ใช่อัตราความสำเร็จจริง
ราคาและสถานะขายจาก Catalogue สาธิตไม่ใช่สต็อกที่ยืนยัน Real-time

## QA
- Automated tests: `PYTHONPATH=. pytest -q`
- Standalone Chromium render ของ HTML/CSS/SVG ที่ viewport 1440,390,320 pixels
- ภาพล่าสุด: `previews/v12/card_large.png`, `card_compact.png`, `card_mobile.png`, `card_small.png`
