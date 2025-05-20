"""
สคริปต์สำหรับการตรวจสอบและแก้ไขปัญหาในการใช้งาน WangchanBERTa
"""
import os
import sys
import subprocess
import importlib
import pkg_resources

def check_package_version(package_name):
    """ตรวจสอบเวอร์ชันของแพ็คเกจ"""
    try:
        version = pkg_resources.get_distribution(package_name).version
        return version
    except pkg_resources.DistributionNotFound:
        return "ไม่ได้ติดตั้ง"

def check_dependencies():
    """ตรวจสอบการติดตั้งแพ็คเกจที่จำเป็น"""
    print("\n=== ตรวจสอบแพ็คเกจที่จำเป็น ===")
    packages = [
        "torch",
        "transformers",
        "sentencepiece",
        "pythainlp",
        "flask",
        "flask-cors",
        "numpy",
        "pandas"
    ]
    
    for package in packages:
        version = check_package_version(package)
        print(f"- {package}: {version}")
    
    # ตรวจสอบเวอร์ชันที่สำคัญ
    transformers_version = check_package_version("transformers")
    if transformers_version != "4.30.2":
        print(f"\nคำเตือน: เวอร์ชันของ transformers ({transformers_version}) ไม่ตรงกับที่แนะนำ (4.30.2)")
        print("ลองติดตั้งเวอร์ชันที่แนะนำด้วยคำสั่ง: pip install transformers==4.30.2")

def test_tokenizer_loading():
    """ทดสอบการโหลด tokenizer ของ WangchanBERTa"""
    print("\n=== ทดสอบการโหลด tokenizer ===")
    try:
        from transformers import AutoTokenizer
        
        print("กำลังโหลด tokenizer แบบปกติ...")
        try:
            tokenizer = AutoTokenizer.from_pretrained("airesearch/wangchanberta-base-att-spm-uncased")
            print("✓ โหลด tokenizer แบบปกติสำเร็จ!")
        except Exception as e:
            print(f"✗ ไม่สามารถโหลด tokenizer แบบปกติได้: {str(e)}")
        
        print("\nกำลังโหลด tokenizer ด้วย use_fast=False...")
        try:
            tokenizer = AutoTokenizer.from_pretrained("airesearch/wangchanberta-base-att-spm-uncased", use_fast=False)
            print("✓ โหลด tokenizer ด้วย use_fast=False สำเร็จ!")
            
            # ทดสอบการ tokenize
            text = "ทุเรียนนี้หวานมาก อร่อยสุดๆ"
            tokens = tokenizer(text, return_tensors="pt")
            print(f"ทดสอบ tokenize: {text}")
            print(f"ได้ input_ids: {tokens['input_ids'].shape}")
            return tokenizer
        except Exception as e:
            print(f"✗ ไม่สามารถโหลด tokenizer ด้วย use_fast=False ได้: {str(e)}")
            return None
    except Exception as e:
        print(f"เกิดข้อผิดพลาดในการโหลด transformers: {str(e)}")
        return None

def test_model_loading(tokenizer):
    """ทดสอบการโหลดโมเดล WangchanBERTa"""
    if tokenizer is None:
        print("\n=== ไม่สามารถทดสอบโมเดลได้เนื่องจากไม่สามารถโหลด tokenizer ได้ ===")
        return
    
    print("\n=== ทดสอบการโหลดโมเดล ===")
    try:
        from transformers import AutoModel, AutoModelForSequenceClassification
        import torch
        
        print("กำลังโหลดโมเดลพื้นฐาน...")
        try:
            model = AutoModel.from_pretrained("airesearch/wangchanberta-base-att-spm-uncased")
            print("✓ โหลดโมเดลพื้นฐานสำเร็จ!")
        except Exception as e:
            print(f"✗ ไม่สามารถโหลดโมเดลพื้นฐานได้: {str(e)}")
        
        print("\nกำลังโหลดโมเดลสำหรับการจำแนกประโยค...")
        try:
            model = AutoModelForSequenceClassification.from_pretrained(
                "airesearch/wangchanberta-base-att-spm-uncased",
                num_labels=3
            )
            print("✓ โหลดโมเดลสำหรับการจำแนกประโยคสำเร็จ!")
            
            # ทดสอบการใช้งานโมเดล
            text = "ทุเรียนนี้หวานมาก อร่อยสุดๆ"
            inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
            
            print("\nกำลังทดสอบการใช้งานโมเดล...")
            with torch.no_grad():
                outputs = model(**inputs)
            
            print("✓ ใช้งานโมเดลสำเร็จ!")
            print(f"รูปร่างของ logits: {outputs.logits.shape}")
            
            # แสดงผลลัพธ์การทำนาย
            scores = torch.nn.functional.softmax(outputs.logits, dim=1)
            prediction = torch.argmax(scores, dim=1).item()
            
            id_to_sentiment = {
                0: "เชิงบวก (positive)",
                1: "เป็นกลาง (neutral)",
                2: "เชิงลบ (negative)"
            }
            
            print(f"\nผลการวิเคราะห์ข้อความ '{text}':")
            print(f"- ความรู้สึก: {id_to_sentiment[prediction]}")
            print(f"- คะแนนความเชื่อมั่น: {scores[0][prediction].item():.4f}")
            print(f"- คะแนนแต่ละประเภท: เชิงบวก: {scores[0][0].item():.4f}, เป็นกลาง: {scores[0][1].item():.4f}, เชิงลบ: {scores[0][2].item():.4f}")
            
        except Exception as e:
            print(f"✗ ไม่สามารถโหลดโมเดลสำหรับการจำแนกประโยคได้: {str(e)}")
    except Exception as e:
        print(f"เกิดข้อผิดพลาดในการโหลดโมเดล: {str(e)}")

def show_recommendations():
    """แสดงคำแนะนำในการแก้ไขปัญหา"""
    print("\n=== คำแนะนำในการแก้ไขปัญหา ===")
    print("1. หากพบปัญหา 'Converting from SentencePiece and Tiktoken failed':")
    print("   - ใช้ use_fast=False เมื่อโหลด tokenizer")
    print("   - ติดตั้ง sentencepiece เวอร์ชันล่าสุด: pip install sentencepiece --upgrade")
    
    print("\n2. หากพบปัญหากับเวอร์ชันของ transformers:")
    print("   - ติดตั้ง transformers เวอร์ชัน 4.30.2: pip install transformers==4.30.2")
    
    print("\n3. หากยังพบปัญหา:")
    print("   - ลองใช้ไฟล์ ai_service_with_wangchanberta.py ที่มีระบบสำรองในกรณีที่โหลดโมเดลไม่สำเร็จ")
    print("   - ลองติดตั้งแพ็คเกจทั้งหมดใหม่ด้วยไฟล์ install_dependencies.bat")

if __name__ == "__main__":
    print("=== การทดสอบและแก้ไขปัญหา WangchanBERTa ===")
    
    # ตรวจสอบแพ็คเกจที่จำเป็น
    check_dependencies()
    
    # ทดสอบการโหลด tokenizer
    tokenizer = test_tokenizer_loading()
    
    # ทดสอบการโหลดโมเดล
    test_model_loading(tokenizer)
    
    # แสดงคำแนะนำ
    show_recommendations() 