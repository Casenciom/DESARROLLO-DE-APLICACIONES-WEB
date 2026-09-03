from flask import Flask, render_template

app = Flask(__name__)


# Ruta principal
@app.route("/")
def inicio():
    return render_template("index.html")


# Ruta de productos
@app.route("/productos")
def productos():

    titulo = "Catálogo de productos"

    lista_productos = [
        {
            "nombre": "Vestido personalizado",
            "descripcion": "Confección de vestidos personalizados de acuerdo con las medidas y preferencias del cliente.",
            "precio": 45.00,
            "disponible": True
        },
        {
            "nombre": "Blusa",
            "descripcion": "Blusas confeccionadas con diferentes diseños, estilos y tipos de tela.",
            "precio": 25.00,
            "disponible": True
        },
        {
            "nombre": "Falda",
            "descripcion": "Faldas elaboradas a medida según los requerimientos del cliente.",
            "precio": 30.00,
            "disponible": True
        },
        {
            "nombre": "Uniforme",
            "descripcion": "Confección de uniformes personalizados para empresas e instituciones.",
            "precio": 40.00,
            "disponible": False
        },
        {
            "nombre": "Conjunto",
            "descripcion": "Conjunto personalizado confeccionado según el estilo y medidas del cliente.",
            "precio": 55.00,
            "disponible": True
        }
    ]

    return render_template(
        "productos.html",
        titulo=titulo,
        productos=lista_productos
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


# Ejecutar aplicación
if __name__ == "__main__":
    app.run(debug=True)