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

## การใช้งาน WangchanBERTa

WangchanBERTa เป็นโมเดลภาษาขนาดใหญ่สำหรับภาษาไทยที่พัฒนาโดย AI Research Thailand ซึ่งสามารถนำมาประยุกต์ใช้กับการวิเคราะห์ข้อความภาษาไทยได้หลากหลายรูปแบบ

### การติดตั้ง

1. ติดตั้ง Python (เวอร์ชัน 3.8 หรือสูงกว่า)
2. สร้าง Virtual Environment:
```
python -m venv .venv
```
3. เปิดใช้งาน Virtual Environment:
   - Windows:
   ```
   .venv\Scripts\activate
   ```
   - macOS/Linux:
   ```
   source .venv/bin/activate
   ```
4. ติดตั้งแพ็คเกจที่จำเป็น:
```
pip install -r requirements.txt
```

### การรัน API Server

1. รันเซิร์ฟเวอร์:
```
python ai_service.py
```
2. เซิร์ฟเวอร์จะทำงานที่ http://localhost:5000

### การติดตั้ง API Server เป็น Service เพื่อให้ทำงานตลอดเวลา

เพื่อให้ API Server ทำงานตลอดเวลาแม้จะปิดหน้าต่างคำสั่งหรือรีสตาร์ทเครื่อง คุณสามารถติดตั้งเป็น Windows Service ได้ดังนี้:

#### สำหรับ Windows

1. **ติดตั้ง NSSM (Non-Sucking Service Manager)**:
   - ดาวน์โหลด NSSM จาก [https://nssm.cc/download](https://nssm.cc/download)
   - แตกไฟล์และคัดลอกไฟล์ `nssm.exe` (จากโฟลเดอร์ที่ตรงกับสถาปัตยกรรมของเครื่อง เช่น win64) ไปยังโฟลเดอร์ที่มีไฟล์ `install_service.bat` หรือเพิ่มไปยัง PATH

2. **ใช้สคริปต์ติดตั้งอัตโนมัติ**:
   - เปิด Command Prompt หรือ PowerShell ในโหมด Administrator
   - รันไฟล์ `install_service.bat`
   ```
   install_service.bat
   ```
   - ทำตามคำแนะนำบนหน้าจอเพื่อติดตั้งและเริ่มต้น service

3. **วิธีจัดการ Service**:
   - เริ่มต้น Service: `nssm start DurianAnalyticsService` หรือผ่าน Services Manager ของ Windows
   - หยุด Service: `nssm stop DurianAnalyticsService`
   - ดูสถานะ: `nssm status DurianAnalyticsService`
   - ถอนการติดตั้ง: รันไฟล์ `uninstall_service.bat`

4. **ตรวจสอบบันทึกการทำงาน (Logs)**:
   บันทึกการทำงานจะถูกเก็บไว้ในโฟลเดอร์ `logs`:
   - `service.log`: บันทึกการทำงานทั่วไป
   - `error.log`: บันทึกข้อผิดพลาด

#### สำหรับ Linux

1. **สร้างไฟล์ Service**:
   สร้างไฟล์ `/etc/systemd/system/durian-analytics.service`:
   ```
   [Unit]
   Description=Durian Analytics Service
   After=network.target

   [Service]
   User=<your-username>
   WorkingDirectory=/path/to/durian
   ExecStart=/path/to/durian/.venv/bin/python /path/to/durian/ai_service.py
   Restart=always
   RestartSec=10

   [Install]
   WantedBy=multi-user.target
   ```
   แทนที่ `<your-username>` และ `/path/to/durian` ด้วยค่าที่ถูกต้อง

2. **เริ่มใช้งาน Service**:
   ```
   sudo systemctl enable durian-analytics.service
   sudo systemctl start durian-analytics.service
   ```

3. **ตรวจสอบสถานะ**:
   ```
   sudo systemctl status durian-analytics.service
   ```

4. **ดูบันทึกการทำงาน**:
   ```
   sudo journalctl -u durian-analytics.service
   ```

### การใช้งานบนหน้าเว็บ

1. เปิดไฟล์ `index.html` ในเบราว์เซอร์
2. ไปที่ส่วน "วิเคราะห์ความคิดเห็นด้วย WangchanBERTa"
3. พิมพ์ข้อความที่ต้องการวิเคราะห์
4. กดปุ่ม "วิเคราะห์" เพื่อส่งข้อความไปยังเซิร์ฟเวอร์และรับผลลัพธ์

### ตัวอย่างการนำไปประยุกต์ใช้

1. **การวิเคราะห์ความรู้สึก (Sentiment Analysis)**: ใช้วิเคราะห์ความคิดเห็นของลูกค้าว่าเป็นเชิงบวก เชิงลบ หรือเป็นกลาง
2. **การจำแนกหมวดหมู่ (Text Classification)**: ใช้จำแนกข้อความทุเรียนเป็นหมวดหมู่ต่างๆ เช่น คุณภาพ, ราคา, รสชาติ
3. **การตอบคำถาม (Question Answering)**: ใช้ตอบคำถามเกี่ยวกับทุเรียนโดยอัตโนมัติ

### การปรับปรุงโมเดล (Fine-tuning)

หากต้องการปรับแต่งโมเดลให้เหมาะกับงานเฉพาะทาง สามารถทำได้โดย:

1. เตรียมชุดข้อมูลฝึกสอนเฉพาะทาง (Domain-specific dataset)
2. ใช้โค้ดตัวอย่างในการ Fine-tune:
```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
import torch

# โหลดโมเดลพื้นฐาน
tokenizer = AutoTokenizer.from_pretrained("airesearch/wangchanberta-base-att-spm-uncased")
model = AutoModelForSequenceClassification.from_pretrained("airesearch/wangchanberta-base-att-spm-uncased", num_labels=3)

# กำหนดค่าการฝึกสอน
training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir="./logs",
)

# กำหนด Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,  # ต้องเตรียมชุดข้อมูลฝึกสอน
    eval_dataset=eval_dataset     # ต้องเตรียมชุดข้อมูลทดสอบ
)

# ฝึกสอนโมเดล
trainer.train()

# บันทึกโมเดลที่ fine-tune แล้ว
model.save_pretrained("./durian-sentiment-model")
tokenizer.save_pretrained("./durian-sentiment-model")
```

### ทรัพยากรเพิ่มเติม

- [WangchanBERTa GitHub](https://github.com/vistec-AI/thai2transformers)
- [HuggingFace WangchanBERTa](https://huggingface.co/airesearch/wangchanberta-base-att-spm-uncased)
- [AI Research Thailand](https://airesearch.in.th/) 