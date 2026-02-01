// 🎮 PARTMART Cards - Интерактивность

// Drag & Drop загрузка файлов
document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.querySelector('input[type="file"]');
    const dropZone = document.getElementById('drop-zone');
    
    if (dropZone && fileInput) {
        // Prevent default drag behaviors
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, preventDefaults, false);
            document.body.addEventListener(eventName, preventDefaults, false);
        });
        
        // Highlight drop zone when item is dragged over it
        ['dragenter', 'dragover'].forEach(eventName => {
            dropZone.addEventListener(eventName, highlight, false);
        });
        
        ['dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, unhighlight, false);
        });
        
        // Handle dropped files
        dropZone.addEventListener('drop', handleDrop, false);
        
        // Click to upload
        dropZone.addEventListener('click', () => fileInput.click());
    }
    
    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }
    
    function highlight(e) {
        dropZone.classList.add('highlight');
    }
    
    function unhighlight(e) {
        dropZone.classList.remove('highlight');
    }
    
    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        
        if (files.length) {
            fileInput.files = files;
            handleFiles(files);
        }
    }
    
    function handleFiles(files) {
        ([...files]).forEach(previewFile);
    }
    
    function previewFile(file) {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onloadend = function() {
            const preview = document.getElementById('photo-preview');
            if (preview) {
                preview.src = reader.result;
                preview.style.display = 'block';
            }
        }
    }
});

// Live Preview обновление
function updatePreview() {
    // Можно добавить AJAX для live preview
    console.log('Превью обновлено');
}

// Preset loader
function loadPreset(presetId) {
    // Загрузка пресета через AJAX
    console.log(`Загрузка пресета ${presetId}`);
}

// Smooth scroll
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Auto-hide messages
setTimeout(() => {
    const messages = document.querySelectorAll('.alert');
    messages.forEach(msg => {
        msg.style.opacity = '0';
        msg.style.transform = 'translateX(400px)';
        setTimeout(() => msg.remove(), 300);
    });
}, 5000);
