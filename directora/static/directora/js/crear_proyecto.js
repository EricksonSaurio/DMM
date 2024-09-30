document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById('proyectoForm');
    form.addEventListener('input', function(event) {
        validateField(event.target);
    });

    function validateField(field) {
        let errorSpan = document.getElementById('error-' + field.name);
        if (!field.value.trim()) {
            showError(field, errorSpan, 'Este campo es obligatorio.');
        } else {
            if (field.name === 'nombre' && !/^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$/.test(field.value)) {
                showError(field, errorSpan, 'El nombre solo debe contener letras.');
            } else if (field.name === 'descripcion' && field.value.trim().length < 10) {
                showError(field, errorSpan, 'La descripción debe tener al menos 10 caracteres.');
            } else if (field.name === 'fechaInicio' || field.name === 'fechaFin') {
                validateDates();
            } else {
                clearError(field, errorSpan);
            }
        }
    }

    function validateDates() {
        const startDate = document.getElementById('fechaInicio').value;
        const endDate = document.getElementById('fechaFin').value;
        const errorSpanStart = document.getElementById('error-fechaInicio');
        const errorSpanEnd = document.getElementById('error-fechaFin');

        if (startDate && endDate && new Date(startDate) > new Date(endDate)) {
            showError(document.getElementById('fechaFin'), errorSpanEnd, 'La fecha de fin no puede ser anterior a la fecha de inicio.');
        } else {
            clearError(document.getElementById('fechaInicio'), errorSpanStart);
            clearError(document.getElementById('fechaFin'), errorSpanEnd);
        }
    }

    function showError(field, errorSpan, message) {
        field.classList.add('is-invalid');
        errorSpan.textContent = message;
        errorSpan.style.display = 'block';
    }

    function clearError(field, errorSpan) {
        field.classList.remove('is-invalid');
        errorSpan.textContent = '';
        errorSpan.style.display = 'none';
    }
});

