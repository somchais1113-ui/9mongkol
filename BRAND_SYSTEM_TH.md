# Brand System — 9 มงคล

## การตีความ Mood & Tone

แบรนด์อ้างอิงโดยตรงจาก Web Asset Kit ที่ผู้ใช้อัปโหลด ใช้ความรู้สึก **Premium Thai Numerology / Sacred Gold / Rich Crimson** บนพื้นสีไวน์เข้มและทองเรืองรอง คู่กับพื้น Ivory สำหรับส่วนอ่านข้อมูลและทำงานจริง

| Color role | HEX | Usage |
| --- | --- | --- |
| Crimson | `#7A0008` | Hero, navigation emphasis, primary cards |
| Vermilion | `#C01818` | Primary accent and active states |
| Gold | `#D4AF37` | Borders, emblem, icon, highlights |
| Gold Light | `#FFE3A0` | High-contrast text on wine surfaces |
| Ivory | `#F8F1E3` | Form, report, chart surfaces |
| Onyx | `#1B0809` | Deep shadow / high depth |
| Wine | `#3B0408` | Main site background |
| Highlight | `#FFF4C7` | Important CTA / decorative glow |

Typography: `Noto Sans Thai` สำหรับเนื้อหาและ Control, `Noto Serif Thai` สำหรับ Headline สำคัญ (fallback เป็น Tahoma / system font เมื่อ Offline ไม่มีอินเทอร์เน็ต)

## Asset mapping ที่นำมาใช้จริง

| Element | ไฟล์ใช้งานภายในเว็บ | Source ใน Kit |
| --- | --- | --- |
| Primary logo | `web/assets/9mongkol/logo-9mongkol.png` | `01_LOGO/logo_9mongkol_clean_transparent.png` |
| Favicon | `web/assets/9mongkol/favicon.svg` | `01_LOGO/favicon_lotus_9.svg` |
| Hero Group | `web/assets/9mongkol/hero-group.png` | `03_HERO/hero_group_source.png` |
| Hero/background | `web/assets/9mongkol/cosmic-red.jpg`, `red-silk.jpg` | `09_BACKGROUND/` |
| Editable image default | `web/assets/9mongkol/ganesha-hero.png` | `02_DEITIES/source_crops/deity_ganesha_hero_source.png` |
| Deity cards | `web/assets/9mongkol/{ganesha,lakshmi,caishen,guanyin}-card.png` | `02_DEITIES/source_crops/` |
| Service icons | `web/assets/9mongkol/icon-*.svg` | `04_SYMBOLS_VECTOR/` |
| Number emblems | `web/assets/9mongkol/badge-{9,99,999}.svg` | `05_NUMBERS_AND_BADGES/` |

## การเปลี่ยนภาพ

- ภายในหน้าเว็บ ปุ่ม **เปลี่ยนภาพ** ใช้อัปโหลดและปรับ zoom / position เฉพาะเบราว์เซอร์นั้น
- ถ้าต้องการเปลี่ยนภาพเริ่มต้นของเว็บไซต์ทุกเครื่อง ให้แก้ไฟล์ `web/assets/9mongkol/ganesha-hero.png` หรือแก้ path ใน `web/index.html` และ `web/insights.js`
- ภาพ `_source.png` ที่เป็น crop จาก moodboard มีพื้นหลังติดอยู่และความละเอียดจำกัด จึงไม่ควรขยายเกินขนาดจริงมากเกินไป

## ความเหมาะสมของการใช้งาน

ใช้การจัดองค์ประกอบและภาพประกอบตามแบรนด์ที่ผู้ใช้ให้ ไม่อ้างว่าภาพเทพมีผลต่อความสำเร็จหรือว่าการคำนวณเบอร์มีหลักฐานทางวิทยาศาสตร์
