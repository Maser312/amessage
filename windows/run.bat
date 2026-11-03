@echo off
title AMessage for Windows
cd /d "%~dp0"
python -m amessage_windows.app
if %errorlevel% neq 0 (
    echo.
    echo Installing requirements...
    pip install -r requirements.txt
    python -m amessage_windows.app
)
pause
