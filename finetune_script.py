"""
สคริปต์สำหรับการ fine-tune โมเดล WangchanBERTa สำหรับการวิเคราะห์ความรู้สึกเกี่ยวกับทุเรียน
"""
import argparse
import os
import pandas as pd
import torch
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    Trainer, 
    TrainingArguments,
    EarlyStoppingCallback
)
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from sklearn.model_selection import train_test_split
from torch.utils.data import Dataset

class SentimentDataset(Dataset):
    """
    Dataset สำหรับการวิเคราะห์ความรู้สึก
    """
    def __init__(self, texts, labels, tokenizer, max_length=128):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
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

def compute_metrics(pred):
    """
    คำนวณเมตริกการประเมินผล
    """
    labels = pred.label_ids
    preds = pred.predictions.argmax(-1)
    
    precision, recall, f1, _ = precision_recall_fscore_support(
        labels, preds, average='weighted')
    acc = accuracy_score(labels, preds)
    
    return {
        'accuracy': acc,
        'f1': f1,
        'precision': precision,
        'recall': recall
    }

def main(args):
    # โหลด tokenizer
    print(f"กำลังโหลด tokenizer จาก {args.model_name}...")
    tokenizer = AutoTokenizer.from_pretrained(args.model_name, use_fast=False)
    
    # โหลดข้อมูล
    print(f"กำลังโหลดข้อมูลจาก {args.data_path}...")
    df = pd.read_csv(args.data_path)
    
    # ข้อมูลต้องมีคอลัมน์ text และ label เท่านั้น
    if 'text' not in df.columns or 'label' not in df.columns:
        raise ValueError("ไฟล์ CSV ต้องมีคอลัมน์ 'text' และ 'label'")
    
    # แบ่งข้อมูลเป็น train และ validation
    train_texts, val_texts, train_labels, val_labels = train_test_split(
        df['text'].tolist(), 
        df['label'].tolist(), 
        test_size=0.2, 
        random_state=42
    )
    
    # สร้าง dataset
    train_dataset = SentimentDataset(train_texts, train_labels, tokenizer)
    val_dataset = SentimentDataset(val_texts, val_labels, tokenizer)
    
    print(f"จำนวนข้อมูลฝึกสอน: {len(train_dataset)}")
    print(f"จำนวนข้อมูลตรวจสอบ: {len(val_dataset)}")
    
    # โหลดโมเดล
    print(f"กำลังโหลดโมเดล {args.model_name}...")
    model = AutoModelForSequenceClassification.from_pretrained(
        args.model_name, 
        num_labels=3  # positive, neutral, negative
    )
    
    # กำหนดค่าการฝึกสอน - แก้ไขพารามิเตอร์ให้สอดคล้องกับเวอร์ชันของ transformers
    training_args = TrainingArguments(
        output_dir=args.output_dir,
        num_train_epochs=args.epochs,
        per_device_train_batch_size=args.batch_size,
        per_device_eval_batch_size=args.batch_size,
        warmup_steps=100,
        weight_decay=0.01,
        logging_dir=os.path.join(args.output_dir, "logs"),
        logging_steps=10,
        eval_strategy="steps",
        eval_steps=100,
        save_strategy="steps",
        save_steps=100,
        load_best_model_at_end=True,
        metric_for_best_model="f1",
        greater_is_better=True,
    )
    
    # สร้าง Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        compute_metrics=compute_metrics,
        callbacks=[EarlyStoppingCallback(early_stopping_patience=3)]
    )
    
    # ฝึกสอนโมเดล
    print("เริ่มการฝึกสอนโมเดล...")
    trainer.train()
    
    # ประเมินผลโมเดล
    print("ประเมินผลโมเดล...")
    eval_results = trainer.evaluate()
    print(f"ผลการประเมิน: {eval_results}")
    
    # บันทึกโมเดล
    print(f"บันทึกโมเดลที่ {args.output_dir}")
    model.save_pretrained(args.output_dir)
    tokenizer.save_pretrained(args.output_dir)
    
    print("เสร็จสิ้นการ fine-tune โมเดล!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fine-tune WangchanBERTa สำหรับการวิเคราะห์ความรู้สึก")
    
    parser.add_argument("--data_path", type=str, default="durian_sentiment_additional.csv",
                        help="พาธไปยังไฟล์ข้อมูล CSV")
    parser.add_argument("--model_name", type=str, default="airesearch/wangchanberta-base-att-spm-uncased",
                        help="ชื่อโมเดล pre-trained")
    parser.add_argument("--output_dir", type=str, default="./durian-sentiment-model",
                        help="โฟลเดอร์สำหรับบันทึกโมเดล")
    parser.add_argument("--epochs", type=int, default=3,
                        help="จำนวนรอบการฝึกสอน")
    parser.add_argument("--batch_size", type=int, default=8,
                        help="ขนาด batch (ลดลงถ้า RAM/VRAM ไม่พอ)")
    
    args = parser.parse_args()
    
    # ตรวจสอบว่ามีไฟล์ข้อมูลหรือไม่
    if not os.path.exists(args.data_path):
        print(f"คำเตือน: ไม่พบไฟล์ข้อมูล {args.data_path} กรุณาระบุพาธที่ถูกต้องด้วยพารามิเตอร์ --data_path")
        exit(1)
    
    # สร้างโฟลเดอร์สำหรับเก็บโมเดล
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
    
    # เริ่มการ fine-tune
    main(args) 