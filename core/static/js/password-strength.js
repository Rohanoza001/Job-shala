// Password Strength Indicator
function createPasswordStrengthIndicator(passwordFieldId) {
    const passwordField = document.getElementById(passwordFieldId);
    if (!passwordField) return;

    // Create strength indicator
    const strengthContainer = document.createElement('div');
    strengthContainer.className = 'password-strength mt-2';
    strengthContainer.innerHTML = `
        <div class="flex items-center space-x-2">
            <div class="flex-1 bg-gray-200 rounded-full h-2">
                <div class="password-strength-bar h-2 rounded-full transition-all duration-300" style="width: 0%"></div>
            </div>
            <span class="password-strength-text text-xs font-medium text-gray-500">Weak</span>
        </div>
        <div class="password-requirements mt-2 text-xs text-gray-500 space-y-1">
            <div class="requirement" data-requirement="length">
                <span class="requirement-icon">○</span> At least 8 characters
            </div>
            <div class="requirement" data-requirement="uppercase">
                <span class="requirement-icon">○</span> One uppercase letter
            </div>
            <div class="requirement" data-requirement="lowercase">
                <span class="requirement-icon">○</span> One lowercase letter
            </div>
            <div class="requirement" data-requirement="number">
                <span class="requirement-icon">○</span> One number
            </div>
            <div class="requirement" data-requirement="special">
                <span class="requirement-icon">○</span> One special character
            </div>
        </div>
    `;

    passwordField.parentNode.appendChild(strengthContainer);

    // Password strength checker
    function checkPasswordStrength(password) {
        const requirements = {
            length: password.length >= 8,
            uppercase: /[A-Z]/.test(password),
            lowercase: /[a-z]/.test(password),
            number: /\d/.test(password),
            special: /[@$!%*?&]/.test(password)
        };

        const metRequirements = Object.values(requirements).filter(Boolean).length;
        const strength = (metRequirements / 5) * 100;

        // Update strength bar
        const strengthBar = strengthContainer.querySelector('.password-strength-bar');
        const strengthText = strengthContainer.querySelector('.password-strength-text');

        strengthBar.style.width = `${strength}%`;

        if (strength <= 20) {
            strengthBar.className = 'password-strength-bar h-2 rounded-full transition-all duration-300 bg-red-500';
            strengthText.textContent = 'Very Weak';
            strengthText.className = 'password-strength-text text-xs font-medium text-red-500';
        } else if (strength <= 40) {
            strengthBar.className = 'password-strength-bar h-2 rounded-full transition-all duration-300 bg-orange-500';
            strengthText.textContent = 'Weak';
            strengthText.className = 'password-strength-text text-xs font-medium text-orange-500';
        } else if (strength <= 60) {
            strengthBar.className = 'password-strength-bar h-2 rounded-full transition-all duration-300 bg-yellow-500';
            strengthText.textContent = 'Fair';
            strengthText.className = 'password-strength-text text-xs font-medium text-yellow-600';
        } else if (strength <= 80) {
            strengthBar.className = 'password-strength-bar h-2 rounded-full transition-all duration-300 bg-blue-500';
            strengthText.textContent = 'Good';
            strengthText.className = 'password-strength-text text-xs font-medium text-blue-500';
        } else {
            strengthBar.className = 'password-strength-bar h-2 rounded-full transition-all duration-300 bg-green-500';
            strengthText.textContent = 'Strong';
            strengthText.className = 'password-strength-text text-xs font-medium text-green-500';
        }

        // Update requirements
        Object.keys(requirements).forEach(requirement => {
            const requirementElement = strengthContainer.querySelector(`[data-requirement="${requirement}"]`);
            const icon = requirementElement.querySelector('.requirement-icon');
            
            if (requirements[requirement]) {
                icon.textContent = '✓';
                icon.className = 'requirement-icon text-green-500';
                requirementElement.className = 'requirement text-green-600';
            } else {
                icon.textContent = '○';
                icon.className = 'requirement-icon text-gray-400';
                requirementElement.className = 'requirement text-gray-500';
            }
        });

        return { strength, requirements };
    }

    // Add event listener
    passwordField.addEventListener('input', function() {
        checkPasswordStrength(this.value);
    });

    return { checkPasswordStrength };
}

// Initialize password strength indicators
document.addEventListener('DOMContentLoaded', function() {
    // For job seeker signup
    if (document.getElementById('password')) {
        createPasswordStrengthIndicator('password');
    }
    
    // For employer signup
    if (document.getElementById('employer-password')) {
        createPasswordStrengthIndicator('employer-password');
    }
}); 