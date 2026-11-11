# 9มงคล v0.9 — Brand Logo & Steady Hover Edition

โลโก้ทางการแบบทอง–ดอกบัวตามไฟล์ล่าสุดของผู้ใช้ ปรับ hover ไม่ยกตัว และปิด parallax ตามเมาส์ ดู `CHANGELOG_v0_9_TH.md`, `LOGO_IMPLEMENTATION_TH.md`

# 9 มงคล — Web Platform v0.8 (Readability Edition)

เว็บไซต์วิเคราะห์เบอร์โทรศัพท์ตาม *ชุดกฎสาธิต* พร้อมระบบค้นหาเบอร์จากหลายแหล่ง จัดอันดับความสอดคล้องตามสายอาชีพ และแสดงกราฟที่อธิบายผลลัพธ์ได้

**Visual master:** `9MONGKOL_Web_Asset_Kit_v1` ที่ผู้ใช้อัปโหลด — Crimson Red / Metallic Gold / Ivory, โลโก้ 9 มงคล, ภาพประกอบเทพ 4 องค์, SVG icons, numerology badges และ ornamental graphics.

## เปิดเว็บไซต์ทันที (Offline Demo)

ดับเบิลคลิก `index.html` จากโฟลเดอร์หลักของ ZIP ที่แตกแล้ว ใช้ค้นหาและวิเคราะห์เบอร์สาธิตได้ทันทีโดยไม่ต้องรันเซิร์ฟเวอร์ ข้อมูลที่นำเข้าในโหมดนี้จะไม่บันทึกข้ามการรีเฟรช

> **ข้อสำคัญ:** ไม่ควรเปิด `web/index.html` ด้วยการดับเบิลคลิก เพราะไฟล์นั้นออกแบบให้เปิดผ่าน Backend; `index.html` ที่ root คือหน้า Offline ที่พร้อมเปิดโดยตรง

## รัน Backend บน Mac

ดับเบิลคลิก `START_MAC.command` หรือรันคำสั่ง:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
./run.sh
```

เปิด `http://127.0.0.1:8000` เพื่อใช้งาน SQLite แบบบันทึกถาวรเฉพาะเครื่อง

## Typography ใหม่ใน v0.8 — อ่านชัดขึ้นสำหรับผู้ใช้วัยทำงาน

- ข้อความที่อ่านต่อเนื่อง: Desktop **17px**, Mobile **16px**
- คำอธิบายหน้ารายงาน / คำแนะนำ / Rule Trace: **16px**
- ตัวอักษรรอง / สถานะ / Labels: **14–16px** แทน 9–13px
- หัวข้อ section: 26–36px, หัวข้อหน้า: 30–45px แบบ Responsive
- ปุ่มและช่องกรอกข้อมูลสูงไม่น้อยกว่าประมาณ 44px; เว้นบรรทัดข้อความให้อ่านได้ชัด
- Mobile ใช้การเรียงหนึ่งคอลัมน์เมื่อจำเป็น แทนการลดฟอนต์ลงเพื่อยัดในกริด
- ไม่มี Blur บนข้อความ; ยังคงเอฟเฟกต์ Sacred Luxury Motion ของ v0.7

แก้ค่าหลักได้ใน `web/nine-readable.css` ที่โหลดเป็นไฟล์ CSS ลำดับสุดท้าย โดยเปลี่ยน font-size และ line-height ได้โดยไม่แตะ Rule Engine หรือกราฟข้อมูล

ดูรายละเอียดที่ `TYPOGRAPHY_GUIDE_TH.md` และ `CHANGELOG_v0_8_TH.md`.

## Motion ที่เพิ่มใน v0.7

