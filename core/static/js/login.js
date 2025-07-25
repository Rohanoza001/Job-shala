// Login page functionality
document.addEventListener('DOMContentLoaded', function() {
    // Account type tab switching
    const jobSeekerTab = document.getElementById('job-seeker-tab');
    const employerTab = document.getElementById('employer-tab');
    const jobSeekerLogin = document.getElementById('job-seeker-login');
    const employerLogin = document.getElementById('employer-login');

    function switchToJobSeeker() {
        if (jobSeekerTab && employerTab && jobSeekerLogin && employerLogin) {
            jobSeekerTab.classList.add('active', 'border-primary', 'bg-primary', 'text-white');
            jobSeekerTab.classList.remove('border-gray-300', 'bg-white', 'text-gray-700');
            
            employerTab.classList.remove('active', 'border-primary', 'bg-primary', 'text-white');
            employerTab.classList.add('border-gray-300', 'bg-white', 'text-gray-700');
            
            jobSeekerLogin.classList.remove('hidden');
            employerLogin.classList.add('hidden');
        }
    }

    function switchToEmployer() {
        if (employerTab && jobSeekerTab && employerLogin && jobSeekerLogin) {
            employerTab.classList.add('active', 'border-primary', 'bg-primary', 'text-white');
            employerTab.classList.remove('border-gray-300', 'bg-white', 'text-gray-700');
            
            jobSeekerTab.classList.remove('active', 'border-primary', 'bg-primary', 'text-white');
            jobSeekerTab.classList.add('border-gray-300', 'bg-white', 'text-gray-700');
            
            employerLogin.classList.remove('hidden');
            jobSeekerLogin.classList.add('hidden');
        }
    }

    if (jobSeekerTab) {
        jobSeekerTab.addEventListener('click', switchToJobSeeker);
    }
    if (employerTab) {
        employerTab.addEventListener('click', switchToEmployer);
    }

    // Password toggle functionality
    const passwordToggles = document.querySelectorAll('.password-toggle');
    
    passwordToggles.forEach(toggle => {
        toggle.addEventListener('click', function() {
            const input = this.previousElementSibling;
            const icon = this.querySelector('svg');
            
            if (input.type === 'password') {
                input.type = 'text';
                icon.innerHTML = `
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.878 9.878L3 3m6.878 6.878L21 21"></path>
                `;
            } else {
                input.type = 'password';
                icon.innerHTML = `
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
                `;
            }
        });
    });

            // Forms will now submit normally to Django backend
        // No need for custom form submission handlers
}); 