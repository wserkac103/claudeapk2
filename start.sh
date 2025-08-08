
#!/bin/bash

# Navigate to the app directory
cd android-app-generator-windows-final

# Check if there's a Python script to run
if [ -f "main.py" ]; then
    echo "Starting Android App Generator..."
    python main.py
elif [ -f "app.py" ]; then
    echo "Starting Android App Generator..."
    python app.py
elif [ -f "start.py" ]; then
    echo "Starting Android App Generator..."
    python start.py
else
    echo "Looking for executable files..."
    # List all potential executable files
    find . -name "*.py" -o -name "*.js" | head -5
    echo "Please specify which file should be run"
fi