- แสงทองกวาดผ่าน Hero Banner แบบนุ่มนวล และกรอบทองหายใจช้า ๆ
- ฝุ่นประกายทองบางเบาบริเวณ Hero (ลดจำนวนบนมือถือ)
- วงแหวนเลขศาสตร์หมุนช้าและแสงที่ตราเลข 9 โดยภาพหลักและตัวหนังสือไม่ถูก Blur
- แสงวิ่งบนปุ่มค้นหา, Feedback เมื่อเลือกเลข, Stagger Cards และ Motion ใน Report / Charts
- ปุ่ม “ลดเอฟเฟกต์ / เปิดเอฟเฟกต์” อยู่ที่แถบเครื่องมือส่วนบน และบันทึกความชอบในเบราว์เซอร์เมื่ออนุญาต
- รองรับ `prefers-reduced-motion` และหยุด Animation เมื่อแท็บไม่ได้อยู่ด้านหน้า
- กราฟ/คะแนนมาจาก Engine ชุดเดิม ไม่มีการเปลี่ยนค่าน้ำหนักหรือ Rulebook

ไฟล์ที่เพิ่ม: `web/nine-motion.css`, `web/nine-motion.js` และ `MOTION_GUIDE_TH.md`.

## ฟีเจอร์ที่คงไว้

- วิเคราะห์เลขมือถือไทย 10 หลัก, รวม `+66`
- แยกคู่เลข 7 คู่ใน 8 หลักท้าย พร้อม rule trace อธิบายคะแนน
- Career Matching 12 อาชีพและคุณลักษณะ 6 ด้าน
- Radar Chart, Career Ranking, Recommendation Cards
- ค้นหาเลขที่ต้องมี, เลขที่ไม่ต้องมี, เลขตำแหน่ง, งบประมาณ, สถานะ, แหล่งขาย
- CSV Import และ Bulk Paste (เมื่อมีสิทธิ์ใช้งานข้อมูล)
- ภาพประกอบปรับได้ด้วยการอัปโหลด, Zoom, X/Y position ในเบราว์เซอร์
- Web UI รองรับ Desktop / Mobile และ `prefers-reduced-motion`

## การปรับแบรนด์

- `web/nine-mongkol.css`: ไฟล์หลักสำหรับ Mood & Tone สีแดง–ทอง (แก้ลำดับท้าย CSS)
- `web/assets/9mongkol/`: โลโก้ ภาพ Banner ภาพเทพ SVG และ Background ที่ใช้จริง
- `web/assets/9mongkol/ganesha-hero.png`: เปลี่ยนไฟล์นี้หากต้องการเปลี่ยนภาพเริ่มต้นให้ผู้ใช้ทุกคน
- `web/index.html`: หน้า Backend
- `index.html`: หน้า Offline ที่สร้างจาก `scripts/build_offline.py`
- `BRAND_SYSTEM_TH.md`: Brand tokens และ Asset Mapping

หลังแก้ไฟล์ HTML/CSS/JS สำหรับ Backend ถ้าต้องการอัปเดตหน้า Offline ให้รัน:

```bash
python3 scripts/build_offline.py
```

## สถานะและข้อจำกัด

**เป็น Working MVP ไม่ใช่ Production-Ready** ฐานข้อมูลเป็นข้อมูลสังเคราะห์เพื่อทดสอบ การขาย/ราคา/สถานะยังไม่ได้ตรวจสอบเรียลไทม์ และการ Import ใน Production ต้องเพิ่ม Authentication, Authorization, Rate Limiting, Audit และการจัดการข้อมูลส่วนบุคคลตามกฎหมาย

คำตีความเบอร์และคะแนน Career Fit เป็นโมเดลเชิงความเชื่อที่ตั้งกฎขึ้นเพื่อสาธิต ไม่ได้พิสูจน์ว่าตัวเลขส่งผลต่อชีวิตหรือผลสำเร็จในการทำงานจริง ภาพเทพในเว็บไซต์เป็นงานศิลป์ประกอบแบรนด์ ไม่ใช่คำรับรองผลลัพธ์ใดๆ

## ทดสอบ

```bash
PYTHONPATH=. pytest -q
node --check web/app.js
node --check web/insights.js
```

ดู `QUICK_START_TH.md` สำหรับคู่มือภาษาไทย และ `CHANGELOG_v0_8_TH.md` สำหรับรายละเอียดที่เปลี่ยนแปลง
