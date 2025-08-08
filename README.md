# Android App Generator

A powerful web application that generates complete Android mobile applications using AI-powered design analysis. Simply describe your app idea, optionally upload a design reference image, and get a fully functional Android project ready for Android Studio.

## 🚀 Features

### Core Functionality
- **AI-Powered Code Generation**: Uses Google's Gemini AI to generate complete Android projects
- **Visual Design Analysis**: Upload design reference images to guide app creation
- **Real-time Preview**: See how your app will look before downloading
- **Complete Project Structure**: Generates all necessary files for Android Studio
- **One-Click Download**: Get your project as a ready-to-import ZIP file

### Technical Capabilities
- **Modern Android Development**: Target SDK 33, Min SDK 21
- **Material Design UI**: Professional, responsive layouts
- **Java Implementation**: Clean, well-structured Java code
- **AndroidX Compatibility**: Uses latest Android libraries
- **Gradle Build System**: Ready for immediate compilation

### User Interface
- **Intuitive Web Interface**: Easy-to-use design with dark theme
- **API Key Management**: Secure handling of Gemini API credentials
- **Image Upload**: Drag-and-drop design reference support
- **Live Preview Updates**: See changes as you modify your prompt
- **Mobile-Responsive**: Works on desktop and mobile browsers

## 🛠️ Setup Instructions

### Prerequisites
- Python 3.7 or higher
- Google Gemini API key (free from https://ai.google.dev/)
- Web browser (Chrome, Firefox, Safari, Edge)

### Installation Steps

1. **Clone or Download** this project to your computer

2. **Install Dependencies** (if not already installed):
   ```bash
   pip install flask google-genai pillow gunicorn werkzeug
   ```

3. **Start the Server**:
   - **Windows**: Double-click `start.bat`
   - **Mac/Linux**: Run `python main.py`

4. **Open Your Browser** and go to: http://127.0.0.1:5001

## 📱 How to Use

### Step 1: Configure API Key
1. Visit https://ai.google.dev/ to get your free Gemini API key
2. In the web app, enter your API key in the "API Configuration" panel
3. Click "Save API Key" then "Test Connection" to verify it works

### Step 2: Describe Your App
1. In the "App Description" text area, describe your Android app idea
2. Be specific about features, colors, layout, and functionality
3. Example: "Create a todo app with a modern blue theme, featuring a list of tasks, add/edit buttons, and checkboxes to mark completed items"

### Step 3: Add Design Reference (Optional)
1. Upload an image of your desired app design in the "GUI Design Reference" section
2. Supported formats: PNG, JPG, JPEG, GIF, WebP
3. The AI will analyze your image and incorporate the design elements

### Step 4: Generate Preview
1. Click "Update Preview" to see how your app will look
2. Modify your description and update the preview as needed
3. The preview updates automatically as you type (with a 2-second delay)

### Step 5: Generate & Download
1. When satisfied with the preview, click "Generate Android App"
2. Wait for the AI to create your complete project (1-3 minutes)
3. Click "Download Android Project ZIP" to get your files

### Step 6: Import to Android Studio
1. Extract the downloaded ZIP file
2. Open Android Studio
3. Select "Open an existing Android Studio project"
4. Navigate to the extracted folder and select it
5. Wait for Gradle sync to complete
6. Build and run your app!

## 🔧 Configuration

### API Settings
- The app stores your API key securely in `config.json`
- You can update or change your API key anytime in the web interface
- API keys are not displayed in plain text for security

### File Limits
- Maximum image upload size: 16MB
- Supported image formats: PNG, JPG, JPEG, GIF, WebP
- Generated projects are stored temporarily in the `generated_projects/` folder

### Server Configuration
- Default server address: http://127.0.0.1:5001
- To change the port, edit `main.py` and `start.bat`
- For external access, change `127.0.0.1` to `0.0.0.0` in the configuration

## 📁 Project Structure

```
android-app-generator/
├── app.py                 # Flask application setup
├── main.py               # Application entry point
├── routes.py             # Web routes and API endpoints
├── gemini_service.py     # Gemini AI integration
├── android_generator.py  # Android project creation logic
├── start.bat            # Windows startup script
├── config.json          # Application configuration
├── templates/           # HTML templates
│   ├── base.html        # Base template
│   └── index.html       # Main page
├── static/              # CSS, JS, and other assets
│   ├── css/style.css    # Custom styles
│   └── js/app.js        # Frontend JavaScript
├── uploads/             # Temporary image storage
├── generated_projects/  # Generated Android projects
└── README.md           # This file
```

## 🎯 Example App Prompts

### Simple Apps
- "Create a calculator app with a clean white design and large buttons"
- "Make a note-taking app with dark theme and folder organization"
- "Build a timer app with circular progress and alarm sounds"

### Business Apps
- "Create a restaurant menu app with food categories and prices"
- "Make an inventory tracker with search and barcode scanning"
- "Build a customer feedback app with rating stars and comments"

### Entertainment Apps
- "Create a quiz app with multiple choice questions and scoring"
- "Make a photo gallery with swipe navigation and filters"
- "Build a music player with playlist management and controls"

## 🔒 Security & Privacy

- **API Keys**: Stored locally in config.json, never transmitted unnecessarily
- **Uploaded Images**: Automatically deleted after project generation
- **Generated Projects**: Stored temporarily, can be manually cleaned up
- **No Data Collection**: The app doesn't collect or store personal information

## 🆘 Troubleshooting

### Common Issues

**"API connection failed"**
- Verify your Gemini API key is correct
- Check your internet connection
- Ensure the API key has proper permissions

**"Image upload failed"**
- Check file size is under 16MB
- Verify file format is supported (PNG, JPG, JPEG, GIF, WebP)
- Try a different image file

**"App generation failed"**
- Make your app description more specific
- Try simplifying complex requirements
- Check the API key is working with "Test Connection"

**"Cannot start server"**
- Ensure Python 3.7+ is installed
- Install required packages: `pip install flask google-genai pillow`
- Check that port 5001 is not in use by another application

### Getting Help
- Check the browser console for error messages (F12)
- Look at the server console output for detailed error logs
- Ensure all dependencies are properly installed
- Try restarting the server if issues persist

## 🔄 Updates & Maintenance

### Keeping Up to Date
- Download the latest version from the source
- Your API key and generated projects will be preserved
- Clear the `uploads/` folder periodically to save disk space

### Performance Tips
- Close old browser tabs to free memory
- Clear generated projects after downloading to save space
- Use specific, detailed prompts for better AI results

## 📞 Support

This Android App Generator was created to make mobile app development accessible to everyone. For Android development questions, refer to the official Android documentation at https://developer.android.com/

**Powered by Google Gemini AI** 🤖