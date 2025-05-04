# Durian Marketing Analytics Web

ระบบวิเคราะห์แคมเปญการตลาดทุเรียน

## คำอธิบาย
เว็บไซต์สำหรับวิเคราะห์ข้อความ รีวิว หรือความคิดเห็นเกี่ยวกับทุเรียน โดยใช้ AI วิเคราะห์ความรู้สึก (Sentiment Analysis) ดึงคำสำคัญ แสดงแนวโน้ม และให้คำแนะนำสำหรับแคมเปญการตลาด

- วิเคราะห์ข้อความภาษาไทยได้
- แสดงผลเป็นกราฟและสถิติที่เข้าใจง่าย
- เก็บประวัติการวิเคราะห์ใน browser (localStorage)
- สามารถดูรายละเอียดและลบประวัติแต่ละรายการได้

## Features
- Sentiment Analysis (Positive / Neutral / Negative)
- Keyword Extraction
- Trend Visualization (Mock)
- Campaign Suggestions
- History with detail modal & delete

## วิธีใช้งาน
1. เปิดไฟล์ `index.html` ด้วย browser
2. กรอกข้อความที่ต้องการวิเคราะห์ แล้วกด "วิเคราะห์ข้อความ"
3. ดูผลวิเคราะห์และสถิติต่าง ๆ
4. ดูประวัติการวิเคราะห์ย้อนหลังที่หน้า "ประวัติการวิเคราะห์"

## การติดตั้ง/รัน
- ไม่ต้องติดตั้ง backend หรือ database ใด ๆ
- ใช้งานได้ทันทีบน browser ที่รองรับ JavaScript

## โครงสร้างไฟล์หลัก
- `index.html` — หน้าเว็บหลักสำหรับวิเคราะห์ข้อความ
- `history.html` — หน้าแสดงประวัติการวิเคราะห์
- `style.css` — ไฟล์ตกแต่งหน้าตาเว็บไซต์
- `logo.png` — โลโก้เว็บไซต์

## License
MIT

---

# Durian Marketing Analytics Web

A simple web app for Thai durian marketing campaign analytics.

## Features
- Sentiment analysis (Thai language)
- Keyword extraction
- Trend visualization (mock)
- Campaign suggestions
- History with detail modal & delete

## Usage
1. Open `index.html` in your browser
2. Enter text and click "วิเคราะห์ข้อความ" (Analyze)
3. View results and statistics
4. See analysis history in "ประวัติการวิเคราะห์" (History)

## No backend required
All data is stored in browser localStorage.

## Main files
- `index.html`
- `history.html`
- `style.css`
- `logo.png`

## License
MIT 