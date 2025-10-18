document.addEventListener("DOMContentLoaded", () => {
    const fechaInput = document.getElementById("fecha");
    const form = document.getElementById("form-agendar");

    // Bloquear días anteriores
    const hoy = new Date();
    const yyyy = hoy.getFullYear();
    const mm = String(hoy.getMonth() + 1).padStart(2, "0");
    const dd = String(hoy.getDate()).padStart(2, "0");
    const minDate = `${yyyy}-${mm}-${dd}`;
    fechaInput.min = minDate;

    // Validar antes de enviar
    form.addEventListener("submit", (e) => {
        const fecha = fechaInput.value;
        const horaSeleccionada = document.querySelector('input[name="hora"]:checked');
        const motivo = document.querySelector('textarea[name="motivo"]').value.trim();

        if (!fecha) {
            alert("⚠️ Debes seleccionar una fecha.");
            e.preventDefault();
            return;
        }

        if (!horaSeleccionada) {
            alert("⚠️ Debes seleccionar una hora disponible.");
            e.preventDefault();
            return;
        }

        if (!motivo) {
            alert("⚠️ Debes ingresar un motivo para la cita.");
            e.preventDefault();
            return;
        }

        // Bloquea fechas pasadas incluso si el navegador lo ignora
        const fechaSeleccionada = new Date(fecha);
        if (fechaSeleccionada < hoy.setHours(0, 0, 0, 0)) {
            alert("⚠️ No puedes seleccionar una fecha pasada.");
            e.preventDefault();
        }
    });
});
