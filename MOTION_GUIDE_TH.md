# คู่มือ Animation · 9 มงคล v0.7

## Mood & Tone — Sacred Luxury

- สีหลักเป็น Crimson Red `#7A0008`, Metallic Gold `#D4AF37`, Ivory `#F8F1E3` ตาม Asset Kit
- การเคลื่อนไหวช้าและประณีต: sheen 7–13 วินาที, ring 40 วินาที, reveal 0.48–0.75 วินาที
- ภาพเทพและข้อความหลักต้องคมชัด: ห้ามใส่ `filter: blur()` ให้กับตัวหนังสือและภาพหลัก

## ปรับความเร็ว / ความเข้ม

- `web/nine-motion.css`: ค้นหา `@keyframes nm-banner-sheen`, `nm-orbit`, `nm-dust-float`, `nm-button-sheen`
- เปลี่ยน duration ที่ declaration `animation` ของแต่ละ component
- `web/nine-motion.js`: แก้ตำแหน่งและจำนวนอนุภาคในตัวแปร `points`
- ปุ่มควบคุมใน Topbar มี ID `nine-motion-toggle` ปิด/เปิดความเคลื่อนไหวและบันทึกความชอบใน localStorage เมื่อเบราว์เซอร์รองรับ

## ความปลอดภัยทาง UX

- หลีกเลี่ยงการกระพริบเร็ว, การแสดงแสงรุนแรง, และการซ่อนหัวข้อสำคัญ
- เคารพ `prefers-reduced-motion`: เนื้อหาทั้งหมดต้องมองเห็นได้แม้ปิด Animation
- ใช้ requestAnimationFrame/IntersectionObserver สำหรับการวาดที่จำเป็น; ไม่โหลดไลบรารี Motion เพิ่ม
- ไม่แตะ `app/engine.py`, `app/rulebook.json`, `app/careers.json` หรือฐานข้อมูล

## การใช้งาน

**Offline:** เปิด `index.html` ในโฟลเดอร์หลัก (ข้อมูลทดลองจะไม่บันทึกข้ามการรีเฟรช)

**Mac Backend:** เปิด `START_MAC.command` จากนั้นไป `http://127.0.0.1:8000`

**ทดสอบ:** `PYTHONPATH=. pytest -q`

**แก้หน้า Backend:** `web/index.html` และ `web/nine-motion.*` จากนั้นรัน `python scripts/build_offline.py` เพื่ออัปเดตหน้า Offline
