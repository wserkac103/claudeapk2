import os
import json
import logging
from app import app

class AndroidGenerator:
    def __init__(self):
        self.base_project_structure = {
            'app/src/main/java/': {},
            'app/src/main/res/layout/': {},
            'app/src/main/res/values/': {},
            'app/src/main/res/drawable/': {},
            'app/src/main/': {},
            'app/': {}
        }

    def create_android_project(self, app_structure, project_id):
        """Create complete Android project structure with generated code"""
        try:
            project_path = os.path.join(app.config['GENERATED_PROJECTS_FOLDER'], project_id)
            os.makedirs(project_path, exist_ok=True)

            # Extract package name and create directory structure
            package_name = app_structure.get('package_name', 'com.example.myapp')
            package_path = package_name.replace('.', '/')

            # Create directory structure
            directories = [
                f'app/src/main/java/{package_path}',
                'app/src/main/res/layout',
                'app/src/main/res/values',
                'app/src/main/res/drawable',
                'app/src/main/res/mipmap-hdpi',
                'app/src/main/res/mipmap-mdpi',
                'app/src/main/res/mipmap-xhdpi',
                'app/src/main/res/mipmap-xxhdpi',
                'app/src/main/res/mipmap-xxxhdpi'
            ]

            for directory in directories:
                os.makedirs(os.path.join(project_path, directory), exist_ok=True)

            # Create MainActivity.java
            main_activity = app_structure.get('main_activity', {})
            if main_activity.get('java_code'):
                with open(os.path.join(project_path, f'app/src/main/java/{package_path}/MainActivity.java'), 'w') as f:
                    f.write(main_activity['java_code'])

            # Create additional activities
            additional_activities = app_structure.get('additional_activities', [])
            for activity in additional_activities:
                if activity.get('java_code'):
                    activity_name = activity.get('name', 'Activity')
                    with open(os.path.join(project_path, f'app/src/main/java/{package_path}/{activity_name}.java'), 'w') as f:
                        f.write(activity['java_code'])

            # Create layout files
            if main_activity.get('xml_layout'):
                layout_name = main_activity.get('layout', 'activity_main')
                with open(os.path.join(project_path, f'app/src/main/res/layout/{layout_name}.xml'), 'w') as f:
                    f.write(main_activity['xml_layout'])

            # Create additional layout files
            for activity in additional_activities:
                if activity.get('xml_layout'):
                    layout_name = activity.get('layout', 'layout')
                    with open(os.path.join(project_path, f'app/src/main/res/layout/{layout_name}.xml'), 'w') as f:
                        f.write(activity['xml_layout'])

            # Create resource files
            resource_files = {
                'strings.xml': app_structure.get('strings'),
                'colors.xml': app_structure.get('colors'),
                'styles.xml': app_structure.get('styles')
            }

            for filename, content in resource_files.items():
                if content:
                    with open(os.path.join(project_path, f'app/src/main/res/values/{filename}'), 'w') as f:
                        f.write(content)

            # Create AndroidManifest.xml
            if app_structure.get('manifest'):
                with open(os.path.join(project_path, 'app/src/main/AndroidManifest.xml'), 'w') as f:
                    f.write(app_structure['manifest'])

            # Create build.gradle
            if app_structure.get('gradle'):
                with open(os.path.join(project_path, 'app/build.gradle'), 'w') as f:
                    f.write(app_structure['gradle'])
            else:
                # Create default build.gradle
                default_gradle = self.generate_default_gradle(app_structure)
                with open(os.path.join(project_path, 'app/build.gradle'), 'w') as f:
                    f.write(default_gradle)

            # Create project-level build.gradle
            project_gradle = self.generate_project_gradle()
            with open(os.path.join(project_path, 'build.gradle'), 'w') as f:
                f.write(project_gradle)

            # Create settings.gradle
            with open(os.path.join(project_path, 'settings.gradle'), 'w') as f:
                f.write("include ':app'\n")

            # Create gradle.properties
            gradle_props = self.generate_gradle_properties()
            with open(os.path.join(project_path, 'gradle.properties'), 'w') as f:
                f.write(gradle_props)

            # Create Gradle wrapper files
            self.create_gradle_wrapper(project_path)

            # Create README.md
            readme_content = self.generate_readme(app_structure)
            with open(os.path.join(project_path, 'README.md'), 'w') as f:
                f.write(readme_content)

            return project_path

        except Exception as e:
            logging.error(f"Error creating Android project: {str(e)}")
            return None

    def generate_preview_html(self, app_structure):
        """Generate HTML preview of the Android app GUI"""
        try:
            app_name = app_structure.get('app_name', 'My Android App')
            ui_components = app_structure.get('ui_components', [])

            # Extract colors for theming
            colors_xml = app_structure.get('colors', '')
            primary_color = self.extract_color(colors_xml, 'colorPrimary', '#2196F3')
            accent_color = self.extract_color(colors_xml, 'colorAccent', '#FF4081')

            # Generate HTML for UI components
            components_html = ""
            for component in ui_components:
                comp_type = component.get('type', 'TextView')
                comp_text = component.get('text', 'Component')
                comp_id = component.get('id', 'component')

                if comp_type == 'Button':
                    components_html += f'''
                    <button class="btn btn-primary mb-2 w-100" style="background-color: {primary_color};">
                        {comp_text}
                    </button>
                    '''
                elif comp_type == 'TextView':
                    components_html += f'''
                    <p class="mb-2">{comp_text}</p>
                    '''
                elif comp_type == 'EditText':
                    components_html += f'''
                    <input type="text" class="form-control mb-2" placeholder="{comp_text}">
                    '''
                elif comp_type == 'ImageView':
                    components_html += f'''
                    <div class="mb-2 p-3 border rounded text-center" style="background-color: #f8f9fa;">
                        <i class="fas fa-image fa-2x text-muted"></i>
                        <p class="mt-2 mb-0 small text-muted">{comp_text}</p>
                    </div>
                    '''
                else:
                    components_html += f'''
                    <div class="mb-2 p-2 border rounded">
                        <small class="text-muted">{comp_type}:</small> {comp_text}
                    </div>
                    '''

            preview_html = f'''
            <div class="card">
                <div class="card-header text-center" style="background-color: {primary_color}; color: white;">
                    <h5 class="mb-0">{app_name}</h5>
                </div>
                <div class="card-body" style="min-height: 400px;">
                    {components_html if components_html else '<p class="text-muted text-center">No UI components defined yet. Add more details to your prompt to see the interface.</p>'}
                </div>
                <div class="card-footer text-center">
                    <small class="text-muted">Android App Preview</small>
                </div>
            </div>
            '''

            return preview_html

        except Exception as e:
            logging.error(f"Error generating preview HTML: {str(e)}")
            return '<div class="alert alert-warning">Could not generate preview</div>'

    def extract_color(self, colors_xml, color_name, default_color):
        """Extract color value from colors.xml content"""
        try:
            if colors_xml and color_name in colors_xml:
                # Simple extraction - look for the color value
                start = colors_xml.find(f'name="{color_name}"')
                if start >= 0:
                    start = colors_xml.find('>', start) + 1
                    end = colors_xml.find('<', start)
                    if end > start:
                        color_value = colors_xml[start:end].strip()
                        if color_value.startswith('#'):
                            return color_value
            return default_color
        except:
            return default_color

    def generate_default_gradle(self, app_structure):
        """Generate default build.gradle for app module"""
        package_name = app_structure.get('package_name', 'com.example.myapp')
        app_name = app_structure.get('app_name', 'MyApp').replace(' ', '')

        return f'''apply plugin: 'com.android.application'

android {{
    namespace '{package_name}'
    compileSdk 33

    defaultConfig {{
        applicationId "{package_name}"
        minSdk 21
        targetSdk 33
        versionCode 1
        versionName "1.0"

        testInstrumentationRunner "androidx.test.runner.AndroidJUnitRunner"
    }}

    buildTypes {{
        release {{
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }}
    }}
    compileOptions {{
        sourceCompatibility JavaVersion.VERSION_11
        targetCompatibility JavaVersion.VERSION_11
    }}
}}

dependencies {{
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'com.google.android.material:material:1.8.0'
    implementation 'androidx.constraintlayout:constraintlayout:2.1.4'
    testImplementation 'junit:junit:4.13.2'
    androidTestImplementation 'androidx.test.ext:junit:1.1.5'
    androidTestImplementation 'androidx.test.espresso:espresso-core:3.5.1'
}}'''

    def generate_project_gradle(self):
        """Generate project-level build.gradle"""
        return '''// Top-level build file where you can add configuration options common to all sub-projects/modules.
plugins {
    id 'com.android.application' version '7.4.2' apply false
    id 'com.android.library' version '7.4.2' apply false
}

task clean(type: Delete) {
    delete rootProject.buildDir
}'''

    def generate_gradle_properties(self):
        """Generate gradle.properties"""
        return '''# Project-wide Gradle settings.
# IDE (e.g. Android Studio) users:
# Gradle settings configured through the IDE *will override*
# any settings specified in this file.
# For more details on how to configure your build environment visit
# http://www.gradle.org/docs/current/userguide/build_environment.html
# Specifies the JVM arguments used for the daemon process.
# The setting is particularly useful for tweaking memory settings.
org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8
# When configured, Gradle will run in incubating parallel mode.
# This option should only be used with decoupled projects. More details, visit
# http://www.gradle.org/docs/current/userguide/multi_project_builds.html#sec:decoupled_projects
# org.gradle.parallel=true
# AndroidX package structure to make it clearer which packages are bundled with the
# Android operating system, and which are packaged with your app"s APK
# https://developer.android.com/topic/libraries/support-library/androidx-rn
android.useAndroidX=true
# Enables namespacing of each library's R class so that its R class includes only the
# resources declared in the library itself and none from the library's dependencies,
# thereby reducing the size of the R class for that library
android.nonTransitiveRClass=true
# Automatically convert third-party libraries to use AndroidX
android.enableJetifier=true'''

    def create_gradle_wrapper(self, project_path):
        """Create Gradle wrapper files"""
        gradle_wrapper_dir = os.path.join(project_path, 'gradle', 'wrapper')
        os.makedirs(gradle_wrapper_dir, exist_ok=True)

        # Create gradle-wrapper.properties
        with open(os.path.join(gradle_wrapper_dir, 'gradle-wrapper.properties'), 'w') as f:
            f.write("distributionBase=GRADLE_USER_HOME\n")
            f.write("distributionPath=wrapper/dists\n")
            f.write("distributionUrl=https\\://services.gradle.org/distributions/gradle-7.6-bin.zip\n")
            f.write("zipStoreBase=GRADLE_USER_HOME\n")
            f.write("zipStorePath=wrapper/dists\n")

        # Create gradlew (Linux/macOS)
        with open(os.path.join(project_path, 'gradlew'), 'w') as f:
            f.write("#!/usr/bin/env sh\n")
            f.write("eval \"$(dirname $0)/gradlew\" \"$@\"\n")
        os.chmod(os.path.join(project_path, 'gradlew'), 0o755)

        # Create gradlew.bat (Windows)
        with open(os.path.join(project_path, 'gradlew.bat'), 'w') as f:
            f.write("@echo off\n")
            f.write("if not defined PROG do set PROG=%0\n")
            f.write("call \"%PROG%\" --sys-prop org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8 \"%@\"\n")


    def generate_readme(self, app_structure):
        """Generate README.md for the Android project"""
        app_name = app_structure.get('app_name', 'Android App')
        description = app_structure.get('description', 'Generated Android application')
        package_name = app_structure.get('package_name', 'com.example.myapp')

        return f'''# {app_name}

{description}

## Project Information
- **Package Name**: {package_name}
- **Generated**: Automatically created using Gemini AI
- **Target SDK**: 33
- **Min SDK**: 21

## Features
This Android application includes:
- Modern Material Design UI
- Responsive layouts
- Java-based implementation
- AndroidX compatibility

## Getting Started

### Prerequisites
- Android Studio (latest version recommended)
- Android SDK 33
- Java Development Kit (JDK) 8 or higher

### Installation
1. Open Android Studio
2. Select "Open an existing Android Studio project"
3. Navigate to and select this project folder
4. Wait for Gradle sync to complete
5. Build and run the app on your device or emulator

### Building the App
1. In Android Studio, go to Build → Build Bundle(s) / APK(s) → Build APK(s)
2. Once built, the APK will be located in `app/build/outputs/apk/`

## Project Structure
```
app/
├── src/main/
│   ├── java/           # Java source files
│   ├── res/           # Resources (layouts, values, etc.)
│   └── AndroidManifest.xml
├── build.gradle       # App-level build configuration
└── README.md          # This file
```

## Support
This project was generated using AI. For Android development help, refer to the official Android documentation at https://developer.android.com/
'''