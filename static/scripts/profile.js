document.addEventListener('DOMContentLoaded', function() {
    const toggleSections = document.querySelectorAll('.toggle-section');

    toggleSections.forEach(section => {
        section.addEventListener('click', function() {
            const targetBlock = document.querySelector(this.dataset.target);
            const arrow = this.querySelector('.arrow');

            if (targetBlock.style.display === 'none' || targetBlock.style.display === '') {
                targetBlock.style.display = 'block';
                arrow.style.transform = 'rotate(180deg)';
            } else {
                targetBlock.style.display = 'none';
                arrow.style.transform = 'rotate(0deg)';
            }
        });
    });
});