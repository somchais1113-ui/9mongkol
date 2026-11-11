# 9มงคล — Typography Guideline v0.8

## เป้าหมาย
เว็บไซต์อ่านได้สบายขึ้นสำหรับกลุ่มผู้ใช้วัยทำงาน 30–40 ปี โดยไม่เปลี่ยนแบรนด์ Crimson/Gold หรือ Rule Engine

| ชนิดข้อความ | Desktop | Mobile | หมายเหตุ |
|---|---:|---:|---|
| เนื้อหา / คำอธิบายหลัก | 17px | 16px | Line-height 1.65–1.8 |
| ข้อความผลวิเคราะห์ / คำแนะนำ | 16px | 16px | แสดงที่มาและข้อจำกัดได้ชัด |
| Labels / Status / Secondary | 14–16px | 14–16px | หลีกเลี่ยง 9–11px ที่เดิมอ่านลำบาก |
| ปุ่มและ Form Input | 16–17px | 16–17px | ช่องกดสูงอย่างน้อยประมาณ 44px |
| Section Heading | 26–36px | 29px | Responsive typography |
| Page Heading | 32–45px | 30–37px | บรรทัดและช่องไฟอ่านง่าย |

### วิธีแก้
1. แก้เฉพาะ `web/nine-readable.css` ซึ่งถูกโหลดท้ายสุดทั้งหน้า Backend/Offline
2. ตรวจสอบที่ 1440px, 1024px, 390px, 320px ก่อนส่งจริง
3. รัน `python3 scripts/build_offline.py` ทุกครั้งหลังปรับ CSS/HTML เพื่อคง Sync กับ `index.html` ที่ root
4. รัน `PYTHONPATH=. pytest -q` และหากติดตั้ง Playwright ให้รัน `python3 scripts/qa_typography.py`

## ระวัง
- ข้อความไม่ควรถูกย่อเพื่อประหยัดพื้นที่บนมือถือ ให้เปลี่ยน Layout เป็นแนวตั้งแทน
- รักษา Contrast ระหว่างสีเบอร์กันดี/คำเตือนกับพื้นหลัง และหลีกเลี่ยง Blur บนข้อความ
- ห้ามใช้ transform scale เพื่อหลอกให้ฟอนต์ใหญ่ขึ้น เพราะอาจทำให้ข้อความเบลอ
- นี่เป็นแนวทาง Typography ไม่ใช่ผลตรวจรับรอง WCAG ทุกเกณฑ์
