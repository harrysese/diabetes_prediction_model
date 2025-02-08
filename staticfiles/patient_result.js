document.addEventListener('DOMContentLoaded', () => {
    // Accordion functionality for recommendations
    document.querySelectorAll('.recommendation-card h4').forEach(header => {
        header.addEventListener('click', () => {
            header.parentElement.classList.toggle('expanded');
        });
    });
});