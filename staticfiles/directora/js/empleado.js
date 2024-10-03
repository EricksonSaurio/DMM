// Función para validar campos
function validarCampo(campo, regex, mensajeError, idError) {
    const valor = campo.value.trim();
    const errorDiv = document.getElementById(idError);

    if (!regex.test(valor)) {
        campo.classList.add('error');
        campo.classList.remove('success');
        errorDiv.textContent = mensajeError;
    } else {
        campo.classList.remove('error');
        campo.classList.add('success');
        errorDiv.textContent = '';
    }
}
// Event listeners para la validación en tiempo real
document.addEventListener('DOMContentLoaded', function() {
    // Buscar los elementos generados por Django Forms
    const nombre = document.querySelector('#id_nombre');
    const apellido = document.querySelector('#id_apellido');
    const correo = document.querySelector('#id_correo');
    const telefono = document.querySelector('#id_telefono');
    const dpi = document.querySelector('#id_dpi');
    const departamento = document.querySelector('#id_departamento');
    const fechaContratacion = document.querySelector('#id_fecha_contratacion');

    // Reglas de validación
    const regexNombre = /^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$/;
    const regexCorreo = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
    const regexTelefono = /^\d+$/;
    const regexDpi = /^\d{13}$/;
    const regexDepartamento = /^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$/;

    // Validar el campo de nombre
    if (nombre) {
        nombre.addEventListener('input', function() {
            validarCampo(nombre, regexNombre, 'El nombre solo debe contener letras.', 'error-nombre');
        });
    }

    // Validar el campo de apellido
    if (apellido) {
        apellido.addEventListener('input', function() {
            validarCampo(apellido, regexNombre, 'El apellido solo debe contener letras.', 'error-apellido');
        });
    }

    // Validar el campo de correo
    if (correo) {
        correo.addEventListener('input', function() {
            validarCampo(correo, regexCorreo, 'El correo no es válido.', 'error-correo');
        });
    }

    // Validar el campo de teléfono
    if (telefono) {
        telefono.addEventListener('input', function() {
            validarCampo(telefono, regexTelefono, 'El teléfono solo debe contener números.', 'error-telefono');
        });
    }

    // Validar el campo de DPI
    if (dpi) {
        dpi.addEventListener('input', function() {
            validarCampo(dpi, regexDpi, 'El DPI debe contener exactamente 13 números.', 'error-dpi');
        });
    }

    // Validar el campo de departamento
    if (departamento) {
        departamento.addEventListener('input', function() {
            validarCampo(departamento, regexDepartamento, 'El departamento solo debe contener letras.', 'error-departamento');
        });
    }

    // Validar el campo de fecha de contratación (sin regex, solo asegurando que se selecciona una fecha)
    if (fechaContratacion) {
        fechaContratacion.addEventListener('input', function() {
            if (fechaContratacion.value === '') {
                fechaContratacion.classList.add('error');
                fechaContratacion.classList.remove('success');
                document.getElementById('error-fecha').textContent = 'Selecciona una fecha de contratación.';
            } else {
                fechaContratacion.classList.remove('error');
                fechaContratacion.classList.add('success');
                document.getElementById('error-fecha').textContent = '';
            }
        });
    }
});
