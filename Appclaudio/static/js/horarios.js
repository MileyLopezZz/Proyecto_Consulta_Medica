document.addEventListener("DOMContentLoaded", () => {
  const fechaInput       = document.getElementById("id_fecha") || document.getElementById("fecha");
  const contenedorHorarios = document.getElementById("horarios-container");
  const mensajeHorarios  = document.getElementById("mensaje-horarios");
  const inputHoraForm    = document.getElementById("id_hora_inicio"); // <-- input del ModelForm (type=time)

  if (!fechaInput || !contenedorHorarios || !mensajeHorarios || !inputHoraForm) return;

  //  Bloquear fechas pasadas 
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

  // Si ya hay fecha, fuerza carga de horarios
  if (fechaInput.value) {
    renderHorariosParaFecha(fechaInput.value);
  }

  // Renderiza horarios cuando cambia la fecha
  fechaInput.addEventListener("change", () => {
    renderHorariosParaFecha(fechaInput.value);
  });


  function renderHorariosParaFecha(valorISO) {
    contenedorHorarios.innerHTML = "";
    mensajeHorarios.textContent = "";

    if (!valorISO) {
      mensajeHorarios.textContent = "Por favor selecciona una fecha válida.";
      return;
    }

    const [Y, M, D] = valorISO.split("-").map(Number);
    const fechaLocal = new Date(Y, M - 1, D);
    const dia = fechaLocal.getDay(); // 0=Dom, 1=Lun, ..., 6=Sáb

    // Fines de semana
    if (dia === 0 || dia === 6) {
      mensajeHorarios.textContent = "No hay horarios disponibles para fines de semana.";
      inputHoraForm.value = ""; // limpia hora del form
      return;
    }

    // Elegir lista (viernes = 5)
    const lista = (dia === 5) ? horariosViernes : horariosNormales;

    
    lista.forEach(horaAMP => {
      const label = document.createElement("label");
      label.classList.add("hora-item");

      const input = document.createElement("input");
      input.type = "radio";
      input.name = "hora";         
      input.value = horaAMP;

      input.addEventListener("change", () => {
        setSeleccionVisual(input);
        inputHoraForm.value = ampmTo24(horaAMP); 
      });

      label.appendChild(input);
      label.appendChild(document.createTextNode(horaAMP));
      contenedorHorarios.appendChild(label);
    });

    if (inputHoraForm.value) {
      const horaAMP = t24ToAmPm(inputHoraForm.value); 
      const radio = [...contenedorHorarios.querySelectorAll('input[name="hora"]')]
        .find(r => r.value === horaAMP);
      if (radio) {
        radio.checked = true;
        setSeleccionVisual(radio);
      }
    }
  }

  function setSeleccionVisual(radio) {
    const radios = contenedorHorarios.querySelectorAll(".hora-item input");
    radios.forEach(x => x.parentElement.classList.remove("activo"));
    if (radio?.parentElement) radio.parentElement.classList.add("activo");
  }

  // "9:00 AM" -> "09:00", "12:00 PM" -> "12:00", "12:00 AM" -> "00:00"
  function ampmTo24(ampm) {
    const m = ampm.trim().match(/^(\d{1,2}):(\d{2})\s?(AM|PM)$/i);
    if (!m) return "";
    let [_, h, min, p] = m;
    let hh = parseInt(h, 10);
    const pm = p.toUpperCase() === "PM";
    if (pm && hh < 12) hh += 12;
    if (!pm && hh === 12) hh = 0;
    return String(hh).padStart(2, "0") + ":" + min;
  }

  // "14:30" -> "2:30 PM", "00:00" -> "12:00 AM"
  function t24ToAmPm(hhmm) {
    const m = hhmm.trim().match(/^(\d{2}):(\d{2})$/);
    if (!m) return "";
    let [_, h, min] = m;
    let hh = parseInt(h, 10);
    const pm = hh >= 12;
    if (hh === 0) hh = 12;       // 00 -> 12 AM
    else if (hh > 12) hh -= 12;  // 13..23 -> 1..11 PM
    return `${hh}:${min} ${pm ? "PM" : "AM"}`;
  }
});


