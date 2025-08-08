import google.generativeai as genai
import os
import logging
import json
from PIL import Image

class GeminiService:
    def __init__(self):
        self.api_key = None

    def set_api_key(self, api_key):
        """Set the Gemini API key and configure the client"""
        try:
            self.api_key = api_key
            genai.configure(api_key=api_key)
            return True
        except Exception as e:
            logging.error(f"Error setting API key: {str(e)}")
            return False

    def test_connection(self):
        """Test the Gemini API connection with a simple call"""
        try:
            if not self.api_key:
                return False, "API key not set"

            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content("Hello, this is a test. Please respond with 'API connection successful.'")

            if response.text and "API connection successful" in response.text:
                return True, "API connection successful"
            elif response.text:
                return True, f"API connected. Response: {response.text[:100]}"
            else:
                return False, "API response was empty"

        except Exception as e:
            logging.error(f"Error testing API connection: {str(e)}")
            return False, f"API connection failed: {str(e)}"

    def analyze_image(self, image_path):
        """Analyze uploaded image for GUI design insights"""
        try:
            if not self.api_key:
                return None

            model = genai.GenerativeModel('gemini-1.5-pro')
            
            # Load and prepare the image
            with open(image_path, "rb") as f:
                image_data = f.read()
            
            # Create the image part
            image_part = {
                "mime_type": "image/jpeg",
                "data": image_data
            }
            
            prompt = "Analyze this image and describe what kind of mobile app UI design it represents. Focus on layout, colors, components, and user interface elements that could be implemented in an Android app."
            
            response = model.generate_content([prompt, image_part])
            return response.text if response.text else "Could not analyze image"

        except Exception as e:
            logging.error(f"Error analyzing image: {str(e)}")
            return None

    def generate_android_app(self, prompt, image_path=None, preview_only=False):
        """Generate Android app structure based on prompt and optional image"""
        try:
            if not self.api_key:
                return None

            model = genai.GenerativeModel('gemini-1.5-pro')

            # Add image analysis if provided
            image_analysis = ""
            if image_path and os.path.exists(image_path):
                image_analysis = self.analyze_image(image_path)
                if image_analysis:
                    prompt = f"GUI Design Reference: {image_analysis}\n\nUser Requirements: {prompt}"
                else:
                    prompt = f"User Requirements: {prompt}"
            else:
                prompt = f"User Requirements: {prompt}"

            # Create the main prompt
            full_prompt = f"""You are an expert Android app developer. Generate a complete Android app structure based on the user's requirements.

{prompt}

Return your response as valid JSON with the following structure:
{{
  "app_name": "App Name",
  "package_name": "com.example.appname",
  "description": "Brief description of the app",
  "main_activity": {{
    "name": "MainActivity",
    "layout": "activity_main",
    "java_code": "Complete Java code for MainActivity",
    "xml_layout": "Complete XML layout code"
  }},
  "additional_activities": [
    {{
      "name": "ActivityName",
      "layout": "layout_name",
      "java_code": "Complete Java code",
      "xml_layout": "Complete XML layout code"
    }}
  ],
  "styles": "Complete styles.xml content",
  "colors": "Complete colors.xml content",
  "strings": "Complete strings.xml content",
  "manifest": "Complete AndroidManifest.xml content",
  "gradle": "Complete build.gradle content",
  "ui_components": [
    {{
      "type": "Button|TextView|ImageView|etc",
      "id": "component_id",
      "text": "display text",
      "properties": {{}}
    }}
  ]
}}

Make sure all code is complete, functional, and follows Android development best practices. Return only the JSON, no other text."""

            response = model.generate_content(full_prompt)

            if not response.text:
                return None

            # Parse the JSON response
            try:
                # Clean the response text
                text = response.text.strip()

                # Check if response starts with HTML (error page)
                if text.startswith('<'):
                    logging.error(f"Received HTML response instead of JSON: {text[:200]}")
                    return None

                # Try direct JSON parsing first
                app_structure = json.loads(text)
                return app_structure

            except json.JSONDecodeError as e:
                logging.error(f"JSON decode error: {str(e)}")
                # Try to extract JSON from the response
                text = response.text.strip()
                start = text.find('{')
                end = text.rfind('}') + 1

                if start >= 0 and end > start:
                    try:
                        json_part = text[start:end]
                        app_structure = json.loads(json_part)
                        return app_structure
                    except json.JSONDecodeError as inner_e:
                        logging.error(f"Failed to parse extracted JSON: {str(inner_e)}")
                        logging.error(f"Raw response: {text[:500]}")
                        return None
                else:
                    logging.error("Could not find JSON structure in response")
                    logging.error(f"Raw response: {text[:500]}")
                    return None

        except Exception as e:
            logging.error(f"Error generating Android app: {str(e)}")
            # Always return a fallback structure when API fails
            return self.get_fallback_app_structure(prompt)

    def get_fallback_app_structure(self, prompt):
        """Generate a basic fallback app structure when API fails"""
        app_name = "Demo App"
        if "todo" in prompt.lower():
            app_name = "Todo App"
        elif "calculator" in prompt.lower():
            app_name = "Calculator"
        elif "note" in prompt.lower():
            app_name = "Notes App"

        return {
            "app_name": app_name,
            "package_name": "com.example.demoapp",
            "description": f"A simple {app_name.lower()} created from your prompt",
            "ui_components": [
                {
                    "type": "TextView",
                    "id": "title",
                    "text": f"Welcome to {app_name}",
                    "properties": {}
                },
                {
                    "type": "Button",
                    "id": "main_button",
                    "text": "Get Started",
                    "properties": {}
                },
                {
                    "type": "TextView",
                    "id": "description",
                    "text": "This is a preview based on your prompt. Generate the full app to get complete functionality.",
                    "properties": {}
                }
            ]
        }