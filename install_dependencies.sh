#!/bin/bash
echo "==============================================================="
echo "             ติดตั้งแพ็คเกจสำหรับ WangchanBERTa"
echo "==============================================================="
echo

echo "กำลังสร้างสภาพแวดล้อมเสมือน (Virtual Environment)..."
python -m venv .venv
source .venv/bin/activate

echo
echo "กำลังอัปเกรด pip..."
python -m pip install --upgrade pip

echo
echo "กำลังติดตั้ง tokenizers ก่อนเพื่อหลีกเลี่ยงปัญหากับ Rust compiler..."
pip install tokenizers --no-build-isolation

echo
echo "กำลังติดตั้ง sentencepiece..."
pip install sentencepiece>=0.1.99

echo
echo "กำลังติดตั้ง transformers เวอร์ชัน 4.30.2..."
pip install transformers==4.30.2 --no-deps

echo
echo "กำลังติดตั้งแพ็คเกจที่เกี่ยวข้องกับ transformers..."
pip install accelerate
pip install safetensors

echo
echo "กำลังติดตั้งแพ็คเกจหลักอื่นๆ..."
pip install torch>=2.0.0
pip install pythainlp>=4.0.2 flask>=2.3.3 flask-cors>=4.0.0 numpy>=1.24.3 pandas>=2.0.3

echo
echo "กำลังตรวจสอบการติดตั้ง..."
python -c "import torch; import transformers; import sentencepiece; import pythainlp; import flask; import flask_cors; import numpy; import pandas; print('การติดตั้งสำเร็จ! แพ็คเกจทั้งหมดพร้อมใช้งาน')"

echo
echo "เสร็จสิ้นการติดตั้ง! คุณสามารถทดสอบโมเดลได้โดยใช้คำสั่ง:"
echo "python workaround_test.py"
echo
echo "หรือเริ่มต้นใช้งาน API ด้วยคำสั่ง:"
echo "python ai_service_with_wangchanberta.py"
echo
echo "สำหรับการ fine-tune โมเดลด้วยข้อมูลของคุณ ใช้คำสั่ง:"
echo "python finetune_script.py --data_path your_data.csv"
echo 