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
        const statusDiv = document.getElementById('apiStatus');
        if (statusDiv) {
            const alertClass = type === 'success' ? 'alert-success' : 'alert-danger';
            statusDiv.innerHTML = `
                <div class="alert ${alertClass} alert-dismissible fade show" role="alert">
                    ${message}
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>
            `;
            
            // Check for rate limit messages and show popup
            if (message.toLowerCase().includes('rate limit') || 
                message.toLowerCase().includes('quota') || 
                message.toLowerCase().includes('limit exceeded')) {
                showRateLimitPopup(message);
            }
        }
    }

    function showGenerationStatus(message, type) {
        const statusDiv = document.getElementById('generationStatus');
        if (statusDiv) {
            const alertClass = type === 'success' ? 'alert-success' : 
                              type === 'error' ? 'alert-danger' : 'alert-info';
            statusDiv.innerHTML = `
                <div class="alert ${alertClass} alert-dismissible fade show" role="alert">
                    ${message}
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>
            `;
            
            // Check for rate limit messages and show popup
            if (message.toLowerCase().includes('rate limit') || 
                message.toLowerCase().includes('quota') || 
                message.toLowerCase().includes('limit exceeded')) {
                showRateLimitPopup(message);
            }
        }
    }

    

    function hideLoadingModal() {
        if (loadingModal) loadingModal.hide();
    }

    function showRateLimitPopup(message) {
        // Create rate limit popup modal
        let popup = document.getElementById('rateLimitPopup');
        if (!popup) {
            popup = document.createElement('div');
            popup.id = 'rateLimitPopup';
            popup.className = 'modal fade';
            popup.innerHTML = `
                <div class="modal-dialog modal-dialog-centered">
                    <div class="modal-content">
                        <div class="modal-header bg-warning text-dark">
                            <h5 class="modal-title">
                                <i class="fas fa-exclamation-triangle me-2"></i>
                                API Rate Limit Reached
                            </h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                            <div class="alert alert-warning mb-3">
                                <strong>Gemini API Limit:</strong> You've reached the free tier quota limit.
                            </div>
                            <p><strong>What this means:</strong></p>
                            <ul>
                                <li>Your free API requests have been exhausted</li>
                                <li>The app will use fallback functionality</li>
                                <li>Generated apps will have basic structure only</li>
                            </ul>
                            <p><strong>Solutions:</strong></p>
                            <ul>
                                <li>Wait for quota reset (usually 24 hours)</li>
                                <li>Upgrade to a paid Gemini API plan</li>
                                <li>Try simpler app descriptions</li>
                            </ul>
                            <div class="mt-3">
                                <small class="text-muted">Error details: ${message}</small>
                            </div>
                        </div>
                        <div class="modal-footer">
                            <a href="https://ai.google.dev/pricing" target="_blank" class="btn btn-primary">
                                <i class="fas fa-external-link-alt me-1"></i>
                                View Gemini Pricing
                            </a>
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        </div>
                    </div>
                </div>
            `;
            document.body.appendChild(popup);
        }
        
        const bsModal = new bootstrap.Modal(popup);
        bsModal.show();
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

    

    function showLoadingModal(title, message) {
        // Create or show loading modal
        let modal = document.getElementById('loadingModal');
        if (!modal) {
            modal = document.createElement('div');
            modal.id = 'loadingModal';
            modal.className = 'modal fade';
            modal.innerHTML = `
                <div class="modal-dialog modal-dialog-centered">
                    <div class="modal-content">
                        <div class="modal-body text-center">
                            <div class="spinner-border mb-3" role="status">
                                <span class="visually-hidden">Loading...</span>
                            </div>
                            <h5 id="loadingTitle">${title}</h5>
                            <p id="loadingMessage">${message}</p>
                        </div>
                    </div>
                </div>
            `;
            document.body.appendChild(modal);
        } else {
            const titleElement = document.getElementById('loadingTitle');
            const messageElement = document.getElementById('loadingMessage');
            if (titleElement) titleElement.textContent = title;
            if (messageElement) messageElement.textContent = message;
        }
        
        const bsModal = new bootstrap.Modal(modal);
        bsModal.show();
    }

    function hideLoadingModal() {
        const modal = document.getElementById('loadingModal');
        if (modal) {
            const bsModal = bootstrap.Modal.getInstance(modal);
            if (bsModal) {
                bsModal.hide();
            }
        }
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
                    showGenerationStatus('Image uploaded successfully', 'success');
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