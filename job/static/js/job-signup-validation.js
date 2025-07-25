// Job Seeker Signup Form Validation
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('job-seeker-signup-form');
    const steps = document.querySelectorAll('.step');
    const nextButtons = document.querySelectorAll('.next-step');
    const prevButtons = document.querySelectorAll('.prev-step');
    const submitBtn = document.getElementById('submit-btn');

    // Validation rules
    const validationRules = {
        'first-name': {
            required: true,
            minLength: 2,
            maxLength: 50,
            pattern: /^[a-zA-Z\s]+$/,
            message: 'First name must be 2-50 characters and contain only letters'
        },
        'last-name': {
            required: true,
            minLength: 2,
            maxLength: 50,
            pattern: /^[a-zA-Z\s]+$/,
            message: 'Last name must be 2-50 characters and contain only letters'
        },
        'email': {
            required: true,
            pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
            message: 'Please enter a valid email address'
        },
        'phone': {
            required: true,
            pattern: /^[0-9+\-\s()]{10,15}$/,
            message: 'Please enter a valid phone number (10-15 digits)'
        },
        'address': {
            required: true,
            minLength: 10,
            maxLength: 500,
            message: 'Address must be 10-500 characters'
        },
        'city': {
            required: true,
            minLength: 2,
            maxLength: 100,
            pattern: /^[a-zA-Z\s]+$/,
            message: 'City must be 2-100 characters and contain only letters'
        },
        'state': {
            required: true,
            message: 'Please select a state'
        },
        'country': {
            required: true,
            message: 'Please select a country'
        },
        'pincode': {
            required: true,
            pattern: /^[0-9]{6}$/,
            message: 'Pincode must be exactly 6 digits'
        },
        'password': {
            required: true,
            minLength: 8,
            pattern: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]/,
            message: 'Password must be at least 8 characters with uppercase, lowercase, number, and special character'
        },
        'confirm-password': {
            required: true,
            message: 'Please confirm your password'
        },
        'description': {
            required: false,
            maxLength: 1000,
            message: 'Description must be no more than 1000 characters'
        }
    };

    // Validation functions
    function validateField(fieldName, value) {
        const rules = validationRules[fieldName];
        if (!rules) return { isValid: true, message: '' };

        // Required check
        if (rules.required && (!value || value.trim() === '')) {
            return { isValid: false, message: `${getFieldLabel(fieldName)} is required` };
        }

        // Skip other validations if not required and empty
        if (!rules.required && (!value || value.trim() === '')) {
            return { isValid: true, message: '' };
        }

        // Min length check
        if (rules.minLength && value.length < rules.minLength) {
            return { isValid: false, message: `${getFieldLabel(fieldName)} must be at least ${rules.minLength} characters` };
        }

        // Max length check
        if (rules.maxLength && value.length > rules.maxLength) {
            return { isValid: false, message: `${getFieldLabel(fieldName)} must be no more than ${rules.maxLength} characters` };
        }

        // Pattern check
        if (rules.pattern && !rules.pattern.test(value)) {
            return { isValid: false, message: rules.message };
        }

        // Password confirmation check
        if (fieldName === 'confirm-password') {
            const password = document.getElementById('password').value;
            if (value !== password) {
                return { isValid: false, message: 'Passwords do not match' };
            }
        }

        return { isValid: true, message: '' };
    }

    function getFieldLabel(fieldName) {
        const labels = {
            'first-name': 'First Name',
            'last-name': 'Last Name',
            'email': 'Email Address',
            'phone': 'Phone Number',
            'address': 'Address',
            'city': 'City',
            'state': 'State',
            'country': 'Country',
            'pincode': 'Pincode',
            'password': 'Password',
            'confirm-password': 'Confirm Password',
            'description': 'Description'
        };
        return labels[fieldName] || fieldName;
    }

    function showFieldError(fieldId, message) {
        const field = document.getElementById(fieldId);
        const errorDiv = document.getElementById(`${fieldId}-error`) || createErrorElement(fieldId);
        
        field.classList.add('border-red-500', 'focus:border-red-500', 'focus:ring-red-500');
        field.classList.remove('border-gray-300', 'focus:border-primary', 'focus:ring-primary');
        errorDiv.textContent = message;
        errorDiv.classList.remove('hidden');
    }

    function clearFieldError(fieldId) {
        const field = document.getElementById(fieldId);
        const errorDiv = document.getElementById(`${fieldId}-error`);
        
        field.classList.remove('border-red-500', 'focus:border-red-500', 'focus:ring-red-500');
        field.classList.add('border-gray-300', 'focus:border-primary', 'focus:ring-primary');
        if (errorDiv) {
            errorDiv.classList.add('hidden');
        }
    }

    function createErrorElement(fieldId) {
        const field = document.getElementById(fieldId);
        const errorDiv = document.createElement('div');
        errorDiv.id = `${fieldId}-error`;
        errorDiv.className = 'text-red-600 text-sm mt-1 hidden';
        field.parentNode.appendChild(errorDiv);
        return errorDiv;
    }

    // Real-time validation
    function setupFieldValidation(fieldId) {
        const field = document.getElementById(fieldId);
        if (!field) return;

        field.addEventListener('blur', function() {
            const validation = validateField(fieldId, this.value);
            if (!validation.isValid) {
                showFieldError(fieldId, validation.message);
            } else {
                clearFieldError(fieldId);
            }
        });

        field.addEventListener('input', function() {
            const validation = validateField(fieldId, this.value);
            if (validation.isValid) {
                clearFieldError(fieldId);
            }
        });
    }

    // Setup validation for all fields
    Object.keys(validationRules).forEach(setupFieldValidation);

    // Step validation
    function validateStep(stepNumber) {
        const currentStep = document.getElementById(`step-${stepNumber}`);
        const fields = currentStep.querySelectorAll('input, select, textarea');
        let isValid = true;
        const errors = [];

        fields.forEach(field => {
            const fieldId = field.id;
            if (validationRules[fieldId]) {
                const validation = validateField(fieldId, field.value);
                if (!validation.isValid) {
                    showFieldError(fieldId, validation.message);
                    isValid = false;
                    errors.push(validation.message);
                } else {
                    clearFieldError(fieldId);
                }
            }
        });

        return { isValid, errors };
    }

    // Next button click handler
    nextButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const currentStep = this.closest('.step');
            const currentStepNumber = parseInt(currentStep.id.split('-')[1]);
            
            const validation = validateStep(currentStepNumber);
            if (!validation.isValid) {
                // Show error message
                showStepError(currentStep, validation.errors[0]);
                return;
            }

            // Move to next step
            currentStep.classList.remove('active');
            const nextStep = document.getElementById(`step-${currentStepNumber + 1}`);
            nextStep.classList.add('active');
            
            // Update progress
            updateProgress(currentStepNumber + 1);
        });
    });

    // Previous button click handler
    prevButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const currentStep = this.closest('.step');
            const currentStepNumber = parseInt(currentStep.id.split('-')[1]);
            
            currentStep.classList.remove('active');
            const prevStep = document.getElementById(`step-${currentStepNumber - 1}`);
            prevStep.classList.add('active');
            
            updateProgress(currentStepNumber - 1);
        });
    });

    // Submit button handler
    if (submitBtn) {
        submitBtn.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Validate all steps
            let allValid = true;
            const allErrors = [];
            
            for (let i = 1; i <= 5; i++) {
                const validation = validateStep(i);
                if (!validation.isValid) {
                    allValid = false;
                    allErrors.push(...validation.errors);
                }
            }

            if (!allValid) {
                // Show first error
                showGlobalError(allErrors[0]);
                return;
            }

            // Show success message or redirect
            showSuccessMessage();
        });
    }

    function showStepError(step, message) {
        let errorDiv = step.querySelector('.step-error');
        if (!errorDiv) {
            errorDiv = document.createElement('div');
            errorDiv.className = 'step-error bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-md mb-4';
            step.insertBefore(errorDiv, step.firstChild);
        }
        errorDiv.textContent = message;
        errorDiv.classList.remove('hidden');
    }

    function showGlobalError(message) {
        let errorDiv = document.querySelector('.global-error');
        if (!errorDiv) {
            errorDiv = document.createElement('div');
            errorDiv.className = 'global-error bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-md mb-4';
            form.insertBefore(errorDiv, form.firstChild);
        }
        errorDiv.textContent = message;
        errorDiv.classList.remove('hidden');
    }

    function showSuccessMessage() {
        // Hide all steps
        steps.forEach(step => step.classList.remove('active'));
        
        // Show success step
        const successStep = document.getElementById('step-5');
        successStep.classList.add('active');
        
        // Update progress
        updateProgress(5);
    }

    function updateProgress(activeStep) {
        const progressSteps = document.querySelectorAll('.flex.items-center.min-w-fit');
        progressSteps.forEach((step, index) => {
            const stepNumber = index + 1;
            const circle = step.querySelector('div');
            const text = step.querySelector('span');
            
            if (stepNumber <= activeStep) {
                circle.classList.remove('bg-gray-200', 'text-gray-500');
                circle.classList.add('bg-primary', 'text-white');
                text.classList.remove('text-gray-500');
                text.classList.add('text-primary');
            } else {
                circle.classList.remove('bg-primary', 'text-white');
                circle.classList.add('bg-gray-200', 'text-gray-500');
                text.classList.remove('text-primary');
                text.classList.add('text-gray-500');
            }
        });
    }

    // Initialize progress
    updateProgress(1);
}); 