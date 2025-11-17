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
            alert(" Debes seleccionar una fecha.");
            e.preventDefault();
            return;
        }

        const horaInputs = document.querySelectorAll('input[name="hora"]');
        if (horaInputs.length === 0 || !horaSeleccionada) {
            alert(" Debes seleccionar una hora disponible.");
            e.preventDefault();
            return;
        }

        if (!motivo) {
            alert(" Debes ingresar un motivo para la cita.");
            e.preventDefault();
            return;
        }

        const partes = fecha.split("-");
        let fechaSeleccionadaDate;
        if (partes[0].length === 4) {
            fechaSeleccionadaDate = new Date(fecha);
        } else {
            const [dd, mm , yyyy] = partes;
            fechaSeleccionadaDate = new Date(`${yyyy}-${mm}-${dd}`);
        }
        const hoyDate = new Date();
        hoyDate.setHours(0, 0, 0, 0);
        fechaSeleccionadaDate.setHours(0, 0, 0, 0);

        if (fechaSeleccionadaDate < hoyDate) {
            alert(" La fecha seleccionada no puede ser anterior a hoy.");
            e.preventDefault();
            return;
        }
    });
});