@echo off
setlocal
title Mahi JARVIS

cd /d "%~dp0"

where py >nul 2>nul
if %errorlevel%==0 (
    set "PY=py"
) else (
    set "PY=python"
)

if not exist ".venv\Scripts\python.exe" (
    echo [JARVIS] Creating virtual environment...
    %PY% -m venv .venv
    if errorlevel 1 goto :error
)

echo [JARVIS] Installing/updating dependencies...
".venv\Scripts\python.exe" -m pip install --upgrade pip
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 goto :error

echo.
echo [JARVIS] Starting Mahi JARVIS...
echo Speak your command after Mahi says she is ready.
echo.
".venv\Scripts\python.exe" jarvis_pro.py
goto :end

:error
echo.
echo [JARVIS] Setup failed. Check that Python 3 is installed and try again.
pause

:end
endlocal
