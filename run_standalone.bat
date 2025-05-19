@echo off
echo ===== เริ่มต้น Durian Analytics Server =====
echo.

REM ไปที่ไดเรกทอรีของสคริปต์
cd /d "%~dp0"

REM ใช้ virtual environment ถ้ามี
if exist .venv\Scripts\activate.bat (
    echo ใช้งาน Virtual Environment...
    call .venv\Scripts\activate.bat
) else (
    echo ไม่พบ Virtual Environment จะใช้ Python ของระบบแทน
)

REM รันเซิร์ฟเวอร์
echo เริ่มต้น Flask Server ที่ http://localhost:5000
echo กด Ctrl+C เพื่อหยุดการทำงาน
echo.

python ai_service.py

REM ถ้าเกิดข้อผิดพลาด
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo เกิดข้อผิดพลาดในการรันเซิร์ฟเวอร์
    echo กรุณาตรวจสอบว่าได้ติดตั้งแพ็คเกจที่จำเป็นแล้ว:
    echo   pip install -r requirements.txt
    echo.
    pause
) 