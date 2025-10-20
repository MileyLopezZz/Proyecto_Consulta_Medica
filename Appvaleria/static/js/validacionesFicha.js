const $ = (id) => document.getElementById(id);

// --- 1. Definiciones de Constantes y IDs ---
const formId = "formFicha";
const rutFieldId = 'id_rut_paciente'; 
const nombreFieldId = 'id_nombre_paciente';
const telefonoFieldId = 'id_telefono_paciente';
const direccionFieldId = 'id_direccion_paciente';
const tituloFieldId = 'id_titulo';
const notasFieldId = 'id_notas';
const horaFieldId = 'id_hora_ficha';

const btnBuscar = document.getElementById('btnBuscar');
const buscarPacienteUrl = btnBuscar ? btnBuscar.dataset.url : ''; 

// --- 2. Funciones de Utilidad y Feedback Visual ---

/**
 * Aplica clases de feedback visual (is-invalid/is-valid) y muestra el mensaje.
 */
function setFieldState(fieldId, valid, message = '') {
    const input = $(fieldId);
    const msgEl = $(`msg_${fieldId}`); 
    
    if (!input) return;

    // 1. Clases al input para color del borde
    input.classList.toggle("is-invalid", !valid);
    input.classList.toggle("is-valid", valid);

    // 2. Mensaje al div
    if (msgEl) {
        msgEl.textContent = message;
        msgEl.className = 'feedback-msg'; // Resetear clase base
        
        if (!valid) {
            msgEl.classList.add('error-msg');
        } else if (message.length > 0) {
             msgEl.classList.add('success-msg');
        }
    }
}

/** Limpia los campos de datos del paciente. */
function limpiarCamposPaciente() {
    $(nombreFieldId).value = '';
    $(telefonoFieldId).value = '';
    $(direccionFieldId).value = '';
}

// --- 3. Validaciones Específicas (AJUSTADAS) ---

/** Valida el RUT en formato XXXXXXXX-X (siempre con guion). */
function validarRutPaciente() {
    const v = $(rutFieldId).value.trim();
    const ok = /^\d{7,8}-[\dkK]$/.test(v); 
    const msg = ok ? 'Formato correcto. Presione Buscar.' : 'RUT: Debe estar en formato XXXXXXXX-X (con guion).';
    setFieldState(rutFieldId, ok, msg);
    return ok;
}

/** * Valida nombre: solo letras, MÍNIMO 3, máximo 20 caracteres, obligatorio.
 * AJUSTE: Mínimo de 3 caracteres.
 */
function validarNombrePaciente() {
    const v = $(nombreFieldId).value.trim();
    const ok = v.length >= 3 && v.length <= 20 && /^[A-Za-zÁÉÍÓÚáéíóúÑñ ]+$/.test(v); 
    const msg = ok ? '✓ Correcto.' : 'Nombre: Solo letras, debe tener entre 3 y 20 caracteres.';
    setFieldState(nombreFieldId, ok, msg);
    return ok;
}

/** Valida teléfono: exactamente 9 dígitos, empieza con 9, solo números. */
function validarTelefonoPaciente() {
    const v = $(telefonoFieldId).value.trim();
    const ok = /^[9]{1}[0-9]{8}$/.test(v);
    const msg = ok ? '✓ Correcto.' : 'Teléfono: Debe ser 9 dígitos, comenzando con 9.';
    setFieldState(telefonoFieldId, ok, msg);
    return ok;
}

/** * Valida dirección: letras y números, MINIMO 5, MAXIMO 25 caracteres, obligatorio.
 * AJUSTE: Mínimo de 5 caracteres.
 */
