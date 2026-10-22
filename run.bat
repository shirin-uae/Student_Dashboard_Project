@echo off
setlocal
cd /d "%~dp0"

where python >nul 2>nul
if errorlevel 1 (
    echo Python was not found. Install Python 3.10 or newer and enable "Add Python to PATH".
    pause
    exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
    echo Creating virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo Could not create the virtual environment.
        pause
        exit /b 1
    )
)

call ".venv\Scripts\activate.bat"

python -m pip install --upgrade pip >nul
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo Dependency installation failed.
    pause
    exit /b 1
)

if not defined MYSQL_HOST set "MYSQL_HOST=localhost"
if not defined MYSQL_USER set "MYSQL_USER=root"
if not defined MYSQL_PASSWORD set /p "MYSQL_PASSWORD=MySQL password for %MYSQL_USER%@%MYSQL_HOST% (press Enter if none): "

echo Starting Student Dashboard...
python -m streamlit run app.py

pause
