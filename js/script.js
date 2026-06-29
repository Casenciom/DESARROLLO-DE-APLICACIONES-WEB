// Obtener los elementos del HTML
const formulario = document.getElementById("formProducto");
const listaProductos = document.getElementById("listaProductos");
const mensaje = document.getElementById("mensaje");
const total = document.getElementById("total");

// Variable para contar los productos
let contador = 0;

// Evento cuando se envía el formulario
formulario.addEventListener("submit", function(event) {

    // Evita que la página se recargue
    event.preventDefault();

    // Obtener los datos del formulario
    let nombre = document.getElementById("nombre").value;
    let descripcion = document.getElementById("descripcion").value;
    let categoria = document.getElementById("categoria").value;

    // Validar que no estén vacíos
    if (nombre == "" || descripcion == "" || categoria == "") {

        mensaje.innerHTML =
        '<div class="alert alert-danger">Debe completar todos los campos.</div>';

        return;
    }

    // Mensaje de éxito
    mensaje.innerHTML =
    '<div class="alert alert-success">Producto registrado correctamente.</div>';

    // Crear el contenedor del producto
    let tarjeta = document.createElement("div");
    tarjeta.className = "card p-3 mb-3";

    // Agregar el contenido de la tarjeta
    tarjeta.innerHTML = `
        <h5>${nombre}</h5>
        <p>${descripcion}</p>
        <p><strong>Categoría:</strong> ${categoria}</p>
        <button class="btn btn-danger btnEliminar">Eliminar</button>
    `;

    // Agregar la tarjeta a la página
    listaProductos.appendChild(tarjeta);

    // Actualizar contador
    contador++;
    total.textContent = contador;

    // Evento para eliminar
    let botonEliminar = tarjeta.querySelector(".btnEliminar");

    botonEliminar.addEventListener("click", function() {

        tarjeta.remove();

        contador--;

        total.textContent = contador;

    });

    // Limpiar formulario
    formulario.reset();

});