@echo off
echo Starting Android App Generator...
echo.
echo Installing dependencies...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
echo.
echo Dependencies installed successfully!
echo.
echo Server will start on http://127.0.0.1:5001
echo Press Ctrl+C to stop the server
echo.

python main.py

pause
