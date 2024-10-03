document.addEventListener('DOMContentLoaded', function() {
    const messages = document.querySelectorAll('.django-message');
    
    if (messages.length > 0) {
        messages.forEach(function(message) {
            const messageType = message.dataset.tag;
            const messageText = message.textContent.trim();  // Asegúrate de eliminar espacios

            Swal.fire({
                icon: messageType === 'success' ? 'success' : 'error',
                title: messageText,
                showConfirmButton: false,
                timer: 2000
            });
        });
    } 
});
