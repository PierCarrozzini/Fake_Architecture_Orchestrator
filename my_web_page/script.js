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

// Questo codice aggiunge un effetto di animazione alla barra di navigazione

window.addEventListener("scroll", function() {
  if (window.scrollY > 0) {
    document.querySelector("nav").style.backgroundColor = "#000";
  } else {
    document.querySelector("nav").style.backgroundColor = "transparent";
  }
});

document.querySelector("a").addEventListener("click", function() {
  window.open("https://github.com/PierCarrozzini/Fake_Architecture_Orchestrator");
});