function validarDireccionPaciente() {
    const v = $(direccionFieldId).value.trim();
    const regex = /^[A-Za-z0-9\s,.\-º°#/]+$/;
    // Debe tener entre 5 y 25 caracteres y seguir el patrón
    const ok = v.length >= 5 && v.length <= 25 && regex.test(v); 
    const msg = ok ? '✓ Correcto.' : 'Dirección: Debe tener entre 5 y 25 caracteres. Permite letras, números y símbolos.';
    setFieldState(direccionFieldId, ok, msg);
    return ok;
}

/** Valida título: solo letras, MÍNIMO 3, máximo 25 caracteres, obligatorio. */
function validarTitulo() {
    const v = $(tituloFieldId).value.trim();
    const ok = v.length >= 3 && v.length <= 25 && /^[A-Za-zÁÉÍÓÚáéíóúÑñ ]+$/.test(v); 
    const msg = ok ? '✓ Correcto.' : 'Título: Solo letras, debe tener entre 3 y 25 caracteres.';
    setFieldState(tituloFieldId, ok, msg);
    return ok;
}

/** Valida notas: MÍNIMO 10 caracteres, obligatorio. */
function validarNotas() {
    const v = $(notasFieldId).value.trim();
    const ok = v.length >= 10;
    const msg = ok ? '✓ Correcto.' : 'Notas: El campo es obligatorio y debe tener al menos 10 caracteres.';
    setFieldState(notasFieldId, ok, msg);
    return ok;
}

/** Valida hora de ficha: obligatorio (no vacío). */
function validarHoraFicha() {
    const v = $(horaFieldId).value;
    const ok = v !== ""; 
    const msg = ok ? '✓ Correcto.' : 'Hora Ficha: Debe seleccionar una hora.';
    setFieldState(horaFieldId, ok, msg);
    return ok;
}

// --- 4. Lógica de Búsqueda de Paciente (AJAX) ---

if (btnBuscar) {
    btnBuscar.addEventListener('click', function() {
        const rutInput = $(rutFieldId);
        const rut = rutInput.value.trim();

        if (!validarRutPaciente()) {
            rutInput.focus();
            return;
        }
        
        limpiarCamposPaciente();

        fetch(`${buscarPacienteUrl}?rut=${rut}`)
            .then(response => {
                if (!response.ok) {
                    return response.json().then(data => Promise.reject(data.error || 'Rut no encontrado'));
                }
                return response.json();
            })
            .then(data => {
                const nombre = data.nombre || '';
                const apellido = data.apellido || '';
                const telefono = data.telefono || '';
                const direccion = data.direccion || '';

                if (nombre === '' && apellido === '') {
                     return Promise.reject('Rut no encontrado');
                }

                // Éxito: Llenar campos SIN ALERTAS
                $(nombreFieldId).value = `${nombre} ${apellido}`.trim(); 
                $(telefonoFieldId).value = telefono;
                $(direccionFieldId).value = direccion;
                
                setFieldState(rutFieldId, true, 'Paciente encontrado.');
            })
            .catch(error => {
                console.error('Error en la búsqueda:', error);
                limpiarCamposPaciente();
                
                setFieldState(rutFieldId, false, `❌ Rut no encontrado.`);
                $(rutFieldId).focus();
            });
    });
}

// --- 5. Manejo del Formulario Principal (Botón "Guardar Ficha") ---

const camposValidar = [
    { id: rutFieldId, fn: validarRutPaciente },
    { id: nombreFieldId, fn: validarNombrePaciente },
    { id: telefonoFieldId, fn: validarTelefonoPaciente },
    { id: direccionFieldId, fn: validarDireccionPaciente },
    { id: tituloFieldId, fn: validarTitulo },
    { id: notasFieldId, fn: validarNotas },
    { id: horaFieldId, fn: validarHoraFicha },
];

if ($(formId)) { 
    $(formId).addEventListener("submit", (ev) => {
        let formIsValid = true;
        let firstInvalidField = null;

        camposValidar.forEach(campo => {
            const isValid = campo.fn();
            
            if (!isValid) {
                formIsValid = false;
                if (!firstInvalidField) {
                    firstInvalidField = $(campo.id);
                }
            }
        });

        if (!formIsValid) {
            ev.preventDefault(); // Detiene el envío si hay errores
            if (firstInvalidField) firstInvalidField.focus(); 
            return;
        }
        
        if (!confirm("¿Está seguro de guardar esta Ficha Médica?")) {
            ev.preventDefault(); 
            return;
        }
    });
}

camposValidar.forEach(campo => {
    const inputElement = $(campo.id);
    if (inputElement) {
        const eventType = campo.id === horaFieldId ? 'change' : 'input';
        
        inputElement.addEventListener(eventType, () => {
            campo.fn(); 
        });
    }
});