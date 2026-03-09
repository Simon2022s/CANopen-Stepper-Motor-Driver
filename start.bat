@echo off
chcp 65001 >nul
title RS485 Stepper Motor Driver Launcher
echo ============================================
echo   RS485 Stepper Motor Driver
echo ============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [Error] Python not detected!
    echo.
    echo Please install Python 3.8 or higher:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo [Info] Python detected
echo.

REM Check if dependencies need to be installed
echo [Info] Checking dependencies...
python -c "import PyQt5" >nul 2>&1
if errorlevel 1 (
    echo [Info] Installing PyQt5...
    pip install PyQt5>=5.15.0
    if errorlevel 1 (
        echo [Error] PyQt5 installation failed!
        pause
        exit /b 1
    )
)

python -c "import serial" >nul 2>&1
if errorlevel 1 (
    echo [Info] Installing pyserial...
    pip install pyserial>=3.5
    if errorlevel 1 (
        echo [Error] pyserial installation failed!
        pause
        exit /b 1
    )
)

echo [Info] Dependency check complete!
echo.

REM Launch program
echo [Info] Starting RS485 Stepper Motor Driver...
echo ============================================
echo.

python BruceLee.py

if errorlevel 1 (
    echo.
    echo [Error] Program encountered an error!
    pause
)
