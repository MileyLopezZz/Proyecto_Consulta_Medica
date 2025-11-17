document.addEventListener("DOMContentLoaded", () => {
    const fechaInput = document.getElementById("fecha");
    const contenedorHorarios = document.getElementById("horarios-container");
    const mensajeHorarios = document.getElementById("mensaje-horarios");

    // Bloquear fechas pasadas (min = hoy en local, sin UTC)
    const hoy = new Date();
    const yyyy = hoy.getFullYear();
    const mm = String(hoy.getMonth() + 1).padStart(2, "0");
    const dd = String(hoy.getDate()).padStart(2, "0");
    fechaInput.min = `${yyyy}-${mm}-${dd}`;

    // Lunes–Jueves
    const horariosNormales = [
        "9:00 AM","9:30 AM","10:00 AM","10:30 AM",
        "11:00 AM","11:30 AM","12:00 PM",
        "2:00 PM","2:30 PM","3:00 PM","3:30 PM","4:00 PM","4:30 PM"
    ];

    // Viernes (hasta 12:00 PM)
    const horariosViernes = [
        "9:00 AM","9:30 AM","10:00 AM","10:30 AM",
        "11:00 AM","11:30 AM","12:00 PM"
    ];

    fechaInput.addEventListener("change", () => {
        contenedorHorarios.innerHTML = "";
        mensajeHorarios.textContent = "";

        if (!fechaInput.value) {
            mensajeHorarios.textContent = "Por favor selecciona una fecha válida.";
            return;
        }

        // Crear la fecha en LOCAL (evita el desfase por UTC)
        const [Y, M, D] = fechaInput.value.split("-").map(Number);
        const fechaLocal = new Date(Y, M - 1, D); // <- local time
        const dia = fechaLocal.getDay(); // 0=Dom, 1=Lun, 2=Mar, 3=Mié, 4=Jue, 5=Vie, 6=Sáb

        // Fines de semana
        if (dia === 0 || dia === 6) {
            mensajeHorarios.textContent = "No hay horarios disponibles para fines de semana.";
            return;
        }

        // Elegir lista según el día (viernes = 5)
        const lista = (dia === 5) ? horariosViernes : horariosNormales;

        // Render de botones
        lista.forEach(hora => {
            const label = document.createElement("label");
            label.classList.add("hora-item");

            const input = document.createElement("input");
            input.type = "radio";
            input.name = "hora";
            input.value = hora;

            label.appendChild(input);
            label.appendChild(document.createTextNode(hora));
            contenedorHorarios.appendChild(label);
        });

        // Activar resaltado al seleccionar
        activarSeleccion();
    });

    function activarSeleccion() {
        const radios = contenedorHorarios.querySelectorAll(".hora-item input");
        radios.forEach(r => {
            r.addEventListener("change", () => {
                radios.forEach(x => x.parentElement.classList.remove("activo"));
                r.parentElement.classList.add("activo");
            });
        });
    }
});
