@echo off
REM สคริปต์สำหรับรัน ai_service.py ในโหมด service
REM ใช้ current working directory เป็นไดเรกทอรีของสคริปต์
cd /d "%~dp0"
REM ใช้ venv ถ้ามี
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
) else (
    echo Virtual environment not found, using system Python
)
REM รัน Flask app
python ai_service.py
REM ถ้าเกิดข้อผิดพลาด รอให้ผู้ใช้กด key ก่อนจบการทำงาน
if %ERRORLEVEL% NEQ 0 (
    echo Error occurred. Press any key to exit.
    pause > nul
) 