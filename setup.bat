@echo off
setlocal
title Mahi JARVIS Setup
cd /d "%~dp0"

where py >nul 2>nul
if %errorlevel%==0 (
    set "PY=py"
) else (
    set "PY=python"
)

echo [JARVIS] Checking Python...
%PY% --version
if errorlevel 1 (
    echo Python 3 is not installed or is not on PATH.
    echo Install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)

if not exist ".venv\Scripts\python.exe" %PY% -m venv .venv
".venv\Scripts\python.exe" -m pip install --upgrade pip
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 (
    echo Dependency installation failed.
    pause
    exit /b 1
)

echo.
echo Setup complete. Double-click run.bat to start JARVIS.
pause
