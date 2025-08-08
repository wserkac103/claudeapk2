
@echo off
echo Installing Python dependencies...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
echo.
echo Dependencies installed successfully!
echo You can now run start.bat to start the application.
pause
