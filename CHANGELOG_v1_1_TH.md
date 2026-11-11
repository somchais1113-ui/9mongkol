# 9มงคล v1.1 — Number Readability & Scanning Refinement

ปรับเฉพาะ Card UI บนหน้าค้นหาเบอร์ (Explorer) จาก v1.0 โดยเก็บสีแดง–ทอง, Official Logo, Asset Kit, Animation อื่น, Backend และระบบคำนวณเดิมไว้ครบ

## สิ่งที่แก้

- เลขโทรศัพท์ 10 หลักแยกเป็นสามกลุ่ม 3–3–4 เช่น `097 – 464 – 1465` แต่ละกลุ่มถูกห่อด้วย span จึงรักษาระยะได้สม่ำเสมอ
- เลิกใช้ letter-spacing ติดลบที่บีบเลขติดกัน ปรับเป็น tabular numerals และ letter spacing บวกเล็กน้อยเพื่ออ่านแบบกวาดสายตา
- คะแนนจัดเป็นเลขหลักเด่น เช่น `71` และ denominator `/ 100` ในกล่องรอง มีระยะห่างชัด ไม่ติดเป็น `71100`
- ลดความเด่นของรหัสลำดับ/สถานะ, ปรับขนาด/คอนทราสต์ของราคาและแหล่งขาย
- ปรับช่องไฟแต่ละบล็อกภายในการ์ด (top, number, fit, score, price, CTA)
- ครอบคลุม 2-column desktop, large-card view, 390px และ 320px mobile
- คง hover แบบไม่มีการเลื่อน/ยกตัว

## แก้โค้ดต่อที่ใด

- `web/number-card/number-card.js` — แยกกลุ่มเลขและ markup คะแนน
- `web/number-card/number-card-integration.css` — คุมจังหวะช่องไฟและลำดับความเด่นในหน้า Explorer
- `web/index.html` และ `index.html` — cache bust v1.1.0 ของ Component

## ข้อสังเกต

Career Fit Index เป็นคะแนนทดลองตาม Rule Engine เดิม ไม่ใช่เปอร์เซ็นต์ความสำเร็จจริงของอาชีพและไม่ได้ยืนยันสต็อกแบบเรียลไทม์
