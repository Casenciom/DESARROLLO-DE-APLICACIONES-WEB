
// ==========================
// OBTENER ELEMENTOS DEL HTML
// ==========================

const formulario = document.getElementById("formProducto");

const nombre = document.getElementById("nombre");
const descripcion = document.getElementById("descripcion");
const categoria = document.getElementById("categoria");

const errorNombre = document.getElementById("errorNombre");
const errorDescripcion = document.getElementById("errorDescripcion");
const errorCategoria = document.getElementById("errorCategoria");

const mensaje = document.getElementById("mensaje");

const listaProductos = document.getElementById("listaProductos");
const estadoProductos = document.getElementById("estadoProductos");

const total = document.getElementById("total");

// ==========================
// NUEVOS ELEMENTOS BOOTSTRAP
// ==========================

const spinner = document.getElementById("spinner");

const modalEliminar = new bootstrap.Modal(
    document.getElementById("modalEliminar")
);

const confirmarEliminar =
document.getElementById("confirmarEliminar");

let indiceEliminar = null;

// ==========================
// ARREGLO DE PRODUCTOS
// ==========================

let productos = [];

// ==========================
// VALIDAR NOMBRE
// ==========================

function validarNombre() {

    if (nombre.value.trim().length < 3) {

        errorNombre.textContent = "Debe ingresar mínimo 3 caracteres.";

        nombre.classList.add("is-invalid");
        nombre.classList.remove("is-valid");

        return false;
    }

    errorNombre.textContent = "";

    nombre.classList.remove("is-invalid");
    nombre.classList.add("is-valid");

    return true;
}

// ==========================
// VALIDAR DESCRIPCIÓN
// ==========================

function validarDescripcion() {

    if (descripcion.value.trim().length < 15) {

        errorDescripcion.textContent = "La descripción debe tener mínimo 15 caracteres.";

        descripcion.classList.add("is-invalid");
        descripcion.classList.remove("is-valid");

        return false;
    }

    errorDescripcion.textContent = "";

    descripcion.classList.remove("is-invalid");
    descripcion.classList.add("is-valid");

    return true;
}

// ==========================
// VALIDAR CATEGORÍA
// ==========================

function validarCategoria() {

    if (categoria.value == "") {

        errorCategoria.textContent = "Seleccione una categoría.";

        categoria.classList.add("is-invalid");
        categoria.classList.remove("is-valid");

        return false;
    }

    errorCategoria.textContent = "";

    categoria.classList.remove("is-invalid");
    categoria.classList.add("is-valid");

    return true;
}

// ==========================
// MOSTRAR PRODUCTOS
// ==========================

function mostrarProductos() {

    listaProductos.innerHTML = "";

    if (productos.length === 0) {

        estadoProductos.innerHTML = `
        <div class="alert alert-warning">
            No existen productos registrados.
        </div>
        `;

    } else {

        estadoProductos.innerHTML = "";

    }

    productos.forEach(function (producto, indice) {

        const columna = document.createElement("div");

        columna.className = "col-md-4 mb-3";

        columna.innerHTML = `

        <div class="card p-3 h-100">

            <h5>${producto.nombre}</h5>

            <p>${producto.descripcion}</p>

            <p><strong>Categoría:</strong> ${producto.categoria}</p>

            <button class="btn btn-danger">
                Eliminar
            </button>

        </div>

        `;

        const botonEliminar = columna.querySelector("button");

botonEliminar.addEventListener("click", function () {

    indiceEliminar = indice;

    modalEliminar.show();

});
        listaProductos.appendChild(columna);

    });

    total.textContent = productos.length;

}

// ==========================
// EVENTOS EN TIEMPO REAL
// ==========================

nombre.addEventListener("input", validarNombre);
nombre.addEventListener("blur", validarNombre);

descripcion.addEventListener("input", validarDescripcion);
descripcion.addEventListener("blur", validarDescripcion);

categoria.addEventListener("change", validarCategoria);
categoria.addEventListener("blur", validarCategoria);

// ==========================
// ENVIAR FORMULARIO
// ==========================

formulario.addEventListener("submit", function (event) {

    event.preventDefault();

    const nombreValido = validarNombre();
    const descripcionValida = validarDescripcion();
    const categoriaValida = validarCategoria();

    if (!(nombreValido && descripcionValida && categoriaValida)) {

        mensaje.innerHTML = `

<div class="alert alert-danger alert-dismissible fade show">

<strong>Error.</strong>

Corrija los campos antes de registrar.

<button
class="btn-close"
data-bs-dismiss="alert">
</button>

</div>

`;

        return;
    }

    // Crear objeto

    const producto = {

        nombre: nombre.value,

        descripcion: descripcion.value,

        categoria: categoria.value

    };

    // Mostrar Spinner

spinner.classList.remove("d-none");

// Simular carga

setTimeout(function(){

    productos.push(producto);

    spinner.classList.add("d-none");

    mensaje.innerHTML=`

    <div class="alert alert-success alert-dismissible fade show">

<strong>Éxito.</strong>

Producto registrado correctamente.

<button
class="btn-close"
data-bs-dismiss="alert">
</button>

</div>

    `;

    mostrarProductos();

},1500);

    formulario.reset();

    nombre.classList.remove("is-valid");
    descripcion.classList.remove("is-valid");
    categoria.classList.remove("is-valid");

});

// ==========================
// CARGAR LA PÁGINA
// ==========================

mostrarProductos();

// ==========================
// CONFIRMAR ELIMINACIÓN
// ==========================

confirmarEliminar.addEventListener("click", function(){

    if(indiceEliminar !== null){

        productos.splice(indiceEliminar,1);

        mostrarProductos();

        modalEliminar.hide();

        indiceEliminar = null;

    }

});