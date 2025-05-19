@echo off
echo ===== ถอนการติดตั้ง Durian Analytics Service =====
echo.

REM ตรวจสอบว่ามี NSSM หรือไม่
where nssm >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo NSSM ไม่พบในระบบ
    echo กรุณาดาวน์โหลด NSSM จาก https://nssm.cc/download
    pause
    exit /b 1
)

echo คุณต้องการถอนการติดตั้ง Durian Analytics Service หรือไม่? (Y/N)
choice /c YN /m "ยืนยันการถอนการติดตั้ง"
if %ERRORLEVEL% NEQ 1 (
    echo ยกเลิกการถอนการติดตั้ง
    pause
    exit /b 0
)

REM หยุด service ก่อน (ถ้ากำลังทำงานอยู่)
echo หยุดการทำงานของ service...
nssm stop DurianAnalyticsService

REM ถอนการติดตั้ง service
echo ถอนการติดตั้ง service...
nssm remove DurianAnalyticsService confirm

echo.
echo ===== ถอนการติดตั้งเสร็จสิ้น =====
pause 