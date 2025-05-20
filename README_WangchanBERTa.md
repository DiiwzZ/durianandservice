# การใช้งาน WangchanBERTa สำหรับวิเคราะห์ความรู้สึกเกี่ยวกับทุเรียน

เอกสารนี้อธิบายวิธีการติดตั้งและใช้งาน WangchanBERTa สำหรับการวิเคราะห์ความรู้สึกของข้อความภาษาไทยเกี่ยวกับทุเรียน เพื่อนำไปใช้ในเว็บไซต์วิเคราะห์แคมเปญการตลาดทุเรียน

## การติดตั้ง

1. ติดตั้งแพ็คเกจที่จำเป็นโดยใช้ไฟล์สคริปต์ที่เหมาะสมกับระบบของคุณ:

   - สำหรับ Windows:
   ```
   install_dependencies.bat
   ```

   - สำหรับ Linux/Mac:
   ```
   chmod +x install_dependencies.sh
   ./install_dependencies.sh
   ```

2. หากไม่ต้องการใช้สคริปต์ คุณสามารถติดตั้งด้วยตัวเองตามลำดับดังนี้:

```bash
# สร้างและเปิดใช้งาน virtual environment
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate

# อัปเกรด pip
pip install --upgrade pip

# ติดตั้ง tokenizers ก่อนเพื่อหลีกเลี่ยงปัญหา Rust compiler
pip install tokenizers --no-build-isolation

# ติดตั้ง sentencepiece
pip install sentencepiece>=0.1.99

# ติดตั้ง transformers เวอร์ชันเฉพาะ
pip install transformers==4.30.2 --no-deps

# ติดตั้งแพ็คเกจที่เกี่ยวข้องกับ transformers
pip install accelerate safetensors

# ติดตั้งแพ็คเกจอื่นๆ
pip install torch>=2.0.0 pythainlp>=4.0.2 flask>=2.3.3 flask-cors>=4.0.0 numpy>=1.24.3 pandas>=2.0.3
```

## การทดสอบโมเดล

คุณสามารถทดสอบการทำงานของโมเดล WangchanBERTa ได้ง่ายๆ ด้วยคำสั่ง:

```bash
python workaround_test.py
```

สคริปต์นี้จะทดสอบ:
1. การตรวจสอบแพ็คเกจที่จำเป็น
2. การโหลด tokenizer แบบปกติและแบบ use_fast=False
3. การโหลดโมเดลสำหรับวิเคราะห์ความรู้สึก
4. การทดสอบการวิเคราะห์ข้อความตัวอย่าง

## การใช้งาน API

เริ่มต้น API สำหรับวิเคราะห์ความรู้สึกด้วยคำสั่ง:

```bash
python ai_service_with_wangchanberta.py
```

API จะทำงานที่ http://localhost:5000 และมีเอนด์พอยต์หลักดังนี้:

- **POST /analyze**: ใช้สำหรับวิเคราะห์ความรู้สึกของข้อความ
  - ตัวอย่าง request:
  ```json
  {
    "text": "ทุเรียนหมอนทองนี้หวานมาก อร่อยสุดๆ"
  }
  ```
  - ตัวอย่าง response:
  ```json
  {
    "text": "ทุเรียนหมอนทองนี้หวานมาก อร่อยสุดๆ",
    "sentiment": "positive",
    "sentiment_text": "เชิงบวก (Positive)",
    "confidence": 0.95,
    "details": {
      "scores": {
        "positive": 0.92,
        "neutral": 0.05,
        "negative": 0.03
      },
      "found_positive_words": ["หวาน", "อร่อย"],
      "found_negative_words": [],
      "found_neutral_words": [],
      "found_durian_types": ["หมอนทอง"]
    }
  }
  ```

## การ Fine-tune โมเดล

หากคุณต้องการปรับปรุงโมเดลให้เหมาะกับข้อมูลทุเรียนมากขึ้น คุณสามารถ fine-tune โมเดลได้ด้วยคำสั่ง:

```bash
python finetune_script.py --data_path durian_sentiment_additional.csv
```

พารามิเตอร์ที่สามารถปรับได้:
- `--data_path`: พาธไปยังไฟล์ข้อมูล CSV (ต้องมีคอลัมน์ "text" และ "label")
- `--model_name`: ชื่อโมเดล pre-trained (ค่าเริ่มต้น: "airesearch/wangchanberta-base-att-spm-uncased")
- `--output_dir`: โฟลเดอร์สำหรับบันทึกโมเดล (ค่าเริ่มต้น: "./durian-sentiment-model")
- `--epochs`: จำนวนรอบการฝึกสอน (ค่าเริ่มต้น: 3)
- `--batch_size`: ขนาด batch (ค่าเริ่มต้น: 8, ลดลงถ้า RAM/VRAM ไม่พอ)

## รูปแบบข้อมูลสำหรับ Fine-tune

ไฟล์ CSV สำหรับ fine-tune ต้องมีคอลัมน์ดังนี้:
- `text`: ข้อความภาษาไทยเกี่ยวกับทุเรียน
- `label`: ป้ายกำกับความรู้สึก (0=positive, 1=neutral, 2=negative)

ตัวอย่าง:
```
text,label
ทุเรียนหมอนทองนี้หวานมาก อร่อยสุดๆ,0
ทุเรียนราคาแพงเกินไป ไม่คุ้มค่าเลย,2
ทุเรียนส่งมาช้ามาก ไม่พอใจ,2
ทุเรียนคุณภาพดี ราคาเหมาะสม,0
```

## การแก้ไขปัญหาที่พบบ่อย

1. **ปัญหา "Converting from SentencePiece and Tiktoken failed"**
   - แก้ไขโดยการเพิ่ม `use_fast=False` เมื่อโหลด tokenizer:
   ```python
   tokenizer = AutoTokenizer.from_pretrained("airesearch/wangchanberta-base-att-spm-uncased", use_fast=False)
   ```
   - ตรวจสอบว่าได้ติดตั้ง sentencepiece เวอร์ชัน 0.1.99 ขึ้นไป

2. **ปัญหา "ImportError: DLL load failed" หรือ "rust compiler not installed"**
   - ติดตั้ง tokenizers โดยไม่สร้างจาก source:
   ```bash
   pip install tokenizers --no-build-isolation
   ```
   - ใช้ตัวเลือก use_fast=False เมื่อโหลด tokenizer จาก transformers

3. **ปัญหาความเข้ากันได้ของ transformers**
   - ถอนการติดตั้ง transformers แล้วติดตั้งใหม่:
   ```bash
   pip uninstall -y transformers
   pip install transformers==4.30.2 --no-deps
   pip install accelerate safetensors
   ```

4. **ปัญหาเมื่อใช้งาน API**
   - ตรวจสอบว่า Flask และ Flask-CORS ทำงานถูกต้อง
   - ตรวจสอบว่า request เป็น JSON format ที่ถูกต้อง
   - ตรวจสอบว่ามีฟิลด์ "text" ในข้อมูล request

5. **ปัญหาเมื่อ fine-tune โมเดล**
   - ตรวจสอบว่ากำหนด eval_strategy แทน evaluation_strategy ในไฟล์ finetune_script.py
   - ลด batch_size ลงหากมีปัญหาเรื่องหน่วยความจำ
   - หากเกิดปัญหากับ CUDA: `torch.cuda.is_available()` ให้ใช้ CPU แทน
   ```python
   device = "cpu"  # แทนที่จะใช้ "cuda"
   ``` 