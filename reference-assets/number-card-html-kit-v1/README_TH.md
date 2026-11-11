# 9มงคล — Number Card HTML / Object Pack V1

**นำหน้า Card ตาม Reference มาแปลงเป็น HTML/CSS และ SVG Object ที่แก้ไขได้**

## เปิดดูเลย

1. แตกไฟล์ ZIP
2. เปิด `index.html` ด้วย Chrome, Edge หรือ Safari — ทดลองแก้ข้อความ/คะแนนทางขวามือได้ทันที
3. กด Desktop / Tablet / Mobile เพื่อดู Responsive Preview
4. เปิด `assets-gallery.html` เพื่อดูไฟล์ SVG แยก
5. เปิด `examples/standalone.html` เพื่อดู Card แบบไม่มีกล่องควบคุม

## ภายในแพ็ก

```text
9MONGKOL_Number_Card_HTML_Objects_v1/
├── index.html                  # Live Preview + Customizer
├── assets-gallery.html         # SVG Asset Overview
├── components/
│   ├── number-card.css         # Card Styling (แก้ไขได้)
│   └── number-card.js          # Card Data-driven Renderer
├── assets/
│   ├── icons/                  # SVG ไอคอน/วัตถุ แยก 9 รายการ
│   ├── reference/              # ภาพจากผู้ใช้ (เพื่อเทียบการออกแบบ)
│   └── screenshots/            # ภาพแสดงผลจริง Desktop / Mobile
├── examples/
│   ├── standalone.html         # ตัวอย่างใช้ในเว็บเดี่ยว ๆ
│   ├── embed-preview.html      # หน้า iframe จำลอง Responsive
│   └── card-data.json          # โครงข้อมูล Number Object
├── js/demo.js                  # ระบบ Live Preview
└── docs/INTEGRATION.md         # คู่มือนำไปใช้งานจริง
```

## จุดเด่น

- HTML จริง: ตัวเบอร์ ราคา คะแนน และคำต่าง ๆ ไม่ใช่รูปภาพ
- CSS Gradient: Red / Gold / Cream / Inner Glow / Shadow
- SVG แยก: Target Icon, Laurel Wreath, CTA Arrow, Lotus, Coin, Number 9 และอื่น ๆ
- ไม่มีกราฟิกข้างล่าง Card ตามคำสั่งล่าสุด
- เบอร์โทรขยายแล้ว (จากเวอร์ชันก่อนหน้า) แต่ Responsive Mobile ไม่ล้นกรอบ
- ไม่ต้องติดตั้งแพ็กเกจหรือเชื่อม API

> หมายเหตุ: เป็นการ Rebuild องค์ประกอบจากภาพอ้างอิง ไม่ใช่ PSD/AI Layer ที่แยกจากภาพเดิมแบบ Pixel Perfect. บางมุมโค้ง เงา แสง และการเรนเดอร์ Font อาจต่างจากภาพต้นฉบับเล็กน้อย
