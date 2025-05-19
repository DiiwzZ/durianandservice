@echo off
echo ===== ติดตั้ง Durian Analytics Service =====
echo.

REM ตรวจสอบว่ามี NSSM หรือไม่
where nssm >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo NSSM ไม่พบในระบบ
    echo กรุณาดาวน์โหลด NSSM จาก https://nssm.cc/download
    echo และติดตั้งหรือวางไฟล์ไว้ในไดเรกทอรีนี้
    echo.
    echo หรือคุณสามารถทำตามขั้นตอนการติดตั้งแบบออนไลน์ได้ที่:
    echo https://nssm.cc/usage
    pause
    exit /b 1
)

REM กำหนด path ของ script ในไดเรกทอรีปัจจุบัน
set SCRIPT_PATH=%~dp0run_service.bat

REM ติดตั้ง service
echo ติดตั้ง Durian Analytics Service...
nssm install DurianAnalyticsService "%SCRIPT_PATH%"
nssm set DurianAnalyticsService DisplayName "Durian Analytics Service"
nssm set DurianAnalyticsService Description "บริการวิเคราะห์ความรู้สึกทุเรียน"
nssm set DurianAnalyticsService AppDirectory "%~dp0"
nssm set DurianAnalyticsService AppStdout "%~dp0logs\service.log"
nssm set DurianAnalyticsService AppStderr "%~dp0logs\error.log"
nssm set DurianAnalyticsService Start SERVICE_AUTO_START

REM สร้างโฟลเดอร์ logs ถ้ายังไม่มี
if not exist "%~dp0logs" mkdir "%~dp0logs"

echo.
echo ติดตั้ง Service เรียบร้อยแล้ว
echo คุณสามารถเริ่มต้น Service ได้โดยใช้คำสั่ง: 
echo nssm start DurianAnalyticsService
echo.
echo หรือจะเริ่มต้นตอนนี้เลยหรือไม่? (Y/N)
choice /c YN /m "เริ่มต้น Service ตอนนี้"
if %ERRORLEVEL% EQU 1 (
    nssm start DurianAnalyticsService
    echo Service เริ่มทำงานแล้ว
) else (
    echo คุณสามารถเริ่มต้น Service ได้ภายหลังผ่าน Services Manager หรือใช้คำสั่ง:
    echo nssm start DurianAnalyticsService
)

echo.
echo ===== เสร็จสิ้นการติดตั้ง =====
pause 