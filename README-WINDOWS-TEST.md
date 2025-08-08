
# Android App Generator - Windows Test Package

## Quick Setup for Windows Testing

1. **Extract ZIP** to a folder like `C:\android-app-generator\`

2. **Install Python 3.7+** from https://python.org
   - ⚠️ **IMPORTANT**: Check "Add Python to PATH" during installation

3. **Install Dependencies**:
   - Double-click `install-dependencies.bat`
   - Wait for completion (2-3 minutes)

4. **Start Application**:
   - Double-click `start.bat`
   - Browser opens to http://127.0.0.1:5001

5. **Get Gemini API Key**:
   - Visit https://ai.google.dev/
   - Sign in and create API key
   - Paste in web interface

## Files Included

- `main.py` - Application entry point
- `app.py` - Flask application setup  
- `routes.py` - Web routes and handlers
- `gemini_service.py` - AI integration
- `android_generator.py` - Android project generator
- `config.json` - Configuration file
- `start.bat` - Windows startup script
- `install-dependencies.bat` - Dependency installer
- `requirements.txt` - Python packages list
- `templates/` - HTML templates
- `static/` - CSS and JavaScript
- `uploads/` - File upload directory
- `generated_projects/` - Output directory

## Troubleshooting

- **Python not found**: Reinstall with PATH option
- **Module errors**: Run install-dependencies.bat first  
- **Port issues**: Ensure port 5001 is available
- **API errors**: Verify Gemini API key is valid

The application includes fallback functionality when AI service is unavailable.
