import os
import json
import uuid
import zipfile
import shutil
from flask import render_template, request, jsonify, flash, redirect, url_for, send_file
from werkzeug.utils import secure_filename
from app import app
from gemini_service import GeminiService
from android_generator import AndroidGenerator
# Assuming you have other service classes like LlamaService, etc.
# from llama_service import LlamaService 

# Initialize services
gemini_service = GeminiService()
android_generator = AndroidGenerator()
# ai_service = None # Will be initialized based on provider

def allowed_file(filename):
    """Check if file extension is allowed"""
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def load_config():
    """Load configuration from config.json"""
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_config(config_data):
    """Save configuration to config.json"""
    with open('config.json', 'w') as f:
        json.dump(config_data, f, indent=2)

@app.route('/')
def index():
    """Main page with Android app generator interface"""
    config = load_config()
    api_key_set = bool(config.get('gemini_api_key')) # This might need to be generalized
    return render_template('index.html', api_key_set=api_key_set)

@app.route('/save_api_key', methods=['POST'])
def save_api_key():
    """Save API key and provider information to configuration"""
    try:
        data = request.get_json()
        api_key = data.get('api_key', '').strip()
        provider = data.get('provider', 'gemini').lower()
        api_url = data.get('api_url', None)

        if not api_key:
            return jsonify({'success': False, 'message': 'API key cannot be empty'})

        config = load_config()
        config['ai_provider'] = provider
        config['api_url'] = api_url
        
        # Store API key securely, perhaps not directly in config if sensitive
        if provider == 'gemini':
            config['gemini_api_key'] = api_key
        elif provider == 'llama':
            config['llama_api_key'] = api_key # Example for Llama

        save_config(config)

        # Initialize or update the appropriate AI service
        # This part needs to be dynamic based on the provider
        global ai_service # Use global to modify the service instance
        if provider == 'gemini':
            ai_service = GeminiService()
            ai_service.set_api_key(api_key)
        elif provider == 'llama':
            # Assuming LlamaService is available and takes api_key and optional api_url
            # ai_service = LlamaService(api_key=api_key, api_url=api_url)
            # For now, we'll just set a placeholder if LlamaService isn't fully integrated yet
            ai_service = GeminiService() # Placeholder, replace with actual LlamaService initialization
            ai_service.set_api_key(api_key) # Placeholder
            app.logger.warning("LlamaService not fully implemented. Using GeminiService as placeholder.")
        else:
            return jsonify({'success': False, 'message': f'Unsupported AI provider: {provider}'})

        return jsonify({'success': True, 'message': 'API configuration saved successfully'})
    except Exception as e:
        app.logger.error(f"Error saving API key/config: {str(e)}")
        return jsonify({'success': False, 'message': f'Error saving API configuration: {str(e)}'})

@app.route('/test_api_key', methods=['POST'])
def test_api_key():
    """Test the configured API key with a simple call"""
    try:
        config = load_config()
        provider = config.get('ai_provider', 'gemini')
        api_key = config.get('gemini_api_key') if provider == 'gemini' else config.get('llama_api_key') # Adjust based on provider
        api_url = config.get('api_url', None)

        if not api_key:
            return jsonify({'success': False, 'message': 'No API key configured for the selected provider'})

        # Initialize the correct service based on the provider
        current_ai_service = None
        if provider == 'gemini':
            current_ai_service = GeminiService()
            current_ai_service.set_api_key(api_key)
        elif provider == 'llama':
            # current_ai_service = LlamaService(api_key=api_key, api_url=api_url) # Assuming this is how LlamaService is initialized
            # Placeholder for LlamaService
            current_ai_service = GeminiService() # Placeholder
            current_ai_service.set_api_key(api_key) # Placeholder
            app.logger.warning("LlamaService not fully implemented for testing. Using GeminiService as placeholder.")

        if not current_ai_service:
            return jsonify({'success': False, 'message': f'AI service not initialized for provider: {provider}'})

        success, message = current_ai_service.test_connection()

        return jsonify({'success': success, 'message': message})
    except Exception as e:
        app.logger.error(f"Error testing API key: {str(e)}")
        return jsonify({'success': False, 'message': f'Error testing API key: {str(e)}'})

@app.route('/upload_image', methods=['POST'])
def upload_image():
    """Handle image upload for GUI design reference"""
    try:
        if 'image' not in request.files:
            return jsonify({'success': False, 'message': 'No image file provided'})

        file = request.files['image']
        if file.filename == '':
            return jsonify({'success': False, 'message': 'No file selected'})

        if file and file.filename and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Add unique prefix to avoid conflicts
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(file_path)

            return jsonify({
                'success': True, 
                'message': 'Image uploaded successfully',
                'filename': unique_filename,
                'file_path': file_path
            })
        else:
            return jsonify({'success': False, 'message': 'Invalid file type. Please upload PNG, JPG, JPEG, GIF, or WEBP files.'})
    except Exception as e:
        app.logger.error(f"Error uploading image: {str(e)}")
        return jsonify({'success': False, 'message': f'Error uploading image: {str(e)}'})

@app.route('/generate_app', methods=['POST'])
def generate_app():
    """Generate Android app based on prompt and optional image"""
    try:
        config = load_config()
        provider = config.get('ai_provider', 'gemini')
        api_key = config.get('gemini_api_key') if provider == 'gemini' else config.get('llama_api_key') # Adjust based on provider
        api_url = config.get('api_url', None)

        if not api_key:
            return jsonify({'success': False, 'message': 'No API key configured for the selected provider'})

        prompt = request.form.get('prompt', '').strip()
        if not prompt:
            return jsonify({'success': False, 'message': 'Prompt cannot be empty'})

        uploaded_image = request.form.get('uploaded_image')
        image_path = None
        if uploaded_image:
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_image)
            if not os.path.exists(image_path):
                image_path = None

        # Initialize the correct AI service
        current_ai_service = None
        if provider == 'gemini':
            current_ai_service = GeminiService()
            current_ai_service.set_api_key(api_key)
        elif provider == 'llama':
            # current_ai_service = LlamaService(api_key=api_key, api_url=api_url) # Assuming this is how LlamaService is initialized
            # Placeholder for LlamaService
            current_ai_service = GeminiService() # Placeholder
            current_ai_service.set_api_key(api_key) # Placeholder
            app.logger.warning("LlamaService not fully implemented for generation. Using GeminiService as placeholder.")

        if not current_ai_service:
            return jsonify({'success': False, 'message': f'AI service not initialized for provider: {provider}'})

        # Generate Android app structure
        app_structure = current_ai_service.generate_android_app(prompt, image_path)
        if not app_structure:
            return jsonify({'success': False, 'message': 'Failed to generate Android app structure'})

        # Create Android project files
        project_id = str(uuid.uuid4())
        project_path = android_generator.create_android_project(app_structure, project_id)

        # Generate preview HTML
        preview_html = android_generator.generate_preview_html(app_structure)

        return jsonify({
            'success': True,
            'message': 'Android app generated successfully',
            'project_id': project_id,
            'preview_html': preview_html,
            'app_structure': app_structure
        })

    except Exception as e:
        app.logger.error(f"Error generating app: {str(e)}")
        return jsonify({'success': False, 'message': f'Error generating app: {str(e)}'})

@app.route('/download_project/<project_id>')
def download_project(project_id):
    """Download generated Android project as ZIP file"""
    try:
        project_path = os.path.join(app.config['GENERATED_PROJECTS_FOLDER'], project_id)
        if not os.path.exists(project_path):
            flash('Project not found', 'error')
            return redirect(url_for('index'))

        # Create ZIP file
        zip_filename = f"android_app_{project_id}.zip"
        zip_path = os.path.join(app.config['GENERATED_PROJECTS_FOLDER'], zip_filename)

        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(project_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, project_path)
                    zipf.write(file_path, arcname)

        return send_file(zip_path, as_attachment=True, download_name=zip_filename)

    except Exception as e:
        app.logger.error(f"Error downloading project: {str(e)}")
        flash(f'Error downloading project: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/download_source')
def download_source():
    """Download the complete source code as ZIP for Windows testing"""
    try:
        zip_path = 'android-app-generator-windows.zip'
        if os.path.exists(zip_path):
            return send_file(zip_path, as_attachment=True, download_name='android-app-generator-windows.zip')
        else:
            flash('Source code package not found', 'error')
            return redirect(url_for('index'))
    except Exception as e:
        app.logger.error(f"Error downloading source: {str(e)}")
        flash(f'Error downloading source: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/update_preview', methods=['POST'])
def update_preview():
    """Update preview based on modified prompt"""
    try:
        config = load_config()
        provider = config.get('ai_provider', 'gemini')
        api_key = config.get('gemini_api_key') if provider == 'gemini' else config.get('llama_api_key') # Adjust based on provider
        api_url = config.get('api_url', None)

        if not api_key:
            return jsonify({'success': False, 'message': 'No API key configured for the selected provider'})

        prompt = request.form.get('prompt', '').strip()
        if not prompt:
            return jsonify({'success': False, 'message': 'Prompt cannot be empty'})

        uploaded_image = request.form.get('uploaded_image')
        image_path = None
        if uploaded_image:
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_image)
            if not os.path.exists(image_path):
                image_path = None

        # Initialize the correct AI service
        current_ai_service = None
        if provider == 'gemini':
            current_ai_service = GeminiService()
            current_ai_service.set_api_key(api_key)
        elif provider == 'llama':
            # current_ai_service = LlamaService(api_key=api_key, api_url=api_url) # Assuming this is how LlamaService is initialized
            # Placeholder for LlamaService
            current_ai_service = GeminiService() # Placeholder
            current_ai_service.set_api_key(api_key) # Placeholder
            app.logger.warning("LlamaService not fully implemented for preview. Using GeminiService as placeholder.")

        if not current_ai_service:
            return jsonify({'success': False, 'message': f'AI service not initialized for provider: {provider}'})

        # Generate updated Android app structure for preview
        app_structure = current_ai_service.generate_android_app(prompt, image_path, preview_only=True)
        if not app_structure:
            return jsonify({'success': False, 'message': 'Failed to generate preview. Please check your API key and try a simpler prompt.'})

        # Generate preview HTML
        preview_html = android_generator.generate_preview_html(app_structure)

        return jsonify({
            'success': True,
            'preview_html': preview_html
        })

    except Exception as e:
        app.logger.error(f"Error updating preview: {str(e)}")
        return jsonify({'success': False, 'message': f'Error updating preview: {str(e)}'})

@app.route('/download-windows-complete')
def download_windows_complete():
    """Download complete Windows ZIP package with fixes"""
    try:
        zip_path = 'android-app-complete-all-files.zip'
        if os.path.exists(zip_path):
            return send_file(zip_path, as_attachment=True, download_name='android-app-generator-windows-complete.zip')
        else:
            flash('Complete Windows package not available', 'error')
            return redirect(url_for('index'))
    except Exception as e:
        # Use logging module directly if app.logger is not available here
        import logging 
        logging.error(f"Error downloading complete Windows package: {str(e)}")
        flash(f'Error downloading complete Windows package: {str(e)}', 'error')
        return redirect(url_for('index'))