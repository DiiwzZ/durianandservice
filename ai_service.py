from flask import Flask, request, jsonify
from flask_cors import CORS
from pythainlp.tokenize import word_tokenize

app = Flask(__name__)
CORS(app)  # เพิ่ม CORS เพื่อให้สามารถเรียกใช้จากหน้าเว็บได้

def sentiment_analysis(text):
    """
    วิเคราะห์ความรู้สึกของข้อความแบบง่ายๆ
    """
    # คลังคำเชิงบวกขยายเพิ่ม
    positive_words = [
        "อร่อย", "ดี", "หวาน", "สด", "คุณภาพดี", "ชอบ", "หอม", "อร่อยมาก", 
        "นุ่ม", "ละมุน", "หอมหวาน", "สุก", "พอดี", "นิ่ม", "เนื้อแน่น", "เยี่ยม", 
        "ประทับใจ", "อร่อยมากๆ", "มีคุณภาพ", "คุ้มค่า", "ถูกใจ", "น่าทาน",
        "อร่อยที่สุด", "ชอบมาก", "เลิศ", "เลิศรส", "โอเค", "โอเคมาก",
        "คุณภาพเยี่ยม", "รสชาติดี", "รสดี", "ดีมาก", "เนื้อดี", "น่าซื้อ",
        "กลมกล่อม", "ถูก", "ราคาไม่แพง", "กำลังดี", "น่ากิน", "หอมหวล",
        "คุ้ม", "รสชาติเยี่ยม", "ถูกปาก", "ถูกใจ", "สะอาด", "ประณีต",
        "สุดยอด", "ยอดเยี่ยม", "เจ๋ง", "เจ๋งมาก", "เด็ด", "เด็ดมาก", "แจ่ม", "แจ่มมาก",
        "สวย", "สวยงาม", "น่ารัก", "เยี่ยมยอด", "เลิศหรู", "ทำได้ดี", "ทำได้ดีมาก",
        "ชนะ", "ชนะเลิศ", "ทำได้", "เก่ง", "เก่งมาก", "ฉลาด", "รวดเร็ว", "เร็ว", "ว่องไว",
        "ปลอดภัย", "มั่นคง", "แข็งแรง", "ทนทาน", "คงทน", "มีประโยชน์", "มีคุณค่า",
        "สำเร็จ", "สำเร็จแล้ว", "พึงพอใจ", "พอใจ", "น่าสนใจ", "น่าตื่นเต้น", "น่าติดตาม"
    ]
    
    # คลังคำเชิงลบขยายเพิ่ม
    negative_words = [
        "แพง", "แย่", "เน่า", "เสีย", "ไม่อร่อย", "ไม่ชอบ", "แข็ง", "ไม่สด", "กลิ่นแรง",
        "แพงเกินไป", "ไม่คุ้ม", "ไม่คุ้มราคา", "เละ", "เน่าเสีย", "เสียเร็ว", "ช้า", 
        "ล่าช้า", "ส่งช้า", "เสียหาย", "ผิดหวัง", "แย่มาก", "น่าผิดหวัง", "ไม่สด", 
        "หมดอายุ", "ใกล้หมดอายุ", "คุณภาพต่ำ", "ไม่น่าทาน", "ไม่น่ากิน", "ไม่ดี", 
        "กลิ่นเหม็น", "จืด", "เฉอะแฉะ", "แพงมาก", "ร้อน", "เดือดร้อน", "ขาดส่ง",
        "เสียดาย", "ไหม้", "ดิบ", "สุกเกินไป", "เปรี้ยว", "ขม", "เค็ม", "ฉ่ำน้ำเกินไป",
        "ไม่คุ้มเงิน", "ไม่สะอาด", "สกปรก", "เสียดายเงิน", "น่าเบื่อ", "ธรรมดา",
        "ไม่เพียงพอ", "น้อยไป", "ราคาเกินจริง", "โกงราคา",
        "ห่วย", "ห่วยแตก", "แย่มากๆ", "เลวร้าย", "เลว", "ล้มเหลว", "ใช้ไม่ได้", "ใช้งานไม่ได้",
        "พัง", "พังมาก", "เสียหาย", "เสียหายมาก", "แตกหัก", "ชำรุด", "บกพร่อง", "ผิดพลาด",
        "ช้ามาก", "เชื่องช้า", "เสียเวลา", "เสียเงิน", "ยาก", "ยากมาก", "ลำบาก", "ยากเย็น",
        "อันตราย", "อันตรายมาก", "ไม่ปลอดภัย", "เสี่ยง", "เสี่ยงอันตราย", "น่ากลัว", "น่ากลัวมาก",
        "ทำไม่ได้", "ไม่สามารถ", "ไม่มีความสามารถ", "ผิด", "ผิดพลาด", "ผิดมหันต์", "ผิดมาก"
    ]
    
    # คลังคำเป็นกลางขยายเพิ่ม
    neutral_words = [
        "ราคา", "ขนส่ง", "ขนาด", "กิโล", "น้ำหนัก", "ทุเรียน", "กวน", 
        "ส่ง", "ส่งมา", "ได้รับ", "สั่ง", "จัดส่ง", "อายุ", "วันหมดอายุ", "เลือก", 
        "ผล", "ลูก", "จำนวน", "หลายลูก", "หมอนทอง", "ชะนี", "พวง", "ก้านยาว", 
        "บรรจุภัณฑ์", "กล่อง", "แพ็ค", "แพ็คเกจ", "เก็บ", "กระสอบ", "ตะกร้า", 
        "โปรโมชั่น", "ส่วนลด", "ผ่อน", "เครดิต", "คูปอง", "ผู้ขาย", "ผู้ส่ง",
        "โฆษณา", "ภาพ", "วีดีโอ", "รีวิว", "คำอธิบาย", "สีสัน", "เนื้อ", "ลักษณะ",
        "คน", "สิ่ง", "อัน", "ที่", "นี่", "นั่น", "โน่น", "บน", "ล่าง", "ข้าง", "ใน", "นอก",
        "ซ้าย", "ขวา", "หน้า", "หลัง", "ระหว่าง", "กลาง", "รอบ", "ผ่าน", "ทาง", "จาก", "ถึง",
        "เมื่อ", "ตอน", "ระหว่าง", "ก่อน", "หลัง", "เดี๋ยวนี้", "ตอนนี้", "วันนี้", "พรุ่งนี้", "เมื่อวาน",
        "เช้า", "สาย", "เที่ยง", "บ่าย", "เย็น", "ค่ำ", "ดึก", "กลางคืน", "กลางวัน",
        "ฉัน", "ผม", "ดิฉัน", "เธอ", "คุณ", "เขา", "มัน", "พวกเรา", "พวกเขา", "ท่าน",
        "ทำ", "ทำงาน", "ใช้", "ใช้งาน", "เปิด", "ปิด", "เริ่ม", "จบ", "เสร็จ", "พูด", "บอก", "ถาม",
        "ตอบ", "เขียน", "อ่าน", "ดู", "เห็น", "ได้ยิน", "ฟัง", "คิด", "จำ", "รู้", "เข้าใจ",
        "นำ", "พา", "เอา", "ให้", "รับ", "วาง", "ยก", "ถือ", "จับ", "ปล่อย", "ถอด", "ใส่",
        "กิน", "ดื่ม", "นอน", "ยืน", "นั่ง", "เดิน", "วิ่ง", "กระโดด", "หยุด", "จอด", "ขึ้น", "ลง"
    ]
    
    # คำหลักเกี่ยวกับประเภทของทุเรียน
    durian_types = [
        "หมอนทอง", "ชะนี", "ก้านยาว", "พวงมณี", "กระดุม", "อีกรอบ", "หลงลับแล",
        "หลินลับแล", "ทองย้อย", "ทุเรียนกวน", "ทุเรียนทอด", "ทุเรียนฟรีซดราย",
        "ทุเรียนพันธุ์", "กระดุมทอง", "ทุเรียนสด", "ทุเรียนแห้ง", "ทุเรียนสุก"
    ]
    
    # คำที่ใช้เน้นความรู้สึก
    intensifiers = [
        "มาก", "มากๆ", "สุดๆ", "ที่สุด", "เหลือเกิน", "อย่างมาก", "จริงๆ", 
        "เกินไป", "มากเกินไป", "เกิน", "กว่า", "พอดี", "เต็มที่", "สุดยอด", "เลย",
        "สุดๆ", "มากมาย", "มหาศาล", "สุด", "จัด", "ที่สุดเลย", "อย่างยิ่ง",
        "มากที่สุด", "แสนจะ", "ขนาดนั้น", "ขั้นสุด", "สุดเหวี่ยง"
    ]
    
    # คำปฏิเสธและการลดทอน
    negation_words = ["ไม่", "ไม่ได้", "ไม่ใช่", "ไม่เคย", "อย่า", "ไม่ต้อง"]
    diminishers = ["น้อย", "เล็กน้อย", "นิดหน่อย", "เบาๆ", "จางๆ", "บางๆ", "พอประมาณ"]
    
    # คำเชื่อมที่อาจเปลี่ยนความหมาย
    conjunctions = ["แต่", "แม้ว่า", "ถึงแม้", "กระนั้น", "อย่างไรก็ตาม", "แต่ว่า", "แต่ทว่า"]
    
    # แยกคำภาษาไทยด้วย pythainlp
    words = word_tokenize(text, engine='newmm')
    
    # กรองคำที่มีความยาวน้อยกว่า 2 ตัวอักษรออก (ยกเว้นคำปฏิเสธ)
    filtered_words = [word for word in words if len(word.strip()) > 1 or word in negation_words]
    
    # ค้นหาคำเชิงบวก เชิงลบ และเป็นกลาง
    found_positive_words = []
    found_negative_words = []
    found_neutral_words = []
    found_durian_types = []
    found_intensifiers = []
    found_conjunctions = []
    
    # รวมคำปฏิเสธกับคำความรู้สึกที่ตามมา
    negated_positive = []  # เก็บคู่คำ "ไม่" + คำเชิงบวก -> เป็นคำเชิงลบ
    negated_negative = []  # เก็บคู่คำ "ไม่" + คำเชิงลบ -> เป็นคำเชิงบวก
    complex_negations = [] # เก็บวลีปฏิเสธที่ซับซ้อน เช่น "ไม่ได้ + [คำ] + เหมือนที่"
    
    # ให้น้ำหนักคำตามการปรากฏร่วมกับคำเน้นความรู้สึก
    sentiment_scores = {"positive": 0, "negative": 0, "neutral": 0}
    
    # ตรวจหาคำเน้นความรู้สึกและคำเชื่อมก่อน
    for i, word in enumerate(filtered_words):
        if any(intensifier in word for intensifier in intensifiers):
            found_intensifiers.append(word)
        if any(conj in word for conj in conjunctions):
            found_conjunctions.append(word)
    
    # ตรวจสอบคำปฏิเสธแบบซับซ้อน (เช่น "ไม่ได้...เหมือนที่")
    for i, word in enumerate(filtered_words):
        if i < len(filtered_words) - 3 and word in negation_words:
            # คำถัดไปต่อจากคำปฏิเสธ
            next_words_window = filtered_words[i+1:i+5] # ดูหน้าต่างของคำถัดไป 4 คำ
            
            # ตรวจสอบแพทเทิร์น "ไม่ได้...เหมือนที่"
            if "เหมือน" in next_words_window or "อย่าง" in next_words_window or "ตามที่" in next_words_window:
                for j, next_word in enumerate(next_words_window):
                    # ตรวจหาความรู้สึกในคำเชื่อมโยง
                    if any(pos_word in next_word for pos_word in positive_words):
                        # เจอคำเชิงบวกหลังจากไม่ได้...เหมือนที่ -> เชิงลบ
                        negated_phrase = word + "..." + next_word
                        complex_negations.append(negated_phrase)
                        found_negative_words.append(negated_phrase)
                        sentiment_scores["negative"] += 1.5 # ให้น้ำหนักมากกว่าปกติ
                    elif any(neg_word in next_word for neg_word in negative_words):
                        # เจอคำเชิงลบหลังจากไม่ได้...เหมือนที่ -> เชิงบวก
                        negated_phrase = word + "..." + next_word
                        complex_negations.append(negated_phrase)
                        found_positive_words.append(negated_phrase)
                        sentiment_scores["positive"] += 1.5 # ให้น้ำหนักมากกว่าปกติ
    
    # ตรวจหาคำปฏิเสธและคำที่ตามมาติดกัน
    for i, word in enumerate(filtered_words):
        if word in negation_words and i < len(filtered_words) - 1:
            next_word = filtered_words[i+1]
            # หากคำถัดไปเป็นคำเชิงบวก ให้รวมเป็นคำเชิงลบ
            if any(pos_word in next_word for pos_word in positive_words):
                negated_phrase = word + next_word
                negated_positive.append(negated_phrase)
                found_negative_words.append(negated_phrase)  # เพิ่มวลีเชิงลบที่รวมแล้ว
                sentiment_scores["negative"] += 1.0
                # ข้ามการตรวจสอบคำถัดไป
                continue
            # หากคำถัดไปเป็นคำเชิงลบ ให้รวมเป็นคำเชิงบวก
            elif any(neg_word in next_word for neg_word in negative_words):
                negated_phrase = word + next_word
                negated_negative.append(negated_phrase)
                found_positive_words.append(negated_phrase)  # เพิ่มวลีเชิงบวกที่รวมแล้ว
                sentiment_scores["positive"] += 1.0
                # ข้ามการตรวจสอบคำถัดไป
                continue
            # หากคำถัดไปเป็นคำเน้นหรือคำลดทอน ให้ตรวจสอบคำต่อไปอีก
            elif any(intens in next_word for intens in intensifiers + diminishers) and i < len(filtered_words) - 2:
                next_next_word = filtered_words[i+2]
                # ตรวจสอบคำที่อยู่หลังคำเน้น
                if any(pos_word in next_next_word for pos_word in positive_words):
                    negated_phrase = word + next_word + next_next_word
                    negated_positive.append(negated_phrase)
                    found_negative_words.append(negated_phrase)
                    sentiment_scores["negative"] += 1.2  # น้ำหนักมากขึ้นเนื่องจากมีคำเน้น
                    continue
                elif any(neg_word in next_next_word for neg_word in negative_words):
                    negated_phrase = word + next_word + next_next_word
                    negated_negative.append(negated_phrase)
                    found_positive_words.append(negated_phrase)
                    sentiment_scores["positive"] += 1.2  # น้ำหนักมากขึ้นเนื่องจากมีคำเน้น
                    continue
    
    # ตรวจหาคำตามประเภท และคำนวณน้ำหนัก (ข้ามคำที่ถูกรวมเป็นวลีแล้ว)
    i = 0
    while i < len(filtered_words):
        word = filtered_words[i]
        skip = False
        
        # ข้ามคำที่เป็นส่วนหนึ่งของวลีที่ถูกรวมแล้ว
        if i < len(filtered_words) - 1:
            if word in negation_words and filtered_words[i+1] in [w for w in filtered_words if any(pos_word in w for pos_word in positive_words) or any(neg_word in w for neg_word in negative_words)]:
                i += 2  # ข้ามไปอีก 2 คำ (คำปฏิเสธและคำความรู้สึก)
                continue
        
        # ตรวจหาคำเชิงบวก (ที่ไม่อยู่ในวลีที่รวมแล้ว)
        if not skip and any(pos_word in word for pos_word in positive_words):
            # ตรวจสอบว่าไม่ใช่คำที่ถูกรวมในวลีปฏิเสธแล้ว
            if not any(word in phrase for phrase in negated_positive + negated_negative + complex_negations):
                found_positive_words.append(word)
                # เพิ่มน้ำหนักถ้าอยู่ใกล้คำเน้นความรู้สึก
                score = 1.0
                for intensifier in found_intensifiers:
                    if intensifier in filtered_words[max(0, i-2):min(len(filtered_words), i+3)]:
                        score *= 1.5
                sentiment_scores["positive"] += score
        
        # ตรวจหาคำเชิงลบ (ที่ไม่อยู่ในวลีที่รวมแล้ว)
        elif not skip and any(neg_word in word for neg_word in negative_words):
            # ตรวจสอบว่าไม่ใช่คำที่ถูกรวมในวลีปฏิเสธแล้ว
            if not any(word in phrase for phrase in negated_positive + negated_negative + complex_negations):
                found_negative_words.append(word)
                # เพิ่มน้ำหนักถ้าอยู่ใกล้คำเน้นความรู้สึก
                score = 1.0
                for intensifier in found_intensifiers:
                    if intensifier in filtered_words[max(0, i-2):min(len(filtered_words), i+3)]:
                        score *= 1.5
                sentiment_scores["negative"] += score
        
        # ตรวจหาคำเป็นกลาง
        elif not skip and any(neu_word in word for neu_word in neutral_words):
            found_neutral_words.append(word)
            sentiment_scores["neutral"] += 0.5
        
        # ตรวจหาประเภททุเรียน
        elif not skip and any(dtype in word for dtype in durian_types):
            found_durian_types.append(word)
            sentiment_scores["neutral"] += 0.2
        
        i += 1  # ไปยังคำถัดไป
    
    # ตรวจสอบการเปลี่ยนแปลงความรู้สึกจากคำเชื่อม
    if found_conjunctions and len(found_positive_words) > 0 and len(found_negative_words) > 0:
        # หาตำแหน่งของคำเชื่อม
        conj_indices = [i for i, word in enumerate(filtered_words) if any(conj in word for conj in conjunctions)]
        
        if conj_indices:
            # แบ่งความรู้สึกเป็นก่อนและหลังคำเชื่อม
            last_conj_idx = conj_indices[-1]  # ใช้คำเชื่อมล่าสุด
            
            # คำนวณน้ำหนักความรู้สึกหลังคำเชื่อม (ให้น้ำหนักมากกว่า)
            pos_after_conj = sum(1 for i, word in enumerate(filtered_words) if 
                               i > last_conj_idx and word in found_positive_words)
            neg_after_conj = sum(1 for i, word in enumerate(filtered_words) if 
                               i > last_conj_idx and word in found_negative_words)
            
            # ปรับน้ำหนักความรู้สึกหลังคำเชื่อม
            if pos_after_conj > neg_after_conj:
                sentiment_scores["positive"] += 0.5  # เพิ่มน้ำหนักเชิงบวก
            elif neg_after_conj > pos_after_conj:
                sentiment_scores["negative"] += 0.5  # เพิ่มน้ำหนักเชิงลบ
    
    # น้ำหนักคะแนนรวม
    total_score = sum(sentiment_scores.values())
    if total_score == 0:
        total_score = 1  # ป้องกันการหารด้วย 0
        
    # ปรับคะแนนให้เป็นสัดส่วน
    sentiment_ratios = {
        "positive": sentiment_scores["positive"] / total_score,
        "negative": sentiment_scores["negative"] / total_score,
        "neutral": sentiment_scores["neutral"] / total_score
    }
    
    # กำหนดค่าความเชื่อมั่น
    total_matches = len(found_positive_words) + len(found_negative_words) + len(found_neutral_words)
    base_confidence = min(0.95, 0.5 + (total_matches * 0.1)) if total_matches > 0 else 0.7
    
    # ตัดสินใจว่าข้อความมีความรู้สึกอย่างไร โดยใช้น้ำหนักที่คำนวณแล้ว
    if sentiment_ratios["positive"] > sentiment_ratios["negative"]:
        sentiment = "positive"
        confidence = base_confidence * (1 + sentiment_ratios["positive"] * 0.5)
    elif sentiment_ratios["negative"] > sentiment_ratios["positive"]:
        sentiment = "negative"
        confidence = base_confidence * (1 + sentiment_ratios["negative"] * 0.5)
    else:
        sentiment = "neutral"
        confidence = base_confidence * (1 + sentiment_ratios["neutral"] * 0.5)
    
    # ปรับค่าความเชื่อมั่นให้อยู่ในช่วง 0-1
    confidence = min(0.98, confidence)
    
    # แปลงความรู้สึกเป็นภาษาไทย
    sentiment_map = {
        'positive': 'เชิงบวก (Positive)',
        'negative': 'เชิงลบ (Negative)',
        'neutral': 'เป็นกลาง (Neutral)'
    }
    
    return {
        "text": text,
        "sentiment": sentiment,
        "sentiment_text": sentiment_map[sentiment],
        "confidence": confidence,
        "details": {
            "positive_matches": len(found_positive_words),
            "negative_matches": len(found_negative_words),
            "neutral_matches": len(found_neutral_words),
            "found_positive_words": found_positive_words,
            "found_negative_words": found_negative_words,
            "found_neutral_words": found_neutral_words,
            "found_durian_types": found_durian_types,
            "found_conjunctions": found_conjunctions,
            "tokenized_words": filtered_words,
            "sentiment_scores": sentiment_scores,
            "sentiment_ratios": sentiment_ratios,
            "negated_phrases": {
                "positive_to_negative": negated_positive, 
                "negative_to_positive": negated_negative,
                "complex_negations": complex_negations
            }
        }
    }

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    text = data.get('text', '')
    
    if not text:
        return jsonify({"error": "ไม่มีข้อความที่ต้องการวิเคราะห์"}), 400
    
    result = sentiment_analysis(text)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5000) 