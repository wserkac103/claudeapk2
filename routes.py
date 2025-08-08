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

# Initialize services
gemini_service = GeminiService()
android_generator = AndroidGenerator()

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
    api_key_set = bool(config.get('gemini_api_key'))
    return render_template('index.html', api_key_set=api_key_set)

@app.route('/save_api_key', methods=['POST'])
def save_api_key():
    """Save Gemini API key to configuration"""
    try:
        api_key = request.form.get('api_key', '').strip()
        if not api_key:
            return jsonify({'success': False, 'message': 'API key cannot be empty'})
        
        config = load_config()
        config['gemini_api_key'] = api_key
        save_config(config)
        
        # Update the gemini service with new API key
        gemini_service.set_api_key(api_key)
        
        return jsonify({'success': True, 'message': 'API key saved successfully'})
    except Exception as e:
        app.logger.error(f"Error saving API key: {str(e)}")
        return jsonify({'success': False, 'message': f'Error saving API key: {str(e)}'})

@app.route('/test_api_key', methods=['POST'])
def test_api_key():
    """Test the Gemini API key with a simple call"""
    try:
        config = load_config()
        api_key = config.get('gemini_api_key')
        
        if not api_key:
            return jsonify({'success': False, 'message': 'No API key configured'})
        
        gemini_service.set_api_key(api_key)
        success, message = gemini_service.test_connection()
        
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
        api_key = config.get('gemini_api_key')
        
        if not api_key:
            return jsonify({'success': False, 'message': 'No API key configured'})
        
        prompt = request.form.get('prompt', '').strip()
        if not prompt:
            return jsonify({'success': False, 'message': 'Prompt cannot be empty'})
        
        uploaded_image = request.form.get('uploaded_image')
        image_path = None
        if uploaded_image:
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_image)
            if not os.path.exists(image_path):
                image_path = None
        
        gemini_service.set_api_key(api_key)
        
        # Generate Android app structure
        app_structure = gemini_service.generate_android_app(prompt, image_path)
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
        api_key = config.get('gemini_api_key')
        
        if not api_key:
            return jsonify({'success': False, 'message': 'No API key configured'})
        
        prompt = request.form.get('prompt', '').strip()
        if not prompt:
            return jsonify({'success': False, 'message': 'Prompt cannot be empty'})
        
        uploaded_image = request.form.get('uploaded_image')
        image_path = None
        if uploaded_image:
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_image)
            if not os.path.exists(image_path):
                image_path = None
        
        gemini_service.set_api_key(api_key)
        
        # Generate updated Android app structure for preview
        app_structure = gemini_service.generate_android_app(prompt, image_path, preview_only=True)
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
        logging.error(f"Error downloading complete Windows package: {str(e)}")
        flash(f'Error downloading complete Windows package: {str(e)}', 'error')
        return redirect(url_for('index'))
