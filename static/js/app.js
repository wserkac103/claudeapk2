// Global variables
let uploadedImageFilename = null;
let currentProjectId = null;

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // DOM elements
    const apiKeyInput = document.getElementById('apiKey');
    const toggleApiKeyBtn = document.getElementById('toggleApiKey');
    const saveApiKeyBtn = document.getElementById('saveApiKey');
    const testApiKeyBtn = document.getElementById('testApiKey');
    const apiStatusDiv = document.getElementById('apiStatus');
    const imageUpload = document.getElementById('imageUpload');
    const imagePreview = document.getElementById('imagePreview');
    const previewImg = document.getElementById('previewImg');
    const removeImageBtn = document.getElementById('removeImage');
    const appPrompt = document.getElementById('appPrompt');
    const updatePreviewBtn = document.getElementById('updatePreview');
    const appGeneratorForm = document.getElementById('appGeneratorForm');
    const generationStatusDiv = document.getElementById('generationStatus');
    const previewPanel = document.getElementById('previewPanel');
    const appPreview = document.getElementById('appPreview');
    const downloadPanel = document.getElementById('downloadPanel');
    const downloadBtn = document.getElementById('downloadBtn');
    const loadingModal = new bootstrap.Modal(document.getElementById('loadingModal'));

    // Utility functions
    function showApiStatus(message, type) {
        const alertClass = type === 'success' ? 'alert-success' : 
                          type === 'error' ? 'alert-danger' : 'alert-info';
        apiStatusDiv.innerHTML = `<div class="alert ${alertClass} mb-0">${message}</div>`;
    }

    function showGenerationStatus(message, type) {
        const alertClass = type === 'success' ? 'alert-success' : 
                          type === 'error' ? 'alert-danger' : 'alert-info';
        generationStatusDiv.innerHTML = `<div class="alert ${alertClass}">${message}</div>`;
    }

    function showLoadingModal(title, subtitle) {
        document.getElementById('loadingText').textContent = title;
        document.getElementById('loadingSubtext').textContent = subtitle;
        loadingModal.show();
    }

    function hideLoadingModal() {
        loadingModal.hide();
    }

    // API Key functionality
    if (toggleApiKeyBtn) {
        toggleApiKeyBtn.addEventListener('click', function() {
            const type = apiKeyInput.type === 'password' ? 'text' : 'password';
            apiKeyInput.type = type;
            const icon = this.querySelector('i');
            icon.className = type === 'password' ? 'fas fa-eye' : 'fas fa-eye-slash';
        });
    }

    if (saveApiKeyBtn) {
        saveApiKeyBtn.addEventListener('click', async function() {
            const apiKey = apiKeyInput.value.trim();
            if (!apiKey) {
                showApiStatus('Please enter an API key', 'error');
                return;
            }

            try {
                const formData = new FormData();
                formData.append('api_key', apiKey);

                const response = await fetch('/save_api_key', {
                    method: 'POST',
                    body: formData
                });

                const result = await response.json();

                if (result.success) {
                    showApiStatus(result.message, 'success');
                    if (testApiKeyBtn) testApiKeyBtn.disabled = false;
                    apiKeyInput.value = '';
                } else {
                    showApiStatus(result.message, 'error');
                }
            } catch (error) {
                showApiStatus('Error saving API key: ' + error.message, 'error');
            }
        });
    }

    if (testApiKeyBtn) {
        testApiKeyBtn.addEventListener('click', async function() {
            try {
                showApiStatus('Testing API connection...', 'info');

                const response = await fetch('/test_api_key', {
                    method: 'POST'
                });

                const result = await response.json();

                if (result.success) {
                    showApiStatus(result.message, 'success');
                } else {
                    showApiStatus(result.message, 'error');
                }
            } catch (error) {
                showApiStatus('Error testing API key: ' + error.message, 'error');
            }
        });
    }

    // Image upload functionality
    if (imageUpload) {
        imageUpload.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (!file) return;

            const formData = new FormData();
            formData.append('image', file);

            // Show preview immediately
            const reader = new FileReader();
            reader.onload = function(e) {
                if (previewImg) previewImg.src = e.target.result;
                if (imagePreview) imagePreview.style.display = 'block';
            };
            reader.readAsDataURL(file);

            // Upload file
            fetch('/upload_image', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(result => {
                if (result.success) {
                    uploadedImageFilename = result.filename;
                } else {
                    showGenerationStatus(result.message, 'error');
                    if (imagePreview) imagePreview.style.display = 'none';
                }
            })
            .catch(error => {
                showGenerationStatus('Error uploading image: ' + error.message, 'error');
                if (imagePreview) imagePreview.style.display = 'none';
            });
        });
    }

    if (removeImageBtn) {
        removeImageBtn.addEventListener('click', function() {
            if (imageUpload) imageUpload.value = '';
            if (imagePreview) imagePreview.style.display = 'none';
            uploadedImageFilename = null;
        });
    }

    // Preview functionality
    if (updatePreviewBtn) {
        updatePreviewBtn.addEventListener('click', async function() {
            const prompt = appPrompt ? appPrompt.value.trim() : '';
            if (!prompt) {
                showGenerationStatus('Please enter an app description', 'error');
                return;
            }

            try {
                showLoadingModal('Generating preview...', 'Please wait while we create your app preview');

                const formData = new FormData();
                formData.append('prompt', prompt);
                if (uploadedImageFilename) {
                    formData.append('uploaded_image', uploadedImageFilename);
                }

                const response = await fetch('/update_preview', {
                    method: 'POST',
                    body: formData
                });

                const result = await response.json();

                hideLoadingModal();

                if (result.success) {
                    if (appPreview) appPreview.innerHTML = result.preview_html;
                    if (previewPanel) {
                        previewPanel.style.display = 'block';
                        previewPanel.scrollIntoView({ behavior: 'smooth' });
                    }
                } else {
                    showGenerationStatus(result.message, 'error');
                }
            } catch (error) {
                hideLoadingModal();
                showGenerationStatus('Error generating preview: ' + error.message, 'error');
            }
        });
    }

    // App generation functionality
    if (appGeneratorForm) {
        appGeneratorForm.addEventListener('submit', async function(e) {
            e.preventDefault();

            const prompt = appPrompt ? appPrompt.value.trim() : '';
            if (!prompt) {
                showGenerationStatus('Please enter an app description', 'error');
                return;
            }

            try {
                showLoadingModal('Generating Android app...', 'This may take a few minutes while AI creates your complete project');

                const formData = new FormData();
                formData.append('prompt', prompt);
                if (uploadedImageFilename) {
                    formData.append('uploaded_image', uploadedImageFilename);
                }

                const response = await fetch('/generate_app', {
                    method: 'POST',
                    body: formData
                });

                const result = await response.json();

                hideLoadingModal();

                if (result.success) {
                    currentProjectId = result.project_id;

                    // Update preview
                    if (appPreview) appPreview.innerHTML = result.preview_html;
                    if (previewPanel) previewPanel.style.display = 'block';

                    // Show download panel
                    if (downloadBtn) downloadBtn.href = `/download_project/${currentProjectId}`;
                    if (downloadPanel) {
                        downloadPanel.style.display = 'block';
                        downloadPanel.scrollIntoView({ behavior: 'smooth' });
                    }

                    showGenerationStatus(result.message, 'success');
                } else {
                    showGenerationStatus(result.message, 'error');
                }
            } catch (error) {
                hideLoadingModal();
                showGenerationStatus('Error generating app: ' + error.message, 'error');
            }
        });
    }

    // Auto-update preview on prompt change (debounced)
    let previewTimeout;
    if (appPrompt) {
        appPrompt.addEventListener('input', function() {
            clearTimeout(previewTimeout);
            previewTimeout = setTimeout(() => {
                if (appPrompt.value.trim() && previewPanel && previewPanel.style.display !== 'none') {
                    if (updatePreviewBtn) updatePreviewBtn.click();
                }
            }, 2000);
        });
    }
});