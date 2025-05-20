"""
สคริปต์ทดสอบการใช้งาน WangchanBERTa อย่างง่าย
"""
import torch
from transformers import AutoTokenizer, AutoModel, AutoModelForSequenceClassification

def test_wangchanberta_base():
    """ทดสอบโหลดโมเดล WangchanBERTa พื้นฐาน"""
    print("กำลังทดสอบการโหลด WangchanBERTa...")
    
    try:
        # โหลด tokenizer (ใช้ slow tokenizer เนื่องจากปัญหากับ SentencePiece)
        print("กำลังโหลด tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(
            "airesearch/wangchanberta-base-att-spm-uncased",
            use_fast=False
        )
        
        # โหลดโมเดลพื้นฐาน
        print("กำลังโหลดโมเดล...")
        model = AutoModel.from_pretrained("airesearch/wangchanberta-base-att-spm-uncased")
        
        # ทดสอบ tokenize ข้อความภาษาไทย
        text = "ทุเรียนนี้หวานมาก อร่อยสุดๆ"
        print(f"\nทดสอบ tokenize ข้อความ: '{text}'")
        
        tokens = tokenizer(
            text,
            return_tensors="pt",
            padding=True,
            truncation=True
        )
        
        print("ผลลัพธ์ tokenization:")
        print(f"- Input IDs: {tokens['input_ids'].shape}")
        print(f"- Attention Mask: {tokens['attention_mask'].shape}")
        
        # ทดสอบใช้งานโมเดล
        print("\nทดสอบการใช้งานโมเดล...")
        with torch.no_grad():
            outputs = model(**tokens)
        
        print(f"- ขนาด output: {outputs.last_hidden_state.shape}")
        print("\nการทดสอบสำเร็จ! WangchanBERTa ทำงานได้ปกติ")
        return True
        
    except Exception as e:
        print(f"\nเกิดข้อผิดพลาด: {str(e)}")
        print("\nข้อแนะนำในการแก้ไข:")
        print("1. ตรวจสอบว่าติดตั้งแพ็คเกจครบถ้วนแล้ว (torch, transformers, sentencepiece)")
        print("2. ตรวจสอบการเชื่อมต่ออินเทอร์เน็ต เนื่องจากต้องดาวน์โหลดโมเดลจาก Hugging Face")
        print("3. หากใช้ proxy ให้ตั้งค่า proxy environment variables")
        print("4. ทดลองติดตั้ง sentencepiece แยก: pip install sentencepiece")
        return False

def test_sentiment_analysis():
    """ทดสอบโมเดลสำหรับการวิเคราะห์ความรู้สึก"""
    print("\n=== ทดสอบการวิเคราะห์ความรู้สึกด้วย WangchanBERTa ===")
    
    try:
        # โหลด tokenizer
        print("กำลังโหลด tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(
            "airesearch/wangchanberta-base-att-spm-uncased",
            use_fast=False
        )
        
        # โหลดโมเดลสำหรับการจำแนกประโยค
        print("กำลังโหลดโมเดลสำหรับการวิเคราะห์ความรู้สึก...")
        model = AutoModelForSequenceClassification.from_pretrained(
            "airesearch/wangchanberta-base-att-spm-uncased",
            num_labels=3
        )
        model.eval()
        
        # ตัวแปรสำหรับการแปลงความรู้สึกจากตัวเลขเป็นข้อความ
        id_to_sentiment = {
            0: "เชิงบวก (positive)",
            1: "เป็นกลาง (neutral)",
            2: "เชิงลบ (negative)"
        }
        
        # ข้อความทดสอบ
        test_texts = [
            "ทุเรียนหมอนทองนี้หวานมาก เนื้อละเอียดอร่อยมากๆ",
            "ทุเรียนลูกนี้ราคาแพงเกินไป ไม่คุ้มค่าเลย",
            "ทุเรียนมาส่งช้ามาก กว่าจะได้รับก็เริ่มเน่าแล้ว",
            "ซื้อทุเรียนที่นี่ราคาสมเหตุสมผล ขนส่งรวดเร็ว"
        ]
        
        print("\nเริ่มทดสอบข้อความ...")
        for i, text in enumerate(test_texts):
            print(f"\nข้อความที่ {i+1}: \"{text}\"")
            
            # tokenize ข้อความ
            inputs = tokenizer(
                text,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=128
            )
            
            # วิเคราะห์ความรู้สึก
            with torch.no_grad():
                outputs = model(**inputs)
                scores = torch.nn.functional.softmax(outputs.logits, dim=1)
                predicted_class = torch.argmax(scores, dim=1).item()
            
            # แสดงผลลัพธ์
            print(f"ผลการวิเคราะห์: {id_to_sentiment[predicted_class]}")
            print(f"คะแนนความเชื่อมั่น: {scores[0][predicted_class].item():.4f}")
            print(f"คะแนนแต่ละประเภท: เชิงบวก: {scores[0][0].item():.4f}, เป็นกลาง: {scores[0][1].item():.4f}, เชิงลบ: {scores[0][2].item():.4f}")
        
        print("\nการทดสอบการวิเคราะห์ความรู้สึกสำเร็จ!")
        return True
        
    except Exception as e:
        print(f"\nเกิดข้อผิดพลาดในการทดสอบการวิเคราะห์ความรู้สึก: {str(e)}")
        return False

if __name__ == "__main__":
    # ทดสอบทั้งสองฟังก์ชัน
    base_result = test_wangchanberta_base()
    
    # หากโหลดโมเดลพื้นฐานสำเร็จ ให้ทดสอบการวิเคราะห์ความรู้สึก
    if base_result:
        test_sentiment_analysis() 