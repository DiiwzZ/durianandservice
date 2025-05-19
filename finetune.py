import torch
import os
import argparse
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    Trainer,
    TrainingArguments,
    EarlyStoppingCallback
)
from dataset import prepare_durian_dataset, create_sample_dataset
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

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

def train(args):
    """
    ฝึกสอนโมเดล WangchanBERTa
    """
    # ตรวจสอบ GPU
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"กำลังใช้งานอุปกรณ์: {device}")
    
    # เตรียมข้อมูล
    if not os.path.exists(args.data_path):
        print(f"ไม่พบไฟล์ข้อมูล {args.data_path} จะสร้างข้อมูลตัวอย่าง")
        data_path = create_sample_dataset()
    else:
        data_path = args.data_path
    
    train_dataset, eval_dataset = prepare_durian_dataset(data_path)
    print(f"ขนาดชุดข้อมูลฝึกสอน: {len(train_dataset)} ตัวอย่าง")
    print(f"ขนาดชุดข้อมูลประเมินผล: {len(eval_dataset)} ตัวอย่าง")
    
    # โหลดโมเดลและ tokenizer
    tokenizer = AutoTokenizer.from_pretrained(args.model_name)
    model = AutoModelForSequenceClassification.from_pretrained(
        args.model_name, 
        num_labels=3  # positive, neutral, negative
    )
    
    # กำหนดค่าการฝึกสอน
    training_args = TrainingArguments(
        output_dir=args.output_dir,
        num_train_epochs=args.epochs,
        per_device_train_batch_size=args.batch_size,
        per_device_eval_batch_size=args.batch_size,
        warmup_steps=args.warmup_steps,
        weight_decay=args.weight_decay,
        logging_dir=os.path.join(args.output_dir, "logs"),
        logging_steps=100,
        evaluation_strategy="steps",
        eval_steps=500,
        save_strategy="steps",
        save_steps=500,
        load_best_model_at_end=True,
        metric_for_best_model="f1",
        greater_is_better=True,
    )
    
    # สร้าง Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
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
    
    return model, tokenizer

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ฝึกสอนโมเดล WangchanBERTa สำหรับวิเคราะห์ความรู้สึกเกี่ยวกับทุเรียน")
    
    parser.add_argument("--data_path", type=str, default="durian_sentiment_sample.csv",
                        help="พาธไปยังไฟล์ข้อมูล CSV")
    parser.add_argument("--model_name", type=str, default="airesearch/wangchanberta-base-att-spm-uncased",
                        help="ชื่อโมเดล pre-trained")
    parser.add_argument("--output_dir", type=str, default="./durian-sentiment-model",
                        help="โฟลเดอร์สำหรับบันทึกโมเดล")
    parser.add_argument("--epochs", type=int, default=3,
                        help="จำนวนรอบการฝึกสอน")
    parser.add_argument("--batch_size", type=int, default=16,
                        help="ขนาด batch")
    parser.add_argument("--warmup_steps", type=int, default=500,
                        help="จำนวน warmup steps")
    parser.add_argument("--weight_decay", type=float, default=0.01,
                        help="ค่า weight decay")
    
    args = parser.parse_args()
    
    # ฝึกสอนโมเดล
    model, tokenizer = train(args) 