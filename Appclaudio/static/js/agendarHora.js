// static/js/agendarHora.js
document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector("form");
    const fechaInput = document.getElementById("fecha");
    const horaRadios = document.querySelectorAll("input[name='hora']");
    const razonInput = document.getElementById("razon");
    const submitBtn = form.querySelector("button[type='submit']");

    form.addEventListener("submit", function(event) {
        let valid = true;
        let mensajes = [];

        // Validar fecha seleccionada
        const fechaSeleccionada = new Date(fechaInput.value);
        const hoy = new Date();
        hoy.setHours(0, 0, 0, 0);

        if (!fechaInput.value) {
            valid = false;
            mensajes.push("Debe seleccionar una fecha.");
        } else if (fechaSeleccionada < hoy) {
            valid = false;
            mensajes.push("No puede agendar una cita en una fecha pasada.");
        }

        // Validar horario seleccionado
        const horarioSeleccionado = Array.from(horaRadios).some(r => r.checked);
        if (!horarioSeleccionado) {
            valid = false;
            mensajes.push("Debe seleccionar un horario disponible.");
        }

        // Validar motivo (si el campo existe)
        if (razonInput && razonInput.value.trim().length === 0) {
            valid = false;
            mensajes.push("Por favor indique el motivo de la cita.");
        }

        // Si hay errores
        if (!valid) {
            event.preventDefault();
            alert(mensajes.join("\n"));
            return;
        }

        // Evitar doble envío
        submitBtn.disabled = true;
        submitBtn.textContent = "Agendando...";
    });

    // Evitar fechas pasadas en el calendario
    const hoyISO = new Date().toISOString().split("T")[0];
    fechaInput.setAttribute("min", hoyISO);

    document.addEventListener("DOMContentLoaded", () => {
    const radios = document.querySelectorAll(".hora-item input[type='radio']");

    radios.forEach(radio => {
        radio.addEventListener("change", () => {
            radios.forEach(r => r.parentElement.classList.remove("activo"));
            radio.parentElement.classList.add("activo");
        });
    });
});

});
