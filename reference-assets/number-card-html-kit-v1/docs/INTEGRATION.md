# วิธีนำ Number Card ไปใช้กับเว็บไซต์ 9มงคล

## 1. นำไฟล์ 2 ชุดไปใส่เว็บไซต์

- `components/number-card.css` และ `components/number-card.js`
- โฟลเดอร์ `assets/icons/` (มี SVG 9 ไฟล์)

ไม่ต้องพึ่ง framework หรือระบบ build และไม่จำเป็นต้องใช้ไฟล์ภาพต้นแบบในการแสดงผล

## 2. เพิ่มใน HTML

```html
<link rel="stylesheet" href="components/number-card.css">
<div id="number-card-005"></div>
<script src="components/number-card.js"></script>
<script>
  NineMongkolNumberCard.mount('#number-card-005', {
    id: '005',
    phone: '0965692970',
    profession: 'Designer / Creative',
    score: 72,
    totalScore: 100,
    price: 3900,
    status: 'ยังไม่ยืนยัน',
    catalogue: 'DEMO — Catalogue A · 1',
    seller: 'แหล่งเสนอขาย · DEMO',
    detailUrl: '/numbers/005'
  }, { assetBase: 'assets/icons' });
</script>
```

ค่า `assetBase` ต้องเป็น path ที่อ้างอิงจากตำแหน่งของหน้า HTML (ไม่ใช่ตำแหน่ง JS)

## 3. แก้ข้อมูล / สร้างหลาย Card

สร้าง `<div id="card-1"></div>` และ `<div id="card-2"></div>` แล้วเรียก `mount` สำหรับแต่ละ ID ด้วยข้อมูลแต่ละใบ โดย data เป็น JavaScript Object และ JSON ตัวอย่างอยู่ที่ `examples/card-data.json`

รองรับ: `id`, `phone`, `status`, `verified`, `profession`, `score`, `totalScore`, `price`, `currency`, `catalogue`, `seller`, `buttonLabel`, `detailUrl`

ใช้ `render(data, options)` เพื่อรับ HTML string ถ้าต้องการนำไปแทรกด้วยระบบ template ส่วนระบบอื่นของเว็บ เช่น การคำนวณ Career Fit Index ไม่ได้รวมในแพ็กนี้

## 4. ปรับธีมสี

ใช้ CSS variables ตามนี้ใน stylesheet ที่โหลดหลัง `number-card.css`:

```css
:root {
  --nmk-bg: #fff4db;
  --nmk-red: #9b0007;
  --nmk-gold: #edac33;
  --nmk-copper: #a34d05;
}
```

ตัวแปรเป็น Design Tokens ชุดเริ่มต้น บางส่วนของ gradient มีการระบุสีโดยตรง เพื่อให้ได้ Art Direction ตามภาพอ้างอิง

## 5. ปรับขนาดเบอร์โทร

```css
.nmk-card__phone {
  font-size: clamp(39px, 9.4vw, 145px);
  transform: scaleX(1.32);
}
```

- เพิ่ม/ลด `9.4vw` เพื่อเปลี่ยนสัดส่วนบน Desktop
- เพิ่ม/ลด `145px` เพื่อเปลี่ยนเพดานขนาดสูงสุด
- มี media query แยกสำหรับ Tablet/Mobile เพื่อไม่ให้เบอร์ล้นการ์ด

## 6. ตำแหน่ง CSS class หลัก

| Class | ส่วนที่ควบคุม |
|---|---|
| `.nmk-card` | กรอบหลัก พื้นหลัง เงา |
| `.nmk-card__top` | Header / สถานะ |
| `.nmk-card__phone` | เบอร์โทร |
| `.nmk-card__fit` | ความสอดคล้องกับอาชีพ |
| `.nmk-card__scorebar` | แถบคะแนนแดง–ทอง |
| `.nmk-card__score-number` | ตัวเลข 72 |
| `.nmk-card__score-denom` | ตัวเลข /100 |
| `.nmk-card__price` | ราคา |
| `.nmk-card__cta` | ปุ่ม CTA |

## หมายเหตุ

- ไฟล์ใน `assets/reference` เป็นภาพที่ผู้ใช้ส่งให้ ใช้ตรวจเทียบ Design เท่านั้น
- ไฟล์ SVG เป็นเวกเตอร์ที่วาดใหม่ เพื่อการปรับแต่ง ไม่ใช่การดึง Layer ตรงจาก PNG
- ข้อความ `คะแนนสาธิต` และข้อมูลการขายในชุดนี้เป็น DEMO และไม่มีระบบคำนวณความเหมาะสมหรือยืนยันเบอร์จริง
- ปุ่มตัวอย่างมี URL placeholder ต้องเปลี่ยน URL ก่อนนำไป Production
- CSS รองรับ reduced-motion และ focus-visible; สี/เอฟเฟกต์อาจต่างกันเล็กน้อยตาม Browser/Font
- ไม่รวมไฟล์ Font เพิ่มเติม ใช้ Font Stack ที่ติดตั้งในเครื่องผู้ใช้
