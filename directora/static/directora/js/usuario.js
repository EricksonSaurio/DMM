document.addEventListener('DOMContentLoaded', function() {
    const empleadoSelect = document.getElementById('id_empleado');
    const emailInput = document.getElementById('id_email');

    empleadoSelect.addEventListener('change', function() {
        const empleadoId = empleadoSelect.value;

        fetch(`/directora/get-email/${empleadoId}/`)  // Asegúrate de incluir 'directora' en la ruta
        .then(response => {
            if (!response.ok) {
                throw new Error('Respuesta de red no fue ok');
            }
            return response.json();
        })
        .then(data => {
            emailInput.value = data.correo;  // 'correo' debe ser la clave
        })
        .catch(error => {
            console.error('Error al cargar el correo:', error);
        });
    });
});

