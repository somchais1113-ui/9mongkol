# 9มงคล — Premium Red & Gold Web Asset Kit (v1)

ชุดไฟล์แยกองค์ประกอบตาม Moodboard ที่ผู้ใช้ส่งมา 2 ภาพ พร้อม vector redraw สำหรับพัฒนาเว็บ

## เปิดดู
1. แตกไฟล์ ZIP
2. เปิด `index.html` ด้วย Chrome / Safari เพื่อดู Asset Library ที่จัดตามหมวด
3. เปิด `00_OVERVIEW/` สำหรับภาพรวมของแต่ละหมวด
4. ใช้ PNG หรือ SVG รายชิ้นในหน้าเว็บไซต์ได้ทันที

## โครงสร้าง
- `01_LOGO/` โลโก้อ้างอิงที่ Crop จากภาพ + โลโก้ที่วาดใหม่แบบตัวหนังสือและ PNG โปร่งใส
- `02_DEITIES/source_crops/` ภาพองค์เทพ 4 องค์ (พระพิฆเนศ พระแม่ลักษมี ไฉ่ซิงเอี๊ย เจ้าแม่กวนอิม)
- `03_HERO/` ภาพ Hero หลักและตำแหน่งโลโก้จาก Moodboard
- `04_SYMBOLS_VECTOR/` ไอคอน SVG / PNG โปร่งใส + ตัวอย่างไอคอนที่ Crop จากต้นฉบับ
- `05_NUMBERS_AND_BADGES/` ตราสัญลักษณ์เลข 9, 99, 999 เวกเตอร์ และต้นแบบ
- `06_FRAMES/` กรอบ SVG/PNG โปร่งใส และภาพ Crop
- `07_ORNAMENTS/` ลวดลาย เมฆ ดอกบัว ทอง ฯลฯ
- `08_PATTERNS_AND_TEXTURES/` แพตเทิร์นและ Texture จาก Moodboard
- `09_BACKGROUND/` ภาพพื้นหลังใหม่ขนาด 1920×1080 และภาพ Crop ที่ใช้เป็น Reference
- `10_UI/` CSS Tokens, Component Styles, ตัวอย่างปุ่ม
- `11_SOURCE_REFERENCES/` Moodboard 2 ภาพต้นฉบับ

## ข้อจำกัดที่ควรทราบ
**ต้นฉบับทั้งสองภาพเป็น PNG แบบ Flatten** ซึ่งไม่มีเลเยอร์ต้นฉบับ จึงไม่สามารถแยกรายละเอียดที่ซ้อนทับกันให้เหมือนงาน Layered PSD ได้
- ไฟล์ลงท้าย `_source.png` คือ **Crop จาก Moodboard**: มีพื้นหลัง/องค์ประกอบเดิมติดมาด้วย จึงไม่ใช่ไฟล์โปร่งใส
- ไฟล์ SVG และ PNG ชื่อเดียวกัน (ไม่ลงท้าย `_source`) เป็น **Vector Redraw ที่สร้างใหม่** มีพื้นหลังโปร่งใส (เฉพาะกลุ่มองค์ประกอบ) สามารถแก้สี เส้น ขนาด และใส่ Animation ได้
- ภาพองค์เทพถูกเก็บเป็นภาพอ้างอิงพร้อมพื้นหลังจาก Moodboard โดยไม่อ้างว่าเป็น die-cut transparent ที่สมบูรณ์
- โลโก้ที่วาดใหม่เป็นการออกแบบเพื่อใช้งานเว็บไซต์ ไม่ใช่การตัดโลโก้ต้นแบบแบบ pixel-perfect และแบบ SVG text ต้องมี font รองรับภาษาไทย
- ภาพ Crop หลายภาพมีความละเอียดเล็กตามตำแหน่งใน Moodboard ไม่ควรขยายเกินความละเอียดต้นฉบับโดยคาดหวังรายละเอียดเพิ่มขึ้น
- ลวดลายเรขาคณิตที่สร้างใหม่เป็นองค์ประกอบเชิงกราฟิก ไม่ได้อ้างความถูกต้องด้านคัมภีร์หรือหลักโหราศาสตร์

## Website integration
ใช้ `10_UI/theme_tokens.css` และ `10_UI/web_components.css` แยกได้ หรือคัดลอก CSS ส่วนที่ต้องการ รวมทั้งรองรับ `prefers-reduced-motion`. ตัวอย่าง:

```html
<link rel="stylesheet" href="10_UI/web_components.css">
<section class="nine-hero">
  <img class="nine-logo" src="01_LOGO/logo_9mongkol_clean_transparent.png" alt="9มงคล">
  <button class="nine-gold-button">ค้นหาเบอร์มงคล</button>
</section>
<img src="04_SYMBOLS_VECTOR/icon_lotus.svg" alt="โชคลาภ">
```

## Brand Palette
- crimson: `#7A0008`
- vermilion: `#C01818`
- gold: `#D4AF37`
- gold_light: `#FFE3A0`
- ivory: `#F8F1E3`
- onyx: `#1B0809`
- wine: `#3B0408`
- highlight: `#FFF4C7`

## ลิขสิทธิ์และความถูกต้อง
ภาพนี้สร้างจาก Moodboard ที่ผู้ใช้ส่งมา พร้อมชุดเวกเตอร์สร้างใหม่ ใช้เป็น concept/illustration เท่านั้น
ก่อนเผยแพร่เว็บไซต์เชิงพาณิชย์ ควรตรวจสอบโลโก้ ชื่อ และความเหมาะสมของภาพองค์เทพ และหลีกเลี่ยงการรับประกันผลความสำเร็จหรือโชคลาภจากหมายเลขโทรศัพท์
