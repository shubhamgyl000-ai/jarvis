@echo off
setlocal
cd /d "%~dp0"
echo === Jarvis / Mahi Windows Setup ===
where py >nul 2>&1 || (echo Python launcher not found. Install Python 3.11+ first.& exit /b 1)
if not exist ".venv\Scripts\python.exe" (
  py -3 -m venv .venv || exit /b 1
)
call ".venv\Scripts\activate.bat"
python -m pip install --upgrade pip
python -m pip install -r requirements.txt || exit /b 1
echo.
echo Setup complete.
echo Run Jarvis with: .venv\Scripts\python.exe jarvis.py
pause
