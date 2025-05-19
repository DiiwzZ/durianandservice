from inference import predict_sentiment

# ทดสอบประโยคที่มีคำปฏิเสธ
test_texts = [
    # ประโยคพื้นฐาน
    "ทุเรียนนี้อร่อยมาก",
    "ทุเรียนนี้แพงเกินไป",
    
    # คำปฏิเสธแบบง่าย
    "ทุเรียนนี้ไม่อร่อยเลย แพงมากด้วย",
    "ทุเรียนนี้ไม่แพง แต่รสชาติดีมาก",
    "อร่อย",
    "ไม่อร่อย",
    "แพง แต่ไม่อร่อย",
    "ไม่แพง และอร่อยมาก",
    
    # คำปฏิเสธกับคำขยาย
    "ทุเรียนนี้ไม่แพงเลย อร่อยด้วย",
    "ทุเรียนนี้ไม่อร่อยมากนัก แต่ราคาเหมาะสม",
    "ทุเรียนนี้ไม่ค่อยหวาน แต่ก็กินได้",
    
    # คำปฏิเสธแบบซับซ้อน
    "ทุเรียนนี้ไม่ได้อร่อยเหมือนที่โฆษณา แต่ก็ไม่แพง",
    "ไม่ได้แพงเหมือนที่คิด อร่อยมาก",
    "ทุเรียนนี้ไม่ได้มีคุณภาพตามที่ขายไว้",
    "ไม่ได้หวานเหมือนที่คาดหวัง แต่ก็ไม่แย่",
    
    # ประโยคที่มีคำเชื่อม
    "ทุเรียนแพงแต่อร่อย",
    "ทุเรียนอร่อยแต่แพง",
    "ทุเรียนนี้มีกลิ่นแรง แต่รสชาติหวานมาก",
    "ทุเรียนนี้เน่าเล็กน้อย แต่ส่วนที่เหลือกินได้",
    
    # ประโยคผสม
    "ทุเรียนนี้ไม่แพงมาก แต่ก็ไม่ได้อร่อยเหมือนที่โฆษณาไว้",
    "ทุเรียนไม่ได้หวานมากอย่างที่คิด แต่ก็ไม่แพงและบรรจุภัณฑ์ดี"
]

print("=" * 70)
print("             ทดสอบระบบวิเคราะห์ความรู้สึกขั้นสูง               ")
print("=" * 70)

for index, text in enumerate(test_texts, 1):
    result = predict_sentiment(text)
    
    # แปลงความรู้สึกเป็นภาษาไทย
    sentiment_map = {
        'positive': 'เชิงบวก (Positive)',
        'negative': 'เชิงลบ (Negative)',
        'neutral': 'เป็นกลาง (Neutral)'
    }
    
    print(f"\nทดสอบที่ {index}: \"{text}\"")
    print(f"ผลการวิเคราะห์: {sentiment_map[result['sentiment']]}")
    print(f"ความเชื่อมั่น: {result['confidence'] * 100:.2f}%")
    
    # แสดงคำแยกตามประเภท
    print("\nคำที่พบ:")
    if result['details']['found_positive_words']:
        print(f"  คำเชิงบวก: {', '.join(result['details']['found_positive_words'])}")
    if result['details']['found_negative_words']:
        print(f"  คำเชิงลบ: {', '.join(result['details']['found_negative_words'])}")
    if result['details']['found_neutral_words']:
        print(f"  คำเป็นกลาง: {', '.join(result['details']['found_neutral_words'])}")
    if result['details']['found_conjunctions']:
        print(f"  คำเชื่อม: {', '.join(result['details']['found_conjunctions'])}")
    
    # แสดงรายละเอียดวลีที่ถูกรวม
    print("\nการตีความคำปฏิเสธ:")
    if result['details']['negated_phrases']['positive_to_negative']:
        print(f"  วลีเชิงบวกที่กลายเป็นเชิงลบ: {', '.join(result['details']['negated_phrases']['positive_to_negative'])}")
    if result['details']['negated_phrases']['negative_to_positive']:
        print(f"  วลีเชิงลบที่กลายเป็นเชิงบวก: {', '.join(result['details']['negated_phrases']['negative_to_positive'])}")
    if result['details']['negated_phrases']['complex_negations']:
        print(f"  วลีปฏิเสธซับซ้อน: {', '.join(result['details']['negated_phrases']['complex_negations'])}")
    if not result['details']['negated_phrases']['positive_to_negative'] and not result['details']['negated_phrases']['negative_to_positive'] and not result['details']['negated_phrases']['complex_negations']:
        print("  ไม่พบการปฏิเสธ")
    
    # แสดงสัดส่วนความรู้สึก
    print("\nสัดส่วนความรู้สึก:")
    ratios = result['details']['sentiment_ratios']
    print(f"  เชิงบวก: {ratios['positive']*100:.1f}%")
    print(f"  เชิงลบ: {ratios['negative']*100:.1f}%")
    print(f"  เป็นกลาง: {ratios['neutral']*100:.1f}%")
    
    print("-" * 70) 