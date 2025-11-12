const $ = (id) => document.getElementById(id);

const formId = "formPaciente";
const campos = {
    rut: "id_rut",
    nombre: "id_nombre",
    apellido: "id_apellido",
    email: "id_email",
    direccion: "id_direccion",
    telefono: "id_telefono",
    prevision: "id_prevision"
};

function setFieldState(fieldId, valid, message='') {
    const input = $(fieldId);
    const msgEl = $(`msg_${fieldId}`);
    if (!input) return;

    input.classList.toggle("is-invalid", !valid);
    input.classList.toggle("is-valid", valid);

    if (msgEl) {
        msgEl.textContent = message;
        msgEl.className = 'feedback-msg';
        if (!valid) msgEl.classList.add('error-msg');
        else if (message.length > 0) msgEl.classList.add('success-msg');
    }
}

// ---------------- Validaciones ----------------
function validarRut() {
    const v = $(campos.rut).value.trim();
    const ok = /^\d{7,8}-[\dkK]$/.test(v);
    setFieldState(campos.rut, ok, ok ? '✓ Correcto.' : 'RUT: formato XXXXXXXX-X.');
    return ok;
}

function validarNombre() {
    const v = $(campos.nombre).value.trim();
    const ok = v.length >= 3 && /^[A-Za-zÁÉÍÓÚáéíóúÑñ ]+$/.test(v);
    setFieldState(campos.nombre, ok, ok ? '✓ Correcto.' : 'Nombre: Solo letras, mínimo 3 caracteres.');
    return ok;
}

function validarApellido() {
    const v = $(campos.apellido).value.trim();
    const ok = v.length >= 3 && /^[A-Za-zÁÉÍÓÚáéíóúÑñ ]+$/.test(v);
    setFieldState(campos.apellido, ok, ok ? '✓ Correcto.' : 'Apellido: Solo letras, mínimo 3 caracteres.');
    return ok;
}

function validarEmail() {
    const v = $(campos.email).value.trim();
    const ok = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v);
    setFieldState(campos.email, ok, ok ? '✓ Correo válido.' : 'Ingrese un correo válido.');
    return ok;
}

function validarDireccion() {
    const v = $(campos.direccion).value.trim();
    const ok = v.length >= 5;
    setFieldState(campos.direccion, ok, ok ? '✓ Correcto.' : 'Dirección: mínimo 5 caracteres.');
    return ok;
}

function validarTelefono() {
    const v = $(campos.telefono).value.trim();
    const ok = /^[9]{1}[0-9]{8}$/.test(v);
    setFieldState(campos.telefono, ok, ok ? '✓ Correcto.' : 'Teléfono: 9 dígitos, comienza con 9.');
    return ok;
}

function validarPrevision() {
    const v = $(campos.prevision).value.trim();
    const ok = v.length >= 3;
    setFieldState(campos.prevision, ok, ok ? '✓ Correcto.' : 'Previsión: mínimo 3 caracteres.');
    return ok;
}

const validadores = [
    validarRut, validarNombre, validarApellido,
    validarEmail, validarDireccion, validarTelefono, validarPrevision
];

document.addEventListener('DOMContentLoaded', () => {
    const form = $(formId);
    if (!form) return;

    Object.values(campos).forEach(id => {
        const input = $(id);
        if (input) input.addEventListener('input', () => {
            switch(id) {
                case campos.rut: validarRut(); break;
                case campos.nombre: validarNombre(); break;
                case campos.apellido: validarApellido(); break;
                case campos.email: validarEmail(); break;
                case campos.direccion: validarDireccion(); break;
                case campos.telefono: validarTelefono(); break;
                case campos.prevision: validarPrevision(); break;
            }
        });
    });

    form.addEventListener('submit', (ev) => {
        let valido = true;
        validadores.forEach(fn => { if(!fn()) valido = false; });

        if (!valido) {
            ev.preventDefault();
            alert("Por favor, corrija los campos con error antes de continuar.");
            return;
        }

        if (!confirm("¿Desea guardar este paciente?")) {
            ev.preventDefault();
        }
    });
});
