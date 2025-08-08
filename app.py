import os
import logging
from flask import Flask

# Configure logging for debug mode
logging.basicConfig(level=logging.DEBUG)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")

# Configure upload settings
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['GENERATED_PROJECTS_FOLDER'] = 'generated_projects'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['GENERATED_PROJECTS_FOLDER'], exist_ok=True)

# Import routes after app creation to avoid circular imports
from routes import *

if __name__ == '__main__':
    # Use 0.0.0.0 for compatibility with different environments
    app.run(host='0.0.0.0', port=8080, debug=True)
