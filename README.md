
# Android App Generator

A powerful web application that generates complete Android mobile applications using AI-powered design analysis. Simply describe your app idea, optionally upload a design reference image, and get a fully functional Android project ready for Android Studio.

## 🚀 Features

### Core Functionality
- **Multi-AI Provider Support**: Works with Google Gemini, Groq (Free Llama), Ollama (Local), and Hugging Face
- **Visual Design Analysis**: Upload design reference images to guide app creation
- **Real-time Preview**: See how your app will look before downloading
- **Complete Project Structure**: Generates all necessary files for Android Studio
- **One-Click Download**: Get your project as a ready-to-import ZIP file

### Technical Capabilities
- **Modern Android Development**: Target SDK 34, Min SDK 21
- **Material Design UI**: Professional, responsive layouts
- **Java Implementation**: Clean, well-structured Java code
- **AndroidX Compatibility**: Uses latest Android libraries
- **Gradle Build System**: Ready for immediate compilation

### User Interface
- **Intuitive Web Interface**: Easy-to-use design with dark theme
- **Multiple AI Provider Support**: Choose from various free and paid options
- **Image Upload**: Drag-and-drop design reference support
- **Live Preview Updates**: See changes as you modify your prompt
- **Mobile-Responsive**: Works on desktop and mobile browsers

## 🤖 AI Provider Options

### 1. Google Gemini (Recommended)
- **Cost**: Free tier available, then paid
- **Quality**: Excellent code generation and image analysis
- **Setup**: Get API key from https://ai.google.dev/
- **Best for**: High-quality, complex apps with image analysis

### 2. Groq (Free Llama Models) ⭐ FREE
- **Cost**: Completely free with generous limits
- **Quality**: Very good code generation, no image analysis
- **Setup**: Get free API key from https://console.groq.com/
- **Best for**: Text-based app descriptions, cost-conscious users

### 3. Ollama (Local/Offline) ⭐ FREE & PRIVATE
- **Cost**: Completely free, runs on your computer
- **Quality**: Good code generation, no image analysis
- **Setup**: Install Ollama locally, no API key needed
- **Best for**: Privacy-conscious users, offline development

### 4. Hugging Face
- **Cost**: Free tier available
- **Quality**: Variable depending on model
- **Setup**: Get API key from https://huggingface.co/
- **Best for**: Experimental use, specific model requirements

## 🛠️ Setup Instructions

### Prerequisites
- Python 3.7 or higher
- Web browser (Chrome, Firefox, Safari, Edge)
- AI Provider API key (see provider sections below)

### Installation Steps

1. **Clone or Download** this project to your computer

2. **Install Dependencies**:
   ```bash
   pip install flask google-genai pillow gunicorn werkzeug requests
   ```

3. **Start the Server**:
   - **Windows**: Double-click `start.bat`
   - **Mac/Linux**: Run `python main.py` or `./start.sh`

4. **Open Your Browser** and go to: http://127.0.0.1:5001

## 🔑 AI Provider Setup Guide

### Option 1: Google Gemini (Best Quality)

1. **Get API Key**:
   - Visit https://ai.google.dev/
   - Sign in with Google account
   - Create new API key
   - Copy the key

2. **Configure in App**:
   - Select "Google Gemini" from provider dropdown
   - Paste your API key
   - Click "Save API Key" then "Test Connection"

### Option 2: Groq (Free Llama) ⭐ RECOMMENDED FREE

1. **Get Free API Key**:
   - Visit https://console.groq.com/
   - Sign up for free account
   - Navigate to API Keys section
   - Create new API key
   - Copy the key

2. **Configure in App**:
   - Select "Groq (Free Llama Models)" from provider dropdown
   - Paste your API key
   - Click "Save API Key" then "Test Connection"

### Option 3: Ollama (Local/Offline) ⭐ PRIVACY FOCUSED

1. **Install Ollama**:
   ```bash
   # Windows/Mac: Download from https://ollama.ai/
   # Linux:
   curl -fsSL https://ollama.ai/install.sh | sh
   ```

2. **Download Llama Model**:
   ```bash
   ollama pull llama3.2
   ```

3. **Start Ollama Server**:
   ```bash
   ollama serve
   ```

4. **Configure in App**:
   - Select "Ollama (Local Llama)" from provider dropdown
   - Leave API key empty (not needed)
   - Optionally set custom URL (default: http://localhost:11434)
   - Click "Save API Key" then "Test Connection"

### Option 4: Hugging Face

1. **Get API Key**:
   - Visit https://huggingface.co/
   - Create account and go to Settings → Access Tokens
   - Create new token with "read" permissions
   - Copy the token

2. **Configure in App**:
   - Select "Hugging Face" from provider dropdown
   - Paste your token as API key
   - Click "Save API Key" then "Test Connection"

## 📱 How to Use

### Step 1: Configure AI Provider
1. Choose your preferred AI provider from the dropdown
2. Enter your API key (if required)
3. Click "Save API Key" then "Test Connection" to verify

### Step 2: Describe Your App
1. In the "App Description" text area, describe your Android app idea
2. Be specific about features, colors, layout, and functionality
3. Example: "Create a todo app with a modern blue theme, featuring a list of tasks, add/edit buttons, and checkboxes to mark completed items"

### Step 3: Add Design Reference (Optional)
1. Upload an image of your desired app design (Gemini only)
2. Supported formats: PNG, JPG, JPEG, GIF, WebP
3. The AI will analyze your image and incorporate design elements

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
4. Navigate to and select the extracted folder
5. Wait for Gradle sync to complete
6. Build and run your app!

## 💡 Tips for Better Results

### Prompt Writing Tips
- **Be Specific**: Include colors, layout details, and exact features
- **Use Examples**: "Like Instagram but for recipes"
- **Mention UI Elements**: "With floating action button", "navigation drawer"
- **Specify Interactions**: "Swipe to delete", "pull to refresh"

### Provider Selection Guide
- **Complex Apps**: Use Gemini for best results
- **Simple Apps**: Groq works great and is free
- **Privacy Concerns**: Use Ollama for local processing
- **Budget Conscious**: Start with Groq, upgrade to Gemini if needed

### Example Prompts

#### Simple Apps (Good for all providers)
```
Create a calculator app with a clean white design and large buttons
Make a note-taking app with dark theme and folder organization
Build a timer app with circular progress and alarm sounds
```

#### Complex Apps (Best with Gemini)
```
Create a social media app like Instagram but for cooking recipes. Include photo uploads, recipe steps, ingredient lists, rating system, and user profiles. Use a warm color scheme with orange and cream colors.
```

#### Business Apps
```
Create a restaurant menu app with food categories, prices, and ordering system
Make an inventory tracker with barcode scanning and low stock alerts
Build a customer feedback app with rating stars and comment system
```

## 🔧 Configuration

### AI Provider Settings
- The app stores your API keys securely in `config.json`
- You can switch providers anytime in the web interface
- API keys are not displayed in plain text for security

### File Limits
- Maximum image upload size: 16MB
- Supported image formats: PNG, JPG, JPEG, GIF, WebP
- Generated projects are stored temporarily in `generated_projects/`

### Server Configuration
- Default server address: http://127.0.0.1:5001
- To change the port, edit `main.py` and `start.bat`
- For external access, change `127.0.0.1` to `0.0.0.0`

## 🆘 Troubleshooting

### API Issues

**"API connection failed"**
- Verify your API key is correct for the selected provider
- Check your internet connection (except for Ollama)
- Ensure the API key has proper permissions

**"Rate limit exceeded" (Gemini)**
- Switch to Groq (free with higher limits)
- Wait for rate limit reset
- Upgrade your Gemini plan

**"Ollama server not responding"**
- Ensure Ollama is installed and running: `ollama serve`
- Check if the model is downloaded: `ollama pull llama3.2`
- Verify the server URL (default: http://localhost:11434)

### App Issues

**"Image upload failed"**
- Check file size is under 16MB
- Verify file format is supported
- Note: Only Gemini supports image analysis

**"App generation failed"**
- Make your app description more specific
- Try a different AI provider
- Simplify complex requirements

**"Cannot start server"**
- Ensure Python 3.7+ is installed
- Install required packages: `pip install -r requirements.txt`
- Check that port 5001 is not in use

## 📁 Project Structure

```
android-app-generator/
├── app.py                 # Flask application setup
├── main.py               # Application entry point
├── routes.py             # Web routes and API endpoints
├── gemini_service.py     # Multi-provider AI integration
├── android_generator.py  # Android project creation logic
├── start.bat/.sh         # Startup scripts
├── config.json          # Application configuration
├── templates/           # HTML templates
│   ├── base.html        # Base template
│   └── index.html       # Main page
├── static/              # CSS, JS, and other assets
├── uploads/             # Temporary image storage
├── generated_projects/  # Generated Android projects
└── README.md           # This file
```

## 🔒 Security & Privacy

- **API Keys**: Stored locally in config.json, never transmitted unnecessarily
- **Uploaded Images**: Automatically deleted after project generation
- **Generated Projects**: Stored temporarily, can be manually cleaned up
- **Ollama**: Completely offline processing for maximum privacy
- **No Data Collection**: The app doesn't collect or store personal information

## 🆓 Cost Comparison

| Provider | Cost | Quality | Image Support | Privacy |
|----------|------|---------|---------------|---------|
| **Groq** | Free ⭐ | Excellent | No | Medium |
| **Ollama** | Free ⭐ | Good | No | Maximum ⭐ |
| **Gemini** | Free tier + Paid | Excellent ⭐ | Yes ⭐ | Medium |
| **Hugging Face** | Free tier + Paid | Variable | No | Medium |

## 🔄 Updates & Maintenance

### Keeping Up to Date
- Download the latest version from the source
- Your API keys and generated projects will be preserved
- Clear the `uploads/` folder periodically to save disk space

### Performance Tips
- Use Groq for fast, free generation
- Use Ollama for offline development
- Use Gemini for complex apps requiring image analysis
- Clear generated projects after downloading to save space

## 📞 Support

This Android App Generator was created to make mobile app development accessible to everyone using various AI providers. 

**Available AI Providers:**
- 🤖 **Google Gemini** - Premium quality with image analysis
- ⚡ **Groq** - Free, fast Llama models
- 🏠 **Ollama** - Local, private processing
- 🤗 **Hugging Face** - Open source models

For Android development questions, refer to the official Android documentation at https://developer.android.com/

**Powered by Multiple AI Providers** 🚀
