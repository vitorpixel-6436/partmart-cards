// 🎮 PARTMART Cards Generator - Interactive Features

// Smooth scroll behavior
document.documentElement.style.scrollBehavior = 'smooth';

// Add fade-in animation to elements on page load
document.addEventListener('DOMContentLoaded', () => {
    const elements = document.querySelectorAll('.glass-panel, .glass-card');
    
    elements.forEach((el, index) => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            el.style.transition = 'all 0.5s cubic-bezier(0.4, 0, 0.2, 1)';
            el.style.opacity = '1';
            el.style.transform = 'translateY(0)';
        }, index * 100);
    });
});

// Style selector radio button visual feedback
const styleOptions = document.querySelectorAll('.style-option');
styleOptions.forEach(option => {
    option.addEventListener('click', () => {
        styleOptions.forEach(opt => opt.classList.remove('selected'));
        option.classList.add('selected');
    });
});

// Form validation enhancement
const forms = document.querySelectorAll('form');
forms.forEach(form => {
    form.addEventListener('submit', (e) => {
        const submitBtn = form.querySelector('button[type="submit"]');
        if (submitBtn) {
            submitBtn.disabled = true;
            submitBtn.innerHTML = '⏳ Обработка...';
        }
    });
});

// Notification auto-hide
const messages = document.querySelectorAll('.glass-panel[class*="border"]');
messages.forEach(msg => {
    setTimeout(() => {
        msg.style.transition = 'all 0.5s ease';
        msg.style.opacity = '0';
        msg.style.transform = 'translateX(100%)';
        setTimeout(() => msg.remove(), 500);
    }, 5000);
});

// Image preview zoom
const images = document.querySelectorAll('img');
images.forEach(img => {
    img.addEventListener('click', () => {
        if (img.classList.contains('zoomed')) {
            img.classList.remove('zoomed');
            img.style.transform = 'scale(1)';
            img.style.cursor = 'zoom-in';
        } else {
            img.classList.add('zoomed');
            img.style.transform = 'scale(1.5)';
            img.style.cursor = 'zoom-out';
            img.style.transition = 'transform 0.3s ease';
        }
    });
});

// Add parallax effect to hero section
window.addEventListener('scroll', () => {
    const scrolled = window.pageYOffset;
    const parallaxElements = document.querySelectorAll('.glass-panel');
    
    parallaxElements.forEach((el, index) => {
        const speed = 0.05 * (index + 1);
        el.style.transform = `translateY(${scrolled * speed}px)`;
    });
});

console.log('👾 PARTMART Cards Generator loaded successfully!');
