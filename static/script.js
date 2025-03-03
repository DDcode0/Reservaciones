document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("reservaForm");
    const listaReservas = document.getElementById("listaReservas");

    function cargarReservas() {
        fetch("/reservas")
            .then(response => response.json())
            .then(reservas => {
                listaReservas.innerHTML = "";
                reservas.forEach(reserva => {
                    const li = document.createElement("li");
                    li.innerHTML = `${reserva.nombre} - ${reserva.fecha_entrada} a ${reserva.fecha_salida} - Habitación ${reserva.habitacion} 
                                    <button onclick="eliminarReserva(${reserva.id})">Eliminar</button>`;
                    listaReservas.appendChild(li);
                });
            });
    }

    form.addEventListener("submit", function (event) {
        event.preventDefault();
        const nuevaReserva = {
            nombre: document.getElementById("nombre").value,
            fecha_entrada: document.getElementById("fecha_entrada").value,
            fecha_salida: document.getElementById("fecha_salida").value,
            habitacion: document.getElementById("habitacion").value
        };

        fetch("/reservas", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(nuevaReserva)
        }).then(() => {
            form.reset();
            cargarReservas();
        });
    });

    window.eliminarReserva = function (id) {
        fetch(`/reservas/${id}`, { method: "DELETE" })
            .then(() => cargarReservas());
    };

    cargarReservas();
});
