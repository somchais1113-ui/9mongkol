# Full Package v1.3 — การ์ดเบอร์ 9มงคล

**สิ่งที่ส่งมอบ:** `index.html` เปิดแบบ Offline, `web/` HTML/CSS/JS และ SVG ที่แก้ไข, Backend FastAPI, ฐานข้อมูลตัวอย่าง, `START_MAC.command`, ชุดทดสอบและ Preview ภายใต้ `previews/v13/`

**รุ่นที่ใช้:** v1.3 ขยายเบอร์และราคา ลบ glow หลังคะแนน และเพิ่มความยาวรวงข้าว โดยยังคงระบบเดิมทุกส่วน  รายละเอียดใน `CHANGELOG_v1_3_TH.md`

# v1.2 Card Design Lock — FULL PACKAGE
- เพิ่ม `web/number-card/number-card-design-lock.css`
- เปลี่ยนมุมมองแรกเป็นการ์ดใหญ่ตาม Master (สลับสองคอลัมน์ได้)
- มีภาพ QA ใหม่ `previews/v12/` และเอกสาร `DESIGN_LOCK_v1_2_TH.md`
- API/Offline รองรับข้อมูล Dynamic เดิมทั้งหมด

# 9มงคล Full Package v1.1 — Readable Number Cards

## 9มงคล v1.0 — Number Card Edition

ปรับผลค้นหาเบอร์ด้วย HTML Objects Kit ที่ผู้ใช้ส่งมา รองรับการ์ด 2 คอลัมน์และการ์ดใหญ่ พร้อมทั้ง Online/Offline โดยคงระบบวิเคราะห์เดิมทุกอย่าง ดู `CHANGELOG_v1_0_TH.md` และ `NUMBER_CARD_GUIDE_TH.md`

# FULL PACKAGE — 9 มงคล v0.8 (Readability Edition)

## ไฟล์ในชุดส่งมอบ

- `index.html` — เว็บไซต์ Demo เปิดได้โดยตรงแบบ Offline
- `web/` — หน้าเว็บแบบเชื่อม Backend, CSS/JS, ภาพและ SVG ที่นำมาจาก Asset Kit
- `app/` — FastAPI API + Number Rule Engine + Career Matching
- `ni.sqlite3` — ฐานข้อมูล SQLite สาธิต
- `sample_data/` — CSV สังเคราะห์สำหรับทดสอบ
- `scripts/` — สร้าง Offline Snapshot, Seed และ Reindex
- `brand_asset_kit/9MONGKOL_Web_Asset_Kit_v1_original.zip` — เก็บไฟล์ Asset Kit ต้นฉบับที่ผู้ใช้ให้มา เพื่อแก้ไขเพิ่มเติมในอนาคต
- `previews/*.jpg` — ภาพตัวอย่างหน้าหลักและหน้ารายงาน ทั้ง Desktop/Mobile
- `README.md`, `QUICK_START_TH.md`, `BRAND_SYSTEM_TH.md`, `CHANGELOG_v0_6_TH.md` — คู่มือ
- `tests/` — เทสต์ Engine/Brand/Asset Routes/Motion, รวม 15 รายการ

## แบรนด์ที่นำมาใช้จริง

สี: Crimson #7A0008, Gold #D4AF37, Wine #3B0408, Ivory #F8F1E3

ภาพ: โลโก้หลัก, ภาพกลุ่ม 4 เทพ, Ganesha ภาพแก้ไขได้, artwork card 4 องค์, SVG Icon, Number Emblems, Cosmic/Red Silk Background

## ข้อจำกัด

นี่คือ MVP สาธิต ไม่ใช่เว็บไซต์ขายเบอร์ Production จริง ไม่มีระบบผู้ขาย/ชำระเงิน/จองเบอร์แบบสด คำพยากรณ์และคะแนนอาชีพใช้กฎสาธิตตามความเชื่อ ไม่ใช่ผลลัพธ์ทางวิทยาศาสตร์

## v0.7 Motion Components

- `web/nine-motion.css` — Motion Layer แยกจากแบรนด์ CSS เดิม
- `web/nine-motion.js` — Particle decorations, reveal, chart animations, effect toggle
- `MOTION_GUIDE_TH.md` — คู่มือเปิด/ปิดและการแก้ Motion Tokens

## v0.8 New Files
- `web/nine-readable.css` — Typography overrides สำหรับความอ่านง่ายทั้ง Desktop/Mobile
- `TYPOGRAPHY_GUIDE_TH.md` — คู่มือขนาดตัวอักษรและการปรับต่อ
- `CHANGELOG_v0_8_TH.md` — สรุปสิ่งที่เปลี่ยนและผล QA
- `scripts/qa_typography.py` — ทดสอบ browser layout/overflow (ต้องมี Playwright และ Chromium)
