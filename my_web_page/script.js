document.addEventListener('DOMContentLoaded', function () {
    fadeInElement('introduction', 2000);
});

document.addEventListener('DOMContentLoaded', function () {
    fadeInElement('features', 3500);
});

document.addEventListener('DOMContentLoaded', function () {
    fadeInElement('contact', 5000);
});

function fadeInElement(elementId, duration) {
    const element = document.getElementById(elementId);

    if (element) {
        let opacity = 0;
        const start = performance.now();

        function animate(currentTime) {
            const elapsed = currentTime - start;
            opacity = elapsed / duration;

            if (opacity <= 1) {
                element.style.opacity = opacity;
                requestAnimationFrame(animate);
            }
        }

        requestAnimationFrame(animate);
    }
}

// Smooth Scroll
document.querySelectorAll('nav a').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();

        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// Parallax Effect
window.addEventListener('scroll', function () {
    let scrollPosition = window.scrollY;

    // Parallax effect on header background
    document.querySelector('header').style.backgroundPositionY = `${scrollPosition * 0.5}px`;
});

// Responsive Footer
window.addEventListener('resize', function () {
    if (window.innerWidth < 768) {
        document.querySelector('footer p').innerHTML = '&copy; 2023 Cybersecurity Summit.';
    } else {
        document.querySelector('footer p').innerHTML = '&copy; 2023 Cybersecurity Summit. All rights reserved.';
    }
});

// Basic Animation
document.addEventListener('DOMContentLoaded', function () {
    const title = document.querySelector('h1');
    title.style.opacity = '0';

    setTimeout(() => {
        title.style.transition = 'opacity 1s ease-in-out';
        title.style.opacity = '1';
    }, 500);
});
