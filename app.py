from flask import Flask, render_template, redirect, url_for, flash
from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm


import sqlite3
import os

app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

DB_PATH = os.path.join(
    BASE_DIR,
    "data",
    "dpatty.db"
)

def inicializar_bd():
    
    conexion = sqlite3.connect(DB_PATH)

    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT NOT NULL,
            precio REAL NOT NULL,
            disponible INTEGER NOT NULL
        )
    """)

    conexion.commit()

    conexion.close()

# Clave secreta utilizada por Flask-WTF para la protección CSRF
app.config["SECRET_KEY"] = "dpatty-clave-secreta-2026"

# Ruta principal
@app.route("/")
def inicio():
    return render_template("index.html")


# Ruta de productos
@app.route("/productos")
def productos():

    conexion = sqlite3.connect(DB_PATH)

    conexion.row_factory = sqlite3.Row

    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id, nombre, descripcion, precio, disponible
        FROM productos
        ORDER BY id DESC
    """)

    lista_productos = cursor.fetchall()

    conexion.close()

    return render_template(
        "productos.html",
        titulo="Productos D'Patty Confecciones",
        productos=lista_productos
    )
    

# Ruta para registrar productos
@app.route("/productos/nuevo", methods=["GET", "POST"])
def nuevo_producto():

    form = ProductoForm()

    if form.validate_on_submit():

        conexion = sqlite3.connect(DB_PATH)

        cursor = conexion.cursor()

        cursor.execute(
            """
            INSERT INTO productos (
                nombre,
                descripcion,
                precio,
                disponible
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                form.nombre.data,
                form.descripcion.data,
                float(form.precio.data),
                1 if form.disponible.data else 0
            )
        )

        conexion.commit()

        conexion.close()

        print("PRODUCTO GUARDADO EN SQLITE")
        flash("Producto guardado correctamente.", "success")
        return redirect(url_for("productos"))

    return render_template(
        "formulario_producto.html",
        form=form
    )

# Ruta de clientes
@app.route("/clientes")
def clientes():

    titulo_clientes = "Clientes registrados"

    lista_clientes = [
        {
            "nombre": "María López",
            "correo": "marialp@gmail.com",
            "tipo_cliente": "Frecuente"
        },
        {
            "nombre": "Andrea Torres",
            "correo": "andreatr@gmail.com",
            "tipo_cliente": "Nuevo"
        },
        {
            "nombre": "Carlos Mendoza",
            "correo": "carlosmz@gmail.com",
            "tipo_cliente": "Frecuente"
        }
    ]

    return render_template(
        "clientes.html",
        titulo=titulo_clientes,
        clientes=lista_clientes
    )

# Ruta para registrar clientes
@app.route("/clientes/nuevo", methods=["GET", "POST"])
def nuevo_cliente():

    form = ClienteForm()

    if form.validate_on_submit():

        print("CLIENTE VÁLIDO")
        print("Nombre:", form.nombre.data)
        print("Correo:", form.correo.data)
        print("Tipo de cliente:", form.tipo_cliente.data)

    return render_template(
        "formulario_cliente.html",
        form=form
    )


# Ruta de proveedores
@app.route("/proveedores")
def proveedores():

    titulo_proveedores = "Proveedores registrados"

    lista_proveedores = [
        {
            "nombre": "Almacén de Telas El Tuko",
            "producto": "Telas y tejidos",
            "telefono": "0991234567",
            "estado": "Activo"
        },
        {
            "nombre": "Distribuidora El Botón",
            "producto": "Botones y accesorios",
            "telefono": "0987654321",
            "estado": "Activo"
        },
        {
            "nombre": "Insumos de Costura",
            "producto": "Hilos y materiales de confección",
            "telefono": "0974561230",
            "estado": "Inactivo"
        }
    ]

    return render_template(
        "proveedores.html",
        titulo=titulo_proveedores,
        proveedores=lista_proveedores
    )


# Ruta para registrar proveedores
@app.route("/proveedores/nuevo", methods=["GET", "POST"])
def nuevo_proveedor():

    form = ProveedorForm()

    if form.validate_on_submit():

        print("PROVEEDOR VÁLIDO")
        print("Nombre:", form.nombre.data)
        print("Producto o insumo:", form.producto.data)
        print("Teléfono:", form.telefono.data)
        print("Estado:", form.estado.data)

    return render_template(
        "formulario_proveedor.html",
        form=form
    )


# Ruta de facturación
@app.route("/facturacion")
def facturacion():

    titulo_facturacion = "Registro de facturación"

    lista_facturas = [
        {
            "numero": "PMH-001",
            "cliente": "María López",
            "producto": "Vestido personalizado",
            "total": 45.00,
            "estado": "Pagada"
        },
        {
            "numero": "PMH-002",
            "cliente": "Andrea Torres",
            "producto": "Blusa",
            "total": 25.00,
            "estado": "Pendiente"
        },
        {
            "numero": "PMH-003",
            "cliente": "Carlos Mendoza",
            "producto": "Conjunto",
            "total": 55.00,
            "estado": "Pagada"
        }
    ]

    return render_template(
        "facturacion.html",
        titulo=titulo_facturacion,
        facturas=lista_facturas
    )


# Ruta para registrar facturación
@app.route("/facturacion/nueva", methods=["GET", "POST"])
def nueva_facturacion():

    form = FacturacionForm()

    if form.validate_on_submit():

        print("FACTURACIÓN VÁLIDA")
        print("Cliente:", form.cliente.data)
        print("Producto:", form.producto.data)
        print("Cantidad:", form.cantidad.data)
        print("Total:", form.total.data)
        print("Estado:", form.estado.data)

    return render_template(
        "formulario_facturacion.html",
        form=form
    )

# Ejecutar aplicación
if __name__ == "__main__":
    
    inicializar_bd()

    app.run(debug=True)