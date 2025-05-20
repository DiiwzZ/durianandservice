# คู่มือการใช้งาน WangchanBERTa สำหรับการวิเคราะห์ความรู้สึกเกี่ยวกับทุเรียน

## เกี่ยวกับ WangchanBERTa

WangchanBERTa เป็นโมเดลภาษาไทยที่พัฒนาโดยสถาบันวิจัยปัญญาประดิษฐ์ประเทศไทย (AI Research Thailand) โดยถูกพัฒนาบนพื้นฐานของสถาปัตยกรรม BERT แต่ได้รับการฝึกฝนด้วยข้อมูลภาษาไทยขนาดใหญ่ มีความสามารถในการเข้าใจบริบทของภาษาไทยได้ดีกว่าโมเดลทั่วไป ทำให้เหมาะสำหรับงานประมวลผลภาษาไทยหลายประเภท เช่น การวิเคราะห์ความรู้สึก การจำแนกหมวดหมู่ข้อความ และการตอบคำถาม

### ข้อดีของ WangchanBERTa สำหรับการวิเคราะห์ความรู้สึกเกี่ยวกับทุเรียน

1. **เข้าใจบริบทภาษาไทย**: WangchanBERTa เข้าใจโครงสร้างประโยคและความหมายของคำในภาษาไทยได้ดี
2. **รองรับคำศัพท์เฉพาะทาง**: สามารถเข้าใจคำศัพท์เฉพาะเกี่ยวกับทุเรียน เช่น พันธุ์ทุเรียน, ลักษณะเนื้อ, กลิ่น ฯลฯ
3. **ประสิทธิภาพสูง**: ให้ความแม่นยำในการวิเคราะห์ความรู้สึกของข้อความภาษาไทยได้ดี
4. **สามารถ Fine-tune**: สามารถปรับแต่งโมเดลเพิ่มเติมให้เหมาะกับข้อมูลเฉพาะทางได้

## การติดตั้ง

ก่อนใช้งานโมเดล WangchanBERTa คุณจำเป็นต้องติดตั้งแพ็คเกจที่เกี่ยวข้อง:

```bash
pip install torch transformers pythainlp scikit-learn pandas
```

## การใช้งานแบบง่าย

### 1. การใช้งานโมเดลโดยตรง

หากต้องการใช้งาน WangchanBERTa โดยตรงโดยไม่ผ่านการ Fine-tune:

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# โหลดโมเดลและ tokenizer
tokenizer = AutoTokenizer.from_pretrained("airesearch/wangchanberta-base-att-spm-uncased")
model = AutoModelForSequenceClassification.from_pretrained("airesearch/wangchanberta-base-att-spm-uncased", num_labels=3)
model.eval()  # ตั้งค่าโมเดลให้อยู่ในโหมดประเมินผล

# ฟังก์ชันสำหรับวิเคราะห์ความรู้สึก
def analyze_sentiment(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=128)
    with torch.no_grad():
        outputs = model(**inputs)
        scores = torch.nn.functional.softmax(outputs.logits, dim=1)
        prediction = torch.argmax(scores, dim=1).item()
    
    # แปลงผลลัพธ์
    sentiment = ["positive", "neutral", "negative"][prediction]
    confidence = scores[0][prediction].item()
    
    return {
        "sentiment": sentiment,
        "confidence": confidence,
        "scores": {
            "positive": scores[0][0].item(),
            "neutral": scores[0][1].item(),
            "negative": scores[0][2].item()
        }
    }

# ทดสอบ
result = analyze_sentiment("ทุเรียนนี้หวานมาก อร่อยสุดๆ")
print(result)
```

### 2. การใช้งาน AI Service สำหรับวิเคราะห์ความรู้สึก

1. เริ่มต้น AI Service โดยรันคำสั่ง:
   ```bash
   python ai_service_with_wangchanberta.py
   ```

2. เรียกใช้งาน API ผ่าน HTTP request:
   ```bash
   curl -X POST -H "Content-Type: application/json" -d "{\"text\":\"ทุเรียนนี้หวานมาก อร่อยสุดๆ\"}" http://localhost:5000/analyze
   ```

3. หรือใช้งานผ่านเว็บแอปพลิเคชัน โดยเปิดไฟล์ `index.html` ในเบราว์เซอร์

## การ Fine-tune โมเดล

หากต้องการปรับแต่งโมเดลให้เข้ากับข้อมูลเฉพาะทางมากขึ้น สามารถทำการ Fine-tune โดยใช้สคริปต์ `finetune_script.py`:

```bash
python finetune_script.py --data_path durian_sentiment_additional.csv --epochs 3 --batch_size 8
```

พารามิเตอร์ที่สามารถปรับแต่งได้:
- `--data_path`: พาธไปยังไฟล์ข้อมูล CSV (จำเป็นต้องมีคอลัมน์ 'text' และ 'label')
- `--model_name`: ชื่อโมเดลพื้นฐาน (ค่าเริ่มต้น: airesearch/wangchanberta-base-att-spm-uncased)
- `--output_dir`: โฟลเดอร์สำหรับบันทึกโมเดล (ค่าเริ่มต้น: ./durian-sentiment-model)
- `--epochs`: จำนวนรอบการฝึกสอน (ค่าเริ่มต้น: 3)
- `--batch_size`: ขนาด batch (ค่าเริ่มต้น: 8)

**หมายเหตุ**: หากคุณมี GPU คุณสามารถใช้ GPU เพื่อเร่งความเร็วในการฝึกสอนโมเดลได้โดยอัตโนมัติ

## การใช้งานโมเดลที่ผ่านการ Fine-tune

หลังจาก Fine-tune โมเดลแล้ว คุณสามารถใช้งานโมเดลที่ Fine-tune แล้วได้โดยเปลี่ยนพาธของโมเดลใน `ai_service_with_wangchanberta.py`:

```python
# เปลี่ยนจาก
MODEL_NAME = "airesearch/wangchanberta-base-att-spm-uncased"
# เป็น
MODEL_NAME = "./durian-sentiment-model"
```

จากนั้นรันคำสั่ง:
```bash
python ai_service_with_wangchanberta.py
```

## เทคนิคการเพิ่มประสิทธิภาพ

1. **เพิ่มข้อมูลฝึกสอน**: ยิ่งมีข้อมูลในการ Fine-tune มากเท่าไหร่ ประสิทธิภาพของโมเดลจะยิ่งดีขึ้น
2. **ทำความสะอาดข้อมูล**: ตรวจสอบและแก้ไขข้อมูลที่มีความผิดพลาดก่อนนำไป Fine-tune
3. **ปรับพารามิเตอร์**: ลองปรับค่าพารามิเตอร์ต่างๆ เช่น learning rate, batch size, epochs เพื่อหาค่าที่เหมาะสมที่สุด
4. **แบ่งข้อมูลอย่างเหมาะสม**: ควรแบ่งข้อมูลเป็นชุดฝึกสอน (training), ชุดตรวจสอบความถูกต้อง (validation) และชุดทดสอบ (test) ในสัดส่วนที่เหมาะสม

## การแก้ไขปัญหาที่พบบ่อย

1. **ปัญหา "CUDA out of memory"**: ลดขนาด batch หรือความยาวของข้อความสูงสุด
2. **ความแม่นยำต่ำ**: เพิ่มข้อมูลฝึกสอนหรือปรับแต่งพารามิเตอร์
3. **โมเดลประมวลผลช้า**: ใช้ GPU หากมี หรือลดความซับซ้อนของโมเดล
4. **ข้อความภาษาไทยแสดงผลไม่ถูกต้อง**: ตรวจสอบการเข้ารหัสตัวอักษรให้เป็น UTF-8

## แหล่งข้อมูลเพิ่มเติม

- [เว็บไซต์ WangchanBERTa](https://airesearch.in.th/releases/wangchanberta-pre-trained-thai-language-model/)
- [GitHub ของ AI Research Thailand](https://github.com/vistec-AI/thai2transformers)
- [เอกสารอ้างอิง Hugging Face Transformers](https://huggingface.co/docs/transformers/index)

## ผู้พัฒนา

พัฒนาโดยทีมวิเคราะห์การตลาดทุเรียน ใช้เทคโนโลยี WangchanBERTa จาก AI Research Thailand

## ลิขสิทธิ์

การใช้งาน WangchanBERTa อยู่ภายใต้ลิขสิทธิ์ของ AI Research Thailand 