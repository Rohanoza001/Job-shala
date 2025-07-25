// Employer Signup functionality
document.addEventListener('DOMContentLoaded', function() {
    // Multi-step form functionality
    let currentStep = 1;
    const totalSteps = 5;
    const progressBar = document.querySelector('.progress-bar-fill');
    const stepIndicators = document.querySelectorAll('.step-indicator');
    const nextBtn = document.getElementById('next-btn');
    const prevBtn = document.getElementById('prev-btn');
    const submitBtn = document.getElementById('submit-btn');

    function updateProgress() {
        const progress = (currentStep / totalSteps) * 100;
        if (progressBar) {
            progressBar.style.width = progress + '%';
        }
        
        stepIndicators.forEach((indicator, index) => {
            if (index + 1 <= currentStep) {
                indicator.classList.add('active');
            } else {
                indicator.classList.remove('active');
            }
        });
    }

    function showStep(step) {
        const steps = document.querySelectorAll('.form-step');
        steps.forEach((stepElement, index) => {
            if (index + 1 === step) {
                stepElement.classList.remove('hidden');
            } else {
                stepElement.classList.add('hidden');
            }
        });

        // Update button visibility
        if (prevBtn) {
            prevBtn.style.display = step === 1 ? 'none' : 'block';
        }
        if (nextBtn) {
            nextBtn.style.display = step === totalSteps ? 'none' : 'block';
        }
        if (submitBtn) {
            submitBtn.style.display = step === totalSteps ? 'block' : 'none';
        }

        updateProgress();
    }

    if (nextBtn) {
        nextBtn.addEventListener('click', function() {
            if (currentStep < totalSteps) {
                currentStep++;
                showStep(currentStep);
            }
        });
    }

    if (prevBtn) {
        prevBtn.addEventListener('click', function() {
            if (currentStep > 1) {
                currentStep--;
                showStep(currentStep);
            }
        });
    }

    // Logo upload functionality
    const logoUpload = document.getElementById('logo-upload');
    const logoPreview = document.getElementById('logo-preview');
    const removeLogoBtn = document.getElementById('remove-logo');

    if (logoUpload && logoPreview) {
        logoUpload.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    logoPreview.src = e.target.result;
                    logoPreview.classList.remove('hidden');
                    logoUpload.classList.add('hidden');
                };
                reader.readAsDataURL(file);
            }
        });

        // Drag and drop functionality
        logoUpload.addEventListener('dragover', function(e) {
            e.preventDefault();
            logoUpload.classList.add('border-primary');
        });

        logoUpload.addEventListener('dragleave', function(e) {
            e.preventDefault();
            logoUpload.classList.remove('border-primary');
        });

        logoUpload.addEventListener('drop', function(e) {
            e.preventDefault();
            logoUpload.classList.remove('border-primary');
            const file = e.dataTransfer.files[0];
            if (file) {
                logoUpload.files = e.dataTransfer.files;
                const reader = new FileReader();
                reader.onload = function(e) {
                    logoPreview.src = e.target.result;
                    logoPreview.classList.remove('hidden');
                    logoUpload.classList.add('hidden');
                };
                reader.readAsDataURL(file);
            }
        });
    }

    if (removeLogoBtn && logoPreview) {
        removeLogoBtn.addEventListener('click', function() {
            logoPreview.classList.add('hidden');
            logoUpload.classList.remove('hidden');
            logoUpload.value = '';
        });
    }

    // GST conditional display
    const gstYesRadio = document.getElementById('gst-yes');
    const gstNoRadio = document.getElementById('gst-no');
    const gstNumberField = document.getElementById('gst-number');

    function toggleGSTField() {
        if (gstYesRadio && gstNoRadio && gstNumberField) {
            if (gstYesRadio.checked) {
                gstNumberField.classList.remove('hidden');
            } else if (gstNoRadio.checked) {
                gstNumberField.classList.add('hidden');
            }
        }
    }

    if (gstYesRadio) {
        gstYesRadio.addEventListener('change', toggleGSTField);
    }
    if (gstNoRadio) {
        gstNoRadio.addEventListener('change', toggleGSTField);
    }

    // Form submission
    const form = document.getElementById('employer-signup-form');

    if (submitBtn) {
        submitBtn.addEventListener('click', function(e) {
            e.preventDefault();
            // Show the verification step
            currentStep = 5;
            showStep(currentStep);
        });
    }

    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            // Show the verification step
            currentStep = 5;
            showStep(currentStep);
        });
    }

    // Initialize the form
    showStep(1);
}); 