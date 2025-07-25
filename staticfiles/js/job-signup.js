// Job Seeker Signup functionality
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

    // Image upload functionality
    const imageUpload = document.getElementById('image-upload');
    const imagePreview = document.getElementById('image-preview');
    const removeImageBtn = document.getElementById('remove-image');

    if (imageUpload && imagePreview) {
        imageUpload.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    imagePreview.src = e.target.result;
                    imagePreview.classList.remove('hidden');
                    imageUpload.classList.add('hidden');
                };
                reader.readAsDataURL(file);
            }
        });

        // Drag and drop functionality
        imageUpload.addEventListener('dragover', function(e) {
            e.preventDefault();
            imageUpload.classList.add('border-primary');
        });

        imageUpload.addEventListener('dragleave', function(e) {
            e.preventDefault();
            imageUpload.classList.remove('border-primary');
        });

        imageUpload.addEventListener('drop', function(e) {
            e.preventDefault();
            imageUpload.classList.remove('border-primary');
            const file = e.dataTransfer.files[0];
            if (file) {
                imageUpload.files = e.dataTransfer.files;
                const reader = new FileReader();
                reader.onload = function(e) {
                    imagePreview.src = e.target.result;
                    imagePreview.classList.remove('hidden');
                    imageUpload.classList.add('hidden');
                };
                reader.readAsDataURL(file);
            }
        });
    }

    if (removeImageBtn && imagePreview) {
        removeImageBtn.addEventListener('click', function() {
            imagePreview.classList.add('hidden');
            imageUpload.classList.remove('hidden');
            imageUpload.value = '';
        });
    }

    // Dynamic dropdowns for Country, State, City
    const countrySelect = document.getElementById('country');
    const stateSelect = document.getElementById('state');
    const citySelect = document.getElementById('city');

    // Country-State mapping
    const countryStateMap = {
        'India': [
            'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh',
            'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jharkhand',
            'Karnataka', 'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur',
            'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Punjab',
            'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura',
            'Uttar Pradesh', 'Uttarakhand', 'West Bengal'
        ],
        'USA': ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California'],
        'Canada': ['Alberta', 'British Columbia', 'Manitoba', 'New Brunswick']
    };

    // State-City mapping
    const stateCityMap = {
        'Maharashtra': ['Mumbai', 'Pune', 'Nagpur', 'Thane', 'Nashik'],
        'Delhi': ['New Delhi', 'North Delhi', 'South Delhi', 'East Delhi', 'West Delhi'],
        'Karnataka': ['Bangalore', 'Mysore', 'Hubli', 'Mangalore', 'Belgaum'],
        'Tamil Nadu': ['Chennai', 'Coimbatore', 'Madurai', 'Salem', 'Vellore'],
        'Gujarat': ['Ahmedabad', 'Surat', 'Vadodara', 'Rajkot', 'Bhavnagar']
    };

    if (countrySelect && stateSelect) {
        countrySelect.addEventListener('change', function() {
            const selectedCountry = this.value;
            stateSelect.innerHTML = '<option value="">Select State</option>';
            
            if (countryStateMap[selectedCountry]) {
                countryStateMap[selectedCountry].forEach(state => {
                    const option = document.createElement('option');
                    option.value = state;
                    option.textContent = state;
                    stateSelect.appendChild(option);
                });
            }
        });
    }

    if (stateSelect && citySelect) {
        stateSelect.addEventListener('change', function() {
            const selectedState = this.value;
            citySelect.innerHTML = '<option value="">Select City</option>';
            
            if (stateCityMap[selectedState]) {
                stateCityMap[selectedState].forEach(city => {
                    const option = document.createElement('option');
                    option.value = city;
                    option.textContent = city;
                    citySelect.appendChild(option);
                });
            }
        });
    }

    // Dynamic form field addition/removal
    let experienceCounter = 1;
    let educationCounter = 1;
    let projectCounter = 1;

    // Experience section
    const addExperienceBtn = document.getElementById('add-experience');
    const experienceContainer = document.getElementById('experience-container');

    if (addExperienceBtn && experienceContainer) {
        addExperienceBtn.addEventListener('click', function() {
            experienceCounter++;
            const newExperience = document.createElement('div');
            newExperience.className = 'experience-section border border-gray-200 rounded-lg p-6 mb-4';
            newExperience.innerHTML = `
                <div class="flex justify-between items-center mb-4">
                    <h4 class="text-lg font-semibold text-gray-900">Work Experience ${experienceCounter}</h4>
                    <button type="button" class="remove-section text-red-500 hover:text-red-700">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                        </svg>
                    </button>
                </div>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Company Name</label>
                        <input type="text" name="company_${experienceCounter}" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent">
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Job Title</label>
                        <input type="text" name="job_title_${experienceCounter}" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent">
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Start Date</label>
                        <input type="date" name="start_date_${experienceCounter}" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent">
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">End Date</label>
                        <input type="date" name="end_date_${experienceCounter}" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent">
                    </div>
                    <div class="md:col-span-2">
                        <label class="block text-sm font-medium text-gray-700 mb-2">Description</label>
                        <textarea name="description_${experienceCounter}" rows="3" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"></textarea>
                    </div>
                </div>
            `;
            
            experienceContainer.appendChild(newExperience);
            
            // Add remove functionality
            const removeBtn = newExperience.querySelector('.remove-section');
            removeBtn.addEventListener('click', function() {
                newExperience.remove();
            });
        });
    }

    // Education section
    const addEducationBtn = document.getElementById('add-education');
    const educationContainer = document.getElementById('education-container');

    if (addEducationBtn && educationContainer) {
        addEducationBtn.addEventListener('click', function() {
            educationCounter++;
            const newEducation = document.createElement('div');
            newEducation.className = 'education-section border border-gray-200 rounded-lg p-6 mb-4';
            newEducation.innerHTML = `
                <div class="flex justify-between items-center mb-4">
                    <h4 class="text-lg font-semibold text-gray-900">Education ${educationCounter}</h4>
                    <button type="button" class="remove-section text-red-500 hover:text-red-700">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                        </svg>
                    </button>
                </div>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Institution</label>
                        <input type="text" name="institution_${educationCounter}" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent">
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Degree</label>
                        <input type="text" name="degree_${educationCounter}" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent">
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Field of Study</label>
                        <input type="text" name="field_${educationCounter}" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent">
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Graduation Year</label>
                        <input type="number" name="graduation_year_${educationCounter}" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent">
                    </div>
                    <div class="md:col-span-2">
                        <label class="block text-sm font-medium text-gray-700 mb-2">Description</label>
                        <textarea name="education_description_${educationCounter}" rows="3" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"></textarea>
                    </div>
                </div>
            `;
            
            educationContainer.appendChild(newEducation);
            
            // Add remove functionality
            const removeBtn = newEducation.querySelector('.remove-section');
            removeBtn.addEventListener('click', function() {
                newEducation.remove();
            });
        });
    }

    // Projects section
    const addProjectBtn = document.getElementById('add-project');
    const projectContainer = document.getElementById('project-container');

    if (addProjectBtn && projectContainer) {
        addProjectBtn.addEventListener('click', function() {
            projectCounter++;
            const newProject = document.createElement('div');
            newProject.className = 'project-section border border-gray-200 rounded-lg p-6 mb-4';
            newProject.innerHTML = `
                <div class="flex justify-between items-center mb-4">
                    <h4 class="text-lg font-semibold text-gray-900">Project ${projectCounter}</h4>
                    <button type="button" class="remove-section text-red-500 hover:text-red-700">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                        </svg>
                    </button>
                </div>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Project Name</label>
                        <input type="text" name="project_name_${projectCounter}" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent">
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Project URL</label>
                        <input type="url" name="project_url_${projectCounter}" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent">
                    </div>
                    <div class="md:col-span-2">
                        <label class="block text-sm font-medium text-gray-700 mb-2">Description</label>
                        <textarea name="project_description_${projectCounter}" rows="3" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"></textarea>
                    </div>
                </div>
            `;
            
            projectContainer.appendChild(newProject);
            
            // Add remove functionality
            const removeBtn = newProject.querySelector('.remove-section');
            removeBtn.addEventListener('click', function() {
                newProject.remove();
            });
        });
    }

    // Skills and Languages functionality
    const programmingLanguageSelect = document.getElementById('programming-language');
    const frameworksSelect = document.getElementById('frameworks');
    const databasesSelect = document.getElementById('databases');
    const otherSkillsSelect = document.getElementById('other-skills');
    const nativeLanguageSelect = document.getElementById('native-language');

    // Programming Language - Frameworks mapping
    const languageFrameworkMap = {
        'Python': ['Django', 'Flask', 'FastAPI', 'PyTorch', 'TensorFlow', 'Pandas', 'NumPy'],
        'JavaScript': ['React', 'Vue.js', 'Angular', 'Node.js', 'Express.js', 'Next.js'],
        'Java': ['Spring Boot', 'Hibernate', 'Maven', 'Gradle', 'JUnit', 'Android'],
        'C++': ['Qt', 'Boost', 'OpenCV', 'STL', 'CMake'],
        'PHP': ['Laravel', 'CodeIgniter', 'Symfony', 'WordPress', 'Drupal']
    };

    if (programmingLanguageSelect && frameworksSelect) {
        programmingLanguageSelect.addEventListener('change', function() {
            const selectedLanguage = this.value;
            frameworksSelect.innerHTML = '<option value="">Select Framework</option>';
            
            if (languageFrameworkMap[selectedLanguage]) {
                languageFrameworkMap[selectedLanguage].forEach(framework => {
                    const option = document.createElement('option');
                    option.value = framework;
                    option.textContent = framework;
                    frameworksSelect.appendChild(option);
                });
            }
        });
    }

    // Dynamic skill display functionality
    function addSkillDisplay(selectElement, displayContainer, skillType) {
        if (selectElement && displayContainer) {
            selectElement.addEventListener('change', function() {
                const selectedValue = this.value;
                if (selectedValue && selectedValue !== '') {
                    const skillTag = document.createElement('div');
                    skillTag.className = 'inline-flex items-center bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm mr-2 mb-2';
                    skillTag.innerHTML = `
                        ${selectedValue}
                        <button type="button" class="ml-2 text-blue-600 hover:text-blue-800 remove-skill" data-skill="${selectedValue}" data-type="${skillType}">
                            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                            </svg>
                        </button>
                    `;
                    displayContainer.appendChild(skillTag);
                    
                    // Reset select
                    this.value = '';
                    
                    // Add remove functionality
                    const removeBtn = skillTag.querySelector('.remove-skill');
                    removeBtn.addEventListener('click', function() {
                        skillTag.remove();
                    });
                }
            });
        }
    }

    // Initialize skill displays
    const programmingDisplay = document.getElementById('programming-display');
    const frameworksDisplay = document.getElementById('frameworks-display');
    const databasesDisplay = document.getElementById('databases-display');
    const otherSkillsDisplay = document.getElementById('other-skills-display');
    const nativeLanguageDisplay = document.getElementById('native-language-display');

    addSkillDisplay(programmingLanguageSelect, programmingDisplay, 'programming');
    addSkillDisplay(frameworksSelect, frameworksDisplay, 'frameworks');
    addSkillDisplay(databasesSelect, databasesDisplay, 'databases');
    addSkillDisplay(otherSkillsSelect, otherSkillsDisplay, 'other');
    addSkillDisplay(nativeLanguageSelect, nativeLanguageDisplay, 'native');

    // Initialize the form
    showStep(1);
}); 