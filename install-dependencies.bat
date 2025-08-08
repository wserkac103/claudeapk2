
@echo off
echo Installing Python dependencies for Android App Generator...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

REM Upgrade pip first
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo Installing required packages...
python -m pip install -r requirements.txt

if %errorlevel% equ 0 (
    echo.
    echo SUCCESS: All dependencies installed successfully!
    echo You can now run start.bat to start the application
) else (
    echo.
    echo ERROR: Failed to install some dependencies
    echo Please check the error messages above
)

echo.
pause
