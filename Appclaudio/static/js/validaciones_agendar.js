document.addEventListener("DOMContentLoaded", () => {
    const fechaInput = document.getElementById("id_fecha") || document.getElementById("fecha");
    const form = document.getElementById("form-agendar");
    const inputHora = document.getElementById("id_hora_inicio"); // campo del form Django
    const motivoInput = document.getElementById("id_razon") || document.querySelector('textarea[name="motivo"]');

    if (!fechaInput || !form) return;

    // Bloquear días anteriores 
    const hoy = new Date();
    const yyyy = hoy.getFullYear();
    const mm = String(hoy.getMonth() + 1).padStart(2, "0");
    const dd = String(hoy.getDate()).padStart(2, "0");
    const minDate = `${yyyy}-${mm}-${dd}`;
    fechaInput.min = minDate;

    // Validar antes de enviar 
    form.addEventListener("submit", (e) => {
        const fecha = fechaInput.value.trim();
        const horaSeleccionada = inputHora ? inputHora.value.trim() : "";
        const motivo = motivoInput ? motivoInput.value.trim() : "";

        if (!fecha) {
            alert(" Debes seleccionar una fecha.");
            e.preventDefault();
            return;
        }

        if (!horaSeleccionada) {
            alert(" Debes seleccionar una hora disponible.");
            e.preventDefault();
            return;
        }

        if (!motivo) {
            alert(" Debes ingresar un motivo para la cita.");
            e.preventDefault();
            return;
        }

        //Bloquea fechas pasadas incluso si el navegador lo ignora 
        const fechaSeleccionada = new Date(fecha);
        const hoySinHora = new Date();
        hoySinHora.setHours(0, 0, 0, 0);

        if (fechaSeleccionada < hoySinHora) {
            alert(" No puedes seleccionar una fecha pasada.");
            e.preventDefault();
        }
    });
});
