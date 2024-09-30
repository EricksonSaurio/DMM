function eliminarProyecto(proyectoId) {
    Swal.fire({
        title: '¿Estás seguro?',
        text: "¡No podrás revertir esto!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#d33',
        cancelButtonColor: '#3085d6',
        confirmButtonText: 'Sí, eliminarlo'
    }).then((result) => {
        if (result.isConfirmed) {
            // Aquí llamas a tu lógica backend para eliminar el proyecto
            window.location.href = '/eliminar-proyecto/' + proyectoId;
        }
    })
}