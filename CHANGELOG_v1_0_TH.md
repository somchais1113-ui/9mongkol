# 9มงคล v1.0 — Number Card Search Integration (11 พฤศจิกายน 2569)

## ขอบเขตการเปลี่ยนแปลง
- ปรับเฉพาะ **การ์ดผลค้นหาเบอร์** ในหน้า `ค้นหาเบอร์` ให้ใช้ HTML/CSS/JS/SVG Component จากไฟล์ `9MONGKOL_Number_Card_HTML_Objects_v1(1).zip` ที่ผู้ใช้ส่งมา
- การ์ดใหม่มี NUMBER ID, สถานะ, ตัวเลขสีแดง-ทอง, หมวดอาชีพ, Career Fit สีแดง-ทองพร้อมตราเป้าหมายและลอเรล, ราคาและ CTA
- เชื่อมแต่ละใบกับหมายเลข/คะแนน/ราคา/สถานะ/ผู้ขายจาก API หรือ Offline Bridge จริง **ไม่ใช้เลขตัวอย่างตายตัวจาก Component**
- เพิ่มตัวเลือกมุมมอง **สองคอลัมน์** กับ **การ์ดใหญ่** และจัดเป็นหนึ่งคอลัมน์อัตโนมัติบนมือถือ
- ปุ่ม `ดูรายละเอียด` ยังเปิดรายงานวิเคราะห์ของหมายเลขที่กดได้
- Animation เมื่อเลื่อนดูการ์ดทำงานต่อไป แต่ยกเลิก Hover แบบนูน/ยกตัวตามข้อกำหนดเดิม
- ไม่แก้ไขภาพ Hero, แถบ Banner, Logo, สีหลัก, กฎการวิเคราะห์, Career Matrix หรือ Database

## ไฟล์สำคัญ
- `web/number-card/number-card.js` — ตัวเรนเดอร์จาก Kit
- `web/number-card/number-card.css` — CSS Component จาก Kit
- `web/number-card/number-card-integration.css` — Responsive/สัดส่วนสำหรับ Search จริง
- `web/number-card/icons/` — SVG Vector จาก Kit
- `reference-assets/number-card-html-kit-v1/` — Kit ต้นฉบับ (รวมคู่มือและตัวอย่าง)
- `tests/test_v10_number_cards.py` — เทสต์โครงสร้างการเชื่อมต่อ
- `scripts/qa_card_integration.py` — ตัวอย่างตรวจการแสดงผล (ต้องมี Playwright/Chromium)

## ข้อจำกัด
- ราคา/สถานะและข้อมูลส่วนใหญ่เป็นรายการสาธิต ไม่ใช่การยืนยันสต็อกแบบเรียลไทม์
- Career Fit Index เป็นคะแนนจำลองจาก Rulebook ตามความเชื่อ ไม่ใช่โอกาสความสำเร็จจริง
- โลโก้/ภาพและระบบข้อมูลส่วนอื่นใช้ไฟล์เดิมในชุด v0.9.2
