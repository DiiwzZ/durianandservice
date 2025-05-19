import pandas as pd
import torch
from torch.utils.data import Dataset
from transformers import AutoTokenizer

class DurianDataset(Dataset):
    def __init__(self, texts, labels, tokenizer_name="airesearch/wangchanberta-base-att-spm-uncased", max_length=128):
        self.texts = texts
        self.labels = labels
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)
        self.max_length = max_length
    
    def __len__(self):
        return len(self.texts)
    
    def __getitem__(self, idx):
        text = self.texts[idx]
        label = self.labels[idx]
        
        encoding = self.tokenizer(
            text,
            truncation=True,
            padding='max_length',
            max_length=self.max_length,
            return_tensors='pt'
        )
        
        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'labels': torch.tensor(label, dtype=torch.long)
        }

def prepare_durian_dataset(csv_path):
    """
    เตรียมชุดข้อมูลทุเรียนจากไฟล์ CSV
    
    Parameters:
    csv_path (str): พาธไปยังไฟล์ CSV ที่มีข้อมูล
    
    Returns:
    tuple: (train_dataset, test_dataset) สำหรับใช้ในการฝึกสอนและทดสอบโมเดล
    """
    # อ่านข้อมูลจาก CSV
    df = pd.read_csv(csv_path)
    
    # ตัวอย่างรูปแบบ CSV ที่คาดหวัง:
    # text,label
    # "ทุเรียนนี้หวานมาก", 0  # 0=positive, 1=neutral, 2=negative
    
    # แปลงเป็นรายการ
    texts = df['text'].tolist()
    labels = df['label'].tolist()
    
    # แบ่งชุดข้อมูลเป็นชุดฝึกสอนและชุดทดสอบ (80:20)
    train_size = int(0.8 * len(texts))
    
    train_texts = texts[:train_size]
    train_labels = labels[:train_size]
    
    test_texts = texts[train_size:]
    test_labels = labels[train_size:]
    
    # สร้าง Dataset
    tokenizer_name = "airesearch/wangchanberta-base-att-spm-uncased"
    
    train_dataset = DurianDataset(train_texts, train_labels, tokenizer_name)
    test_dataset = DurianDataset(test_texts, test_labels, tokenizer_name)
    
    return train_dataset, test_dataset

def create_sample_dataset():
    """
    สร้างชุดข้อมูลตัวอย่างสำหรับการทดสอบ
    
    Returns:
    str: พาธไปยังไฟล์ CSV ที่สร้างขึ้น
    """
    # สร้างข้อมูลตัวอย่าง
    data = {
        'text': [
            "ทุเรียนนี้หวานมาก อร่อยสุดๆ",
            "ทุเรียนพันธุ์นี้เนื้อเยอะดี",
            "ราคาทุเรียนปีนี้สูงกว่าปีที่แล้ว",
            "ทุเรียนนี้เนื้อแข็งไป ไม่อร่อยเลย",
            "กลิ่นทุเรียนแรงมาก ไม่ชอบเลย",
            "ทุเรียนนี้ไม่สุก แข็งมาก",
            "ทุเรียนหมอนทองอร่อยที่สุดในโลก",
            "ทุเรียนนี้ราคาแพงเกินไป ไม่คุ้มค่า",
            "ทุเรียนพันธุ์นี้มีกลิ่นหอม รสชาติดี",
            "ฉันซื้อทุเรียนมาแล้วเน่า เสียใจมาก"
        ],
        'label': [
            0,  # positive
            0,  # positive
            1,  # neutral
            2,  # negative
            2,  # negative
            2,  # negative
            0,  # positive
            2,  # negative
            0,  # positive
            2   # negative
        ]
    }
    
    # สร้าง DataFrame
    df = pd.DataFrame(data)
    
    # บันทึกเป็นไฟล์ CSV
    output_path = "durian_sentiment_sample.csv"
    df.to_csv(output_path, index=False)
    
    print(f"สร้างไฟล์ตัวอย่าง {output_path} เรียบร้อยแล้ว")
    return output_path

if __name__ == "__main__":
    # สร้างชุดข้อมูลตัวอย่าง
    csv_path = create_sample_dataset()
    
    # ทดสอบการโหลดข้อมูล
    train_dataset, test_dataset = prepare_durian_dataset(csv_path)
    
    print(f"ขนาดชุดข้อมูลฝึกสอน: {len(train_dataset)}")
    print(f"ขนาดชุดข้อมูลทดสอบ: {len(test_dataset)}")
    
    # ทดสอบการเข้าถึงข้อมูล
    sample = train_dataset[0]
    print(f"ตัวอย่างข้อมูล: {sample['input_ids'].shape}, {sample['attention_mask'].shape}, {sample['labels']}") 