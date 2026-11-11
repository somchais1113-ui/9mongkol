# อัปเดต v1.1: การ์ดค้นหาใช้ span 3–3–4 สำหรับเลขโทรศัพท์ + แยกเลขคะแนน/100 และจังหวะช่องไฟใหม่ แก้ไฟล์ web/number-card/number-card-integration.css

# คู่มือแก้ไขการ์ดเบอร์ 9มงคล

## เปลี่ยนดีไซน์
แก้ `web/number-card/number-card-integration.css` เป็นหลัก เพราะเป็นตัวกำหนดสัดส่วนการ์ดบนหน้า Search (2 คอลัมน์ / การ์ดใหญ่ / Mobile) ส่วน `number-card.css` เป็นต้นฉบับจาก Kit ที่ได้รับมา

## เปลี่ยนข้อมูลบนการ์ด
ข้อมูลมาจาก `web/app.js` ฟังก์ชัน `loadResults()` เรียก API `/api/search` แล้วส่ง object ให้ `NineMongkolNumberCard.render()` โดยใช้ `phone`, `score`, `price`, `status`, `source` ตามผลจริงของระบบ

## ไอคอนที่ใช้
`web/number-card/icons/` มี SVG จาก Kit 9 ไฟล์ โดย Component เรียกตาม `assetBase` ที่คำนวณจากลิงก์ CSS ในหน้า จึงทำงานทั้งเมื่อเปิดไฟล์ `index.html` และเมื่อใช้ FastAPI

## พฤติกรรมปุ่ม
CTA `ดูรายละเอียด` ใช้ event delegation เดิมเพื่อเปิดรายงานวิเคราะห์ของเบอร์ที่เลือก และไม่พาไปลิงก์ตัวอย่างของ Kit

## เลือกขนาดการ์ด
ผู้เข้าชมคลิกปุ่ม `สองคอลัมน์` หรือ `การ์ดใหญ่` เหนือรายการเบอร์ ไม่เปลี่ยนข้อมูลผลค้นหา (บนมือถือระบบเป็น 1 คอลัมน์อัตโนมัติ)

## ทดสอบ
`PYTHONPATH=. pytest -q`
ใช้ `python scripts/build_offline.py` หากแก้ฐานข้อมูลและต้องการสร้าง Offline Snapshot ใหม่
