// scripts.js
function greetUser() {
    alert('Hello! Welcome to our example website.');
}

// Add a simple animation trigger
document.addEventListener('DOMContentLoaded', function() {
    const header = document.querySelector('header h1');
    header.addEventListener('click', function() {
        header.style.animation = 'none';
        setTimeout(() => {
            header.style.animation = '';
        }, 10);
    });
});
