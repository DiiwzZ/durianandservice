from flask import Flask, request, jsonify
from flask_cors import CORS
import torch
import os
import sys
from pythainlp.tokenize import word_tokenize

# ตัวแปรกำหนดว่ากำลังใช้โมเดล (True) หรือวิธีการวิเคราะห์แบบกฎ (False)
use_model = False
tokenizer = None
model = None

app = Flask(__name__)
CORS(app)  # เพิ่ม CORS เพื่อให้สามารถเรียกใช้จากหน้าเว็บได้

# โหลดโมเดล WangchanBERTa ถ้า use_model เป็น True
if use_model:
    try:
        from transformers import AutoTokenizer, AutoModelForSequenceClassification
        print("กำลังโหลด WangchanBERTa...")
        MODEL_NAME = "airesearch/wangchanberta-base-att-spm-uncased"
        # จำเป็นต้องระบุ use_fast=False เพื่อหลีกเลี่ยงปัญหากับ SentencePiece
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_fast=False)
        # Fine-tune โมเดลสำหรับการวิเคราะห์ความรู้สึก (3 คลาส: positive, neutral, negative)
        model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=3)
        model.eval()  # ตั้งค่าโมเดลให้อยู่ในโหมดประเมินผล
        print("โหลดโมเดลสำเร็จ")
    except Exception as e:
        print(f"เกิดข้อผิดพลาดในการโหลดโมเดล: {str(e)}")
        print("จะใช้วิธีการตรวจสอบคำแทนการใช้โมเดล")
        use_model = False

# คลังคำสำหรับการแยกคำในการวิเคราะห์แบบละเอียด
positive_words = [
    "อร่อย", "ดี", "หวาน", "สด", "คุณภาพดี", "ชอบ", "หอม", "อร่อยมาก", 
    "นุ่ม", "ละมุน", "หอมหวาน", "สุก", "พอดี", "นิ่ม", "เนื้อแน่น", "เยี่ยม", 
    "ประทับใจ", "อร่อยมากๆ", "มีคุณภาพ", "คุ้มค่า", "ถูกใจ", "น่าทาน"
]

negative_words = [
    "แพง", "แย่", "เน่า", "เสีย", "ไม่อร่อย", "ไม่ชอบ", "แข็ง", "ไม่สด", "กลิ่นแรง",
    "แพงเกินไป", "ไม่คุ้ม", "ไม่คุ้มราคา", "เละ", "เน่าเสีย", "เสียเร็ว", "ช้า", 
    "ล่าช้า", "ส่งช้า", "เสียหาย", "ผิดหวัง", "แย่มาก"
]

neutral_words = [
    "ราคา", "ขนส่ง", "ขนาด", "กิโล", "น้ำหนัก", "ทุเรียน", "กวน", 
    "ส่ง", "ส่งมา", "ได้รับ", "สั่ง", "จัดส่ง", "อายุ", "วันหมดอายุ", "เลือก"
]

durian_types = [
    "หมอนทอง", "ชะนี", "ก้านยาว", "พวงมณี", "กระดุม", "อีกรอบ", "หลงลับแล",
    "หลินลับแล", "ทองย้อย", "ทุเรียนกวน", "ทุเรียนทอด"
]

# ตัวแปรสำหรับการแปลงความรู้สึกจากตัวเลขเป็นข้อความ
id_to_sentiment = {
    0: "positive",  # เชิงบวก
    1: "neutral",   # เป็นกลาง
    2: "negative"   # เชิงลบ
}

# ตัวแปรสำหรับการแปลงความรู้สึกเป็นภาษาไทย
sentiment_map = {
    'positive': 'เชิงบวก (Positive)',
    'negative': 'เชิงลบ (Negative)',
    'neutral': 'เป็นกลาง (Neutral)'
}

def predict_sentiment_with_rules(text):
    """
    ใช้วิธีการตรวจสอบคำสำคัญในการวิเคราะห์ความรู้สึกของข้อความ
    
    Parameters:
    text (str): ข้อความที่ต้องการวิเคราะห์
    
    Returns:
    dict: ผลการวิเคราะห์ความรู้สึกของข้อความ
    """
    words = word_tokenize(text, engine='newmm')
    
    # ค้นหาคำเชิงบวก เชิงลบ และเป็นกลาง
    found_positive_words = [word for word in words if any(pos_word in word for pos_word in positive_words)]
    found_negative_words = [word for word in words if any(neg_word in word for neg_word in negative_words)]
    found_neutral_words = [word for word in words if any(neu_word in word for neu_word in neutral_words)]
    found_durian_types = [word for word in words if any(dtype in word for dtype in durian_types)]
    
    # นับจำนวนคำเพื่อตัดสินความรู้สึก
    pos_count = len(found_positive_words)
    neg_count = len(found_negative_words)
    neu_count = len(found_neutral_words)
    
    # คำนวณเปอร์เซ็นต์ความรู้สึก
    total = pos_count + neg_count + neu_count
    if total == 0:
        total = 1  # ป้องกันการหารด้วยศูนย์
    
    pos_ratio = pos_count / total
    neg_ratio = neg_count / total
    neu_ratio = neu_count / total
    
    # ตัดสินความรู้สึก
    if pos_count > neg_count:
        sentiment = "positive"
        confidence = 0.5 + (pos_ratio * 0.5)
    elif neg_count > pos_count:
        sentiment = "negative"
        confidence = 0.5 + (neg_ratio * 0.5)
    else:
        sentiment = "neutral"
        confidence = 0.5 + (neu_ratio * 0.5)
    
    sentiment_ratios = {
        "positive": pos_ratio,
        "neutral": neu_ratio,
        "negative": neg_ratio
    }
    
    return {
        "text": text,
        "sentiment": sentiment,
        "sentiment_text": sentiment_map[sentiment],
        "confidence": confidence,
        "details": {
            "scores": {
                "positive": pos_ratio,
                "neutral": neu_ratio,
                "negative": neg_ratio
            },
            "sentiment_ratios": sentiment_ratios,
            "found_positive_words": found_positive_words,
            "found_negative_words": found_negative_words,
            "found_neutral_words": found_neutral_words,
            "found_durian_types": found_durian_types,
            "tokenized_words": words
        }
    }

def predict_sentiment_with_wangchanberta(text):
    """
    ใช้โมเดล WangchanBERTa ในการวิเคราะห์ความรู้สึกของข้อความ
    
    Parameters:
    text (str): ข้อความที่ต้องการวิเคราะห์
    
    Returns:
    dict: ผลการวิเคราะห์ความรู้สึกของข้อความ
    """
    if not use_model:
        return predict_sentiment_with_rules(text)
    
    try:
        # tokenize ข้อความ
        encoded_input = tokenizer(
            text,
            truncation=True,
            padding="max_length",
            max_length=128,
            return_tensors="pt"
        )
        
        # วิเคราะห์ความรู้สึก
        with torch.no_grad():
            output = model(**encoded_input)
            scores = torch.nn.functional.softmax(output.logits, dim=1)
            prediction = torch.argmax(scores, dim=1).item()
        
        # คำนวณความเชื่อมั่น
        confidence = scores[0][prediction].item()
        
        # แปลงผลลัพธ์เป็น sentiment
        sentiment = id_to_sentiment[prediction]
        
        # แยกคำเพื่อวิเคราะห์เพิ่มเติม
        words = word_tokenize(text, engine='newmm')
        
        # ค้นหาคำเชิงบวก เชิงลบ และเป็นกลาง
        found_positive_words = [word for word in words if any(pos_word in word for pos_word in positive_words)]
        found_negative_words = [word for word in words if any(neg_word in word for neg_word in negative_words)]
        found_neutral_words = [word for word in words if any(neu_word in word for neu_word in neutral_words)]
        found_durian_types = [word for word in words if any(dtype in word for dtype in durian_types)]
        
        # คำนวณเปอร์เซ็นต์ความรู้สึก
        sentiment_ratios = {
            "positive": scores[0][0].item(),
            "neutral": scores[0][1].item(),
            "negative": scores[0][2].item()
        }
        
        return {
            "text": text,
            "sentiment": sentiment,
            "sentiment_text": sentiment_map[sentiment],
            "confidence": confidence,
            "details": {
                "scores": {
                    "positive": scores[0][0].item(),
                    "neutral": scores[0][1].item(),
                    "negative": scores[0][2].item()
                },
                "sentiment_ratios": sentiment_ratios,
                "found_positive_words": found_positive_words,
                "found_negative_words": found_negative_words,
                "found_neutral_words": found_neutral_words,
                "found_durian_types": found_durian_types,
                "tokenized_words": words
            }
        }
    except Exception as e:
        print(f"เกิดข้อผิดพลาดในการวิเคราะห์ด้วยโมเดล: {str(e)}")
        print("ใช้วิธีการตรวจสอบคำแทน")
        return predict_sentiment_with_rules(text)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    text = data.get('text', '')
    
    if not text:
        return jsonify({"error": "ไม่มีข้อความที่ต้องการวิเคราะห์"}), 400
    
    try:
        result = predict_sentiment_with_wangchanberta(text)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": f"เกิดข้อผิดพลาด: {str(e)}"}), 500

if __name__ == '__main__':
    print("กำลังเริ่มต้นเซิร์ฟเวอร์วิเคราะห์ความรู้สึกทุเรียน...")
    if use_model:
        print(f"ใช้โมเดล: {MODEL_NAME}")
    else:
        print("ใช้วิธีการตรวจสอบคำแทนโมเดล (เนื่องจากโหลดโมเดลไม่สำเร็จ)")
    app.run(debug=True, port=5000) 