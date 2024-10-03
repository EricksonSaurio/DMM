document.addEventListener('DOMContentLoaded', function() {
    // Obtener el contenedor con los datos de éxito y error
    const container = document.querySelector('.container');

    // Leer el valor del éxito
    const isSuccess = container.getAttribute('data-success') === 'true';

    // Leer el mensaje de error
    const errorMessage = container.getAttribute('data-error-message');

    // Mostrar la alerta de éxito si es necesario
    if (isSuccess) {
        Swal.fire({
            icon: 'success',
            title: 'Bienvenido',
            text: 'Inicio de sesión exitoso.',
        });
    }

    // Mostrar la alerta de error si es necesario
    if (errorMessage) {
        Swal.fire({
            icon: 'error',
            title: 'Oops...',
            text: errorMessage,
        });
    }

    // Funcionalidad para mostrar/ocultar la contraseña
    const mostrarPasswordCheckbox = document.querySelector('#mostrarPassword');
    const passwordField = document.querySelector('#password');
    mostrarPasswordCheckbox.addEventListener('change', function () {
        if (this.checked) {
            passwordField.setAttribute('type', 'text');
        } else {
            passwordField.setAttribute('type', 'password');
        }
    });
});
