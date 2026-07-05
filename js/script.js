
// OBTENER ELEMENTOS


const formulario = document.getElementById("formProducto");

const nombre = document.getElementById("nombre");

const descripcion = document.getElementById("descripcion");

const categoria = document.getElementById("categoria");

const errorNombre = document.getElementById("errorNombre");

const errorDescripcion = document.getElementById("errorDescripcion");

const errorCategoria = document.getElementById("errorCategoria");

const listaProductos = document.getElementById("listaProductos");

const total = document.getElementById("total");

const mensaje = document.getElementById("mensaje");

let contador = 0;


// VALIDAR NOMBRE


function validarNombre(){

    if(nombre.value.trim().length < 3){

        errorNombre.textContent="Debe tener mínimo 3 caracteres.";

        nombre.classList.add("is-invalid");

        nombre.classList.remove("is-valid");

        return false;

    }

    errorNombre.textContent="";

    nombre.classList.remove("is-invalid");

    nombre.classList.add("is-valid");

    return true;

}


// VALIDAR DESCRIPCIÓN


function validarDescripcion(){

    if(descripcion.value.trim().length < 15){

        errorDescripcion.textContent="La descripción debe tener mínimo 15 caracteres.";

        descripcion.classList.add("is-invalid");

        descripcion.classList.remove("is-valid");

        return false;

    }

    errorDescripcion.textContent="";

    descripcion.classList.remove("is-invalid");

    descripcion.classList.add("is-valid");

    return true;

}


// VALIDAR CATEGORÍA


function validarCategoria(){

    if(categoria.value==""){

        errorCategoria.textContent="Seleccione una categoría.";

        categoria.classList.add("is-invalid");

        categoria.classList.remove("is-valid");

        return false;

    }

    errorCategoria.textContent="";

    categoria.classList.remove("is-invalid");

    categoria.classList.add("is-valid");

    return true;

}


// EVENTOS EN TIEMPO REAL


nombre.addEventListener("input",validarNombre);

nombre.addEventListener("blur",validarNombre);

descripcion.addEventListener("input",validarDescripcion);

descripcion.addEventListener("blur",validarDescripcion);

categoria.addEventListener("change",validarCategoria);

categoria.addEventListener("blur",validarCategoria);


// ENVIAR FORMULARIO


formulario.addEventListener("submit",function(event){

    event.preventDefault();

    let nombreValido=validarNombre();

    let descripcionValida=validarDescripcion();

    let categoriaValida=validarCategoria();

    if(!(nombreValido && descripcionValida && categoriaValida)){

        mensaje.innerHTML=`
        <div class="alert alert-danger">
        Corrija los errores del formulario.
        </div>
        `;

        return;

    }

    mensaje.innerHTML=`
    <div class="alert alert-success">
    Producto registrado correctamente.
    </div>
    `;

    // Crear tarjeta

    let tarjeta=document.createElement("div");

    tarjeta.className="card p-3 mt-3";

    tarjeta.innerHTML=`

        <h5>${nombre.value}</h5>

        <p>${descripcion.value}</p>

        <p><strong>Categoría:</strong> ${categoria.value}</p>

        <button class="btn btn-danger btnEliminar">
            Eliminar
        </button>

    `;

    listaProductos.appendChild(tarjeta);

    contador++;

    total.textContent=contador;

    // Eliminar producto

    let botonEliminar=tarjeta.querySelector(".btnEliminar");

    botonEliminar.addEventListener("click",function(){

        tarjeta.remove();

        contador--;

        total.textContent=contador;

    });

    formulario.reset();

    nombre.classList.remove("is-valid");

    descripcion.classList.remove("is-valid");

    categoria.classList.remove("is-valid");

});