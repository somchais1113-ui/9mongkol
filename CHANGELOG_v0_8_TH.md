# Changelog v0.8 — Readability Edition (11 พ.ย. 2026)

- ขยายรายละเอียดจาก 9–13px ให้เป็น 14–17px ตามหน้าที่การใช้งาน
- ปรับ Form Input / Filter / Number Card / Career Matrix / Rule Library / Import Dialog / Modal และ Chart Report
- เพิ่มความสูงของปุ่มและช่องกรอกที่ใช้บ่อยเป็นประมาณ 44–56px
- ปรับระยะบรรทัด, ลำดับหัวข้อ, ระยะห่างและกริด Mobile
- แก้ CSS เดิมที่ override ขนาดย่อยเหลือ 11px ในหน้ารายงาน
- ทำ Announce Bar มือถือไม่บีบชื่อ 9มงคลจนตัดบรรทัด
- เปลี่ยนฟอร์มวิเคราะห์ที่ 480px ลงมาเป็นหนึ่งคอลัมน์หลังมีผลการวิเคราะห์
- คง Brand Asset, Sacred Luxury Motion, Career Matching/Rule Engine และตัวอย่าง 420 เบอร์เดิม
- สร้าง Offline index.html ใหม่ที่ลิงก์ CSS v0.8 และ Backend cache busting

QA: Automated unit tests 15 ผ่าน; ตรวจ browser จำลอง 1440, 1024, 390, 320px ไม่มี horizontal overflow, ไม่มี JS exceptions ใน flow ค้นหา/วิเคราะห์; นี่ไม่ใช่การรับรอง WCAG ตามมาตรฐานทุกข้อ
