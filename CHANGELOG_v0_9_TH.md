# 9มงคล v0.9 — Brand Logo & Steady Hover Edition

## เปลี่ยนแปลง
1. แทนโลโก้เดิมด้วยไฟล์ `Golden 9มงคล Lotus Emblem(1).png` ที่ผู้ใช้ส่งมา โดยบรรจุไฟล์ต้นฉบับไว้ใน `web/assets/9mongkol/logo-9mongkol-lotus-original.png` และไฟล์ใช้งานจริง `logo-9mongkol-lotus.webp`
2. ใช้โลโก้หลักใน Header, Hero, Footer และใช้ Favicon ที่ตัดจากภาพต้นฉบับเดียวกัน
3. เอาข้อความรองใต้โลโก้ซ้ายบนออก
4. แก้แถบข้อความล่างแบนเนอร์: ซ่อนข้อความเดิมซึ่งเป็นส่วนหนึ่งของไฟล์ภาพต้นฉบับ ด้วยแถบสีแดงไวน์ทึบ เพื่อไม่ตัดต่อหรือทำลายภาพต้นฉบับ
5. Hover การ์ดสถิติ, บริการ, ค้นหา, ภาพประกอบ, หมวดหมู่ ไม่ยกตัวหรือขยายภาพอีกต่อไป ใช้แสงขอบทองเบา ๆ แทน
6. ยกเลิก Hero Parallax ที่ทำให้ Widget เคลื่อนตามเมาส์
7. คง Animation แสงทองและ Motion ที่ไม่ทำให้ข้อความเบลอไว้
8. รองรับทั้ง `index.html` แบบ Offline และหน้า Backend; สร้าง Offline Snapshot ใหม่จากฐานข้อมูล 420 เบอร์สาธิต

## จุดแก้ไขสำคัญ
- `web/nine-polish.css` — ค่า hover, logo, banner, responsiveness
- `web/index.html` และ `index.html` — รูปโลโก้และ stylesheet ใหม่
- `web/app.js` — เลิกเรียก pointer-driven parallax
- `scripts/build_offline.py` — ชี้ไปยัง stylesheet ใหม่ในโหมด Offline

## ข้อจำกัด
ระบบยังเป็น MVP และใช้ข้อมูล/คะแนนตัวอย่างตามกฎความเชื่อ ไม่ได้ยืนยันผลจริงทางวิทยาศาสตร์
