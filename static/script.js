// Modern JavaScript for enhanced interactions

document.addEventListener('DOMContentLoaded', function() {
    // Add checked class to answer options and module options for better styling
    const checkboxes = document.querySelectorAll('input[type="checkbox"]');
    
    checkboxes.forEach(checkbox => {
        // Set initial state
        updateCheckboxState(checkbox);
        
        // Update on change
        checkbox.addEventListener('change', function() {
            updateCheckboxState(this);
        });
    });
    
    function updateCheckboxState(checkbox) {
        const parent = checkbox.closest('.answer-option, .module-option');
        if (parent) {
            if (checkbox.checked) {
                parent.classList.add('checked');
            } else {
                parent.classList.remove('checked');
            }
        }
    }
    
    // Add smooth scroll to top when navigating
    const links = document.querySelectorAll('a[href^="/"]');
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            // Only scroll if not already at top
            if (window.scrollY > 0) {
                window.scrollTo({ top: 0, behavior: 'smooth' });
            }
        });
    });
    
    // Add animation to progress bar on load
    const progressBars = document.querySelectorAll('.progress-bar-inner');
    progressBars.forEach(bar => {
        const width = bar.style.width || bar.getAttribute('style')?.match(/width:\s*(\d+)%/)?.[1];
        if (width) {
            bar.style.width = '0%';
            setTimeout(() => {
                bar.style.width = width + '%';
            }, 100);
        }
    });
});

