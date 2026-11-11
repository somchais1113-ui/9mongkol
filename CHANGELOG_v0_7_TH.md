# CHANGELOG · 9 มงคล v0.7 · Sacred Luxury Motion

วันที่ 11 พฤศจิกายน 2569

**หลักการ:** ไม่เปลี่ยน Mood & Tone ของ v0.6 / ใช้ Asset Kit เดิม, เพิ่มเฉพาะความเคลื่อนไหวที่สื่อถึงความประณีตและแสงทอง

- Golden sweep บน Hero Banner, soft border breathe และประกายทองขนาดเล็ก
- หมุนเส้นลายรัศมีรอบเลข 9 อย่างช้า ๆ โดยภาพตราเลข 9 ไม่หมุนตาม
- Premium call-to-action sheen, hover halo และ number-chip feedback
- Scroll reveal เน้นการเข้าจังหวะโดยไม่ซ่อนคอนเทนต์หาก JavaScript ปิด
- Stagger Number Cards / Career Bars / Radar Polygon เมื่อแสดงผล
- ปุ่มลด/เปิดเอฟเฟกต์, เคารพ Reduce Motion, หยุดแอนิเมชันเมื่อแท็บไม่ได้อยู่ด้านหน้า
- ป้องกันปัญหาข้อความ Hero เบลอและไม่ปรากฏเมื่อเปิด Reduce Motion
- ซ่อม Offline Builder ให้แทรก offline-data.js และ offline-bridge.js ก่อน app.js แบบถูกต้อง
- Backend version label อัปเดตเป็น 0.7.0; ไม่เปลี่ยนสูตรหรือฐานข้อมูล

**ทดสอบ:** 15 Pytest ผ่าน; ตรวจหน้า Offline ด้วย HTML/CSS/JS inline simulation บน Chromium 1440/390 px รวม Reduce Motion
