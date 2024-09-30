// Alternar el modo oscuro
document.getElementById('dark-mode-toggle').addEventListener('click', function() {
    // Alternar el modo oscuro en el body
    document.body.classList.toggle('dark-mode');

    // Alternar el modo oscuro en el jumbotron
    var jumbotron = document.querySelector('.jumbotron');
    if (jumbotron) {
        jumbotron.classList.toggle('dark-mode');
    }

    // Alternar el modo oscuro en todas las tarjetas
    var cards = document.querySelectorAll('.card-body');
    cards.forEach(function(card) {
        card.classList.toggle('dark-mode');
    });

    // Guardar el estado del modo oscuro en localStorage
    if (document.body.classList.contains('dark-mode')) {
        localStorage.setItem('darkMode', 'enabled');
    } else {
        localStorage.setItem('darkMode', 'disabled');
    }
});

// Mantener el estado del modo oscuro entre sesiones
if (localStorage.getItem('darkMode') === 'enabled') {
    document.body.classList.add('dark-mode');
    var jumbotron = document.querySelector('.jumbotron');
    if (jumbotron) {
        jumbotron.classList.add('dark-mode');
    }
    var cards = document.querySelectorAll('.card-body');
    cards.forEach(function(card) {
        card.classList.add('dark-mode');
    });
}
