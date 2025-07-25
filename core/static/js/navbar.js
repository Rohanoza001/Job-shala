// Navbar functionality
document.addEventListener('DOMContentLoaded', function() {
    console.log('Navbar.js loaded successfully');
    
    // Mobile menu functionality
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');
    const mobileSignupBtn = document.getElementById('signup-btn-mobile');
    const desktopSignupBtn = document.getElementById('signup-btn-desktop');
    
    console.log('Elements found:', {
        mobileMenuButton: !!mobileMenuButton,
        mobileMenu: !!mobileMenu,
        mobileSignupBtn: !!mobileSignupBtn,
        desktopSignupBtn: !!desktopSignupBtn
    });

    // Toggle mobile menu
    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', function() {
            mobileMenu.classList.toggle('open');
        });
    }

    // Close mobile menu when clicking outside
    document.addEventListener('click', function(event) {
        if (mobileMenu && mobileMenu.classList.contains('open')) {
            if (!mobileMenu.contains(event.target) && !mobileMenuButton.contains(event.target)) {
                mobileMenu.classList.remove('open');
            }
        }
    });

    // Signup modal functionality
    const modal = document.getElementById('signup-modal');
    const modalContent = document.querySelector('.modal-content');
    const closeModalBtn = document.getElementById('close-modal');
    
    console.log('Modal elements found:', {
        modal: !!modal,
        modalContent: !!modalContent,
        closeModalBtn: !!closeModalBtn
    });

    function openModal() {
        console.log('openModal function called');
        if (modal) {
            modal.classList.add('open');
            document.body.style.overflow = 'hidden';
            console.log('Modal opened successfully');
        } else {
            console.log('Modal element not found');
        }
    }

    function closeModal() {
        if (modal) {
            modal.classList.remove('open');
            document.body.style.overflow = 'auto';
        }
    }

    // Open modal event listeners
    if (desktopSignupBtn) {
        desktopSignupBtn.addEventListener('click', function(e) {
            console.log('Desktop signup button clicked');
            openModal();
        });
    } else {
        console.log('Desktop signup button not found');
    }
    if (mobileSignupBtn) {
        mobileSignupBtn.addEventListener('click', function(e) {
            console.log('Mobile signup button clicked');
            openModal();
        });
    } else {
        console.log('Mobile signup button not found');
    }

    // Close modal event listeners
    if (closeModalBtn) {
        closeModalBtn.addEventListener('click', closeModal);
    }

    // Close modal when clicking outside
    if (modal) {
        modal.addEventListener('click', function(event) {
            if (event.target === modal) {
                closeModal();
            }
        });
    }

    // Close modal with Escape key
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape' && modal && modal.classList.contains('open')) {
            closeModal();
        }
    });

    // Job seeker and employer button functionality
    const jobSeekerBtn = document.getElementById('job-seeker-btn');
    const employerBtn = document.getElementById('employer-btn');

    if (jobSeekerBtn) {
        jobSeekerBtn.addEventListener('click', function() {
            // Redirect to job seeker signup page
            window.location.href = '/job/signup/';
            closeModal();
        });
    }

    if (employerBtn) {
        employerBtn.addEventListener('click', function() {
            // Redirect to employer signup page
            window.location.href = '/employer/signup/';
            closeModal();
        });
    }

    // User menu modal functionality
    const userMenuModal = document.getElementById('user-menu-modal');
    const userMenuBtnDesktop = document.getElementById('user-menu-btn-desktop');
    const userMenuBtnMobile = document.getElementById('user-menu-btn-mobile');
    const closeUserMenuBtn = document.getElementById('close-user-menu');
    
    console.log('User menu elements found:', {
        userMenuModal: !!userMenuModal,
        userMenuBtnDesktop: !!userMenuBtnDesktop,
        userMenuBtnMobile: !!userMenuBtnMobile,
        closeUserMenuBtn: !!closeUserMenuBtn
    });

    function openUserMenu() {
        console.log('openUserMenu function called');
        if (userMenuModal) {
            userMenuModal.classList.add('open');
            document.body.style.overflow = 'hidden';
            console.log('User menu opened successfully');
        } else {
            console.log('User menu modal element not found');
        }
    }

    function closeUserMenu() {
        if (userMenuModal) {
            userMenuModal.classList.remove('open');
            document.body.style.overflow = 'auto';
        }
    }

    // Open user menu event listeners
    if (userMenuBtnDesktop) {
        userMenuBtnDesktop.addEventListener('click', function(e) {
            console.log('Desktop user menu button clicked');
            openUserMenu();
        });
    } else {
        console.log('Desktop user menu button not found');
    }
    
    if (userMenuBtnMobile) {
        userMenuBtnMobile.addEventListener('click', function(e) {
            console.log('Mobile user menu button clicked');
            openUserMenu();
        });
    } else {
        console.log('Mobile user menu button not found');
    }

    // Close user menu event listeners
    if (closeUserMenuBtn) {
        closeUserMenuBtn.addEventListener('click', closeUserMenu);
    }

    // Close user menu when clicking outside
    if (userMenuModal) {
        userMenuModal.addEventListener('click', function(event) {
            if (event.target === userMenuModal) {
                closeUserMenu();
            }
        });
    }

    // Close user menu with Escape key
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape' && userMenuModal && userMenuModal.classList.contains('open')) {
            closeUserMenu();
        }
    });

    // Navbar scroll effect
    const navbar = document.querySelector('nav');
    let lastScrollTop = 0;

    window.addEventListener('scroll', function() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        if (scrollTop > lastScrollTop && scrollTop > 100) {
            // Scrolling down
            navbar.style.transform = 'translateY(-100%)';
        } else {
            // Scrolling up
            navbar.style.transform = 'translateY(0)';
        }
        
        lastScrollTop = scrollTop;
    });
}); 