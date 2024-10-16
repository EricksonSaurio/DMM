document.addEventListener('DOMContentLoaded', function() {
    const messages = document.querySelectorAll('.django-message');
    
    if (messages.length > 0) {
        messages.forEach(function(message) {
            const messageType = message.dataset.tag;
            const messageText = message.textContent.trim();  // Asegúrate de eliminar espacios

            Swal.fire({
                icon: messageType === 'success' ? 'success' : 'error',
                title: messageText,
                showConfirmButton: true,  // Mostrar botón OK
                confirmButtonText: 'OK'
            }).then(function(result) {
                // Verificar si el SweetAlert fue confirmado
                if (result.isConfirmed) {
                    // Si es un mensaje de éxito, redirigimos a listar empleados
                    if (messageType === 'success') {
                        window.location.href = '/directora/menu_tareas/';  // Cambia la URL según corresponda
                    }
                }
            });
        });
    } 
});
