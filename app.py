from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from psycopg2.extras import RealDictCursor

from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm
from forms.registro_form import RegistroForm
from forms.login_form import LoginForm


from conexion.conexion import obtener_conexion
from models.usuario import Usuario


app = Flask(__name__)


# Clave secreta utilizada por Flask-WTF para la protección CSRF
app.config["SECRET_KEY"] = "dpatty-clave-secreta-2026"

# Configuración de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "Debe iniciar sesión para acceder a esta página."
login_manager.login_message_category = "warning"

@login_manager.user_loader
def load_user(user_id):

    conexion = obtener_conexion()
    cursor = conexion.cursor(cursor_factory=RealDictCursor)

    cursor.execute("""
        SELECT id, usuario, password
        FROM usuarios
        WHERE id = %s
    """, (user_id,))

    usuario = cursor.fetchone()

    cursor.close()
    conexion.close()

    if usuario:
        return Usuario(
            usuario["id"],
            usuario["usuario"],
            usuario["password"]
        )

    return None
# Ruta para registrar usuarios
@app.route("/registro", methods=["GET", "POST"])
def registro():

    form = RegistroForm()

    if form.validate_on_submit():

        conexion = obtener_conexion()
        cursor = conexion.cursor(cursor_factory=RealDictCursor)

        # Comprobar si el usuario ya existe
        cursor.execute("""
            SELECT id
            FROM usuarios
            WHERE usuario = %s
        """, (form.usuario.data,))

        usuario_existente = cursor.fetchone()

        if usuario_existente:
            cursor.close()
            conexion.close()

            flash(
                "El nombre de usuario ya está registrado.",
                "warning"
            )

            return render_template(
                "registro.html",
                form=form
            )

        # Generar hash de la contraseña
        password_hash = generate_password_hash(
            form.password.data
        )

        #  Guardar usuario en PostgreSQL
        cursor.execute("""
            INSERT INTO usuarios (usuario, password)
            VALUES (%s, %s)
        """, (
            form.usuario.data,
            password_hash
        ))

        conexion.commit()

        cursor.close()
        conexion.close()

        flash(
            "Usuario registrado correctamente.",
            "success"
        )

        return redirect(url_for("login"))

    return render_template(
        "registro.html",
        form=form
    )

# Ruta para iniciar sesión
@app.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():

        conexion = obtener_conexion()
        cursor = conexion.cursor(cursor_factory=RealDictCursor)

        # Buscar el usuario en la base de datos
        cursor.execute("""
            SELECT id, usuario, password
            FROM usuarios
            WHERE usuario = %s
        """, (form.usuario.data,))

        usuario = cursor.fetchone()

        cursor.close()
        conexion.close()

        # Verificar usuario y contraseña
        if usuario and check_password_hash(
            usuario["password"],
            form.password.data
        ):

            usuario_obj = Usuario(
                usuario["id"],
                usuario["usuario"],
                usuario["password"]
            )

            login_user(usuario_obj)

            flash(
                "Inicio de sesión correcto.",
                "success"
            )

            return redirect(url_for("inicio"))

        flash(
            "Usuario o contraseña incorrectos.",
            "danger"
        )

    return render_template(
        "login.html",
        form=form
    )

# Ruta para cerrar sesión
@app.route("/logout")
def logout():
    logout_user()

    flash(
        "Sesión cerrada correctamente.",
        "success"
    )

    return redirect(url_for("login"))



# Ruta principal
@app.route("/")
def inicio():
    return render_template("index.html")


# Ruta de productos
@app.route("/productos")
@login_required
def productos():

    conexion = obtener_conexion()
    cursor = conexion.cursor(cursor_factory=RealDictCursor)

    cursor.execute("""
    SELECT
        p.id_producto,
        p.nombre,
        p.descripcion,
        p.precio,
        p.disponible,
        pr.nombre AS proveedor
    FROM productos p
    LEFT JOIN proveedores pr
        ON p.id_proveedor = pr.id_proveedor
    ORDER BY p.id_producto DESC
""")

    lista_productos = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        "productos.html",
        titulo="Productos D'Patty Confecciones",
        productos=lista_productos
    )

# Ruta para registrar productos
@app.route("/productos/nuevo", methods=["GET", "POST"])
@login_required
def nuevo_producto():

    form = ProductoForm()

    # Cargar proveedores para el selector
    conexion = obtener_conexion()
    cursor = conexion.cursor(cursor_factory=RealDictCursor)

    cursor.execute("""
        SELECT id_proveedor, nombre
        FROM proveedores
        ORDER BY nombre
    """)

    lista_proveedores = cursor.fetchall()

    cursor.close()
    conexion.close()

    form.proveedor.choices = [
        (proveedor["id_proveedor"], proveedor["nombre"])
        for proveedor in lista_proveedores
    ]

    # Guardar producto solamente cuando el formulario sea válido
    if form.validate_on_submit():

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            """
            INSERT INTO productos (
                nombre,
                descripcion,
                precio,
                disponible,
                id_proveedor
            )
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                form.nombre.data,
                form.descripcion.data,
                float(form.precio.data),
                form.disponible.data,
                form.proveedor.data
            )
        )

        conexion.commit()

        cursor.close()
        conexion.close()

        print("PRODUCTO GUARDADO EN POSTGRESQL")
        flash("Producto guardado correctamente.", "success")

        return redirect(url_for("productos"))

    return render_template(
        "formulario_producto.html",
        form=form
    )
# Ruta para editar producto
@app.route("/productos/editar/<int:id_producto>", methods=["GET", "POST"])
@login_required
def editar_producto(id_producto):

    conexion = obtener_conexion()
    cursor = conexion.cursor(cursor_factory=RealDictCursor)

    # Buscar el producto por ID
    cursor.execute("""
        SELECT
            id_producto,
            nombre,
            descripcion,
            precio,
            disponible,
            id_proveedor
        FROM productos
        WHERE id_producto = %s
    """, (id_producto,))

    producto = cursor.fetchone()

    if producto is None:
        cursor.close()
        conexion.close()
        return "Producto no encontrado", 404

    form = ProductoForm()

    # Cargar proveedores en el selector
    cursor.execute("""
        SELECT id_proveedor, nombre
        FROM proveedores
        ORDER BY nombre
    """)

    lista_proveedores = cursor.fetchall()

    form.proveedor.choices = [
        (proveedor["id_proveedor"], proveedor["nombre"])
        for proveedor in lista_proveedores
    ]

    # Cargar los datos actuales en el formulario
    if request.method == "GET":
        form.nombre.data = producto["nombre"]
        form.descripcion.data = producto["descripcion"]
        form.precio.data = producto["precio"]
        form.disponible.data = producto["disponible"]

        if producto["id_proveedor"] is not None:
            form.proveedor.data = producto["id_proveedor"]

    # Actualizar producto
    if form.validate_on_submit():

        cursor.execute("""
            UPDATE productos
            SET nombre = %s,
                descripcion = %s,
                precio = %s,
                disponible = %s,
                id_proveedor = %s
            WHERE id_producto = %s
        """, (
            form.nombre.data,
            form.descripcion.data,
            form.precio.data,
            form.disponible.data,
            form.proveedor.data,
            id_producto
        ))

        conexion.commit()

        cursor.close()
        conexion.close()

        flash("Producto actualizado correctamente.", "success")

        return redirect(url_for("productos"))

    cursor.close()
    conexion.close()

    return render_template(
        "formulario_producto.html",
        form=form,
        titulo="Editar producto"
    )

# Ruta para eliminar producto
@app.route("/productos/eliminar/<int:id_producto>", methods=["POST"])
@login_required
def eliminar_producto(id_producto):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        """
        DELETE FROM productos
        WHERE id_producto = %s
        """,
        (id_producto,)
    )

    conexion.commit()

    cursor.close()
    conexion.close()

    flash("Producto eliminado correctamente.", "success")

    return redirect(url_for("productos"))

# Ruta de clientes

@app.route("/clientes")
@login_required
def clientes():

    conexion = obtener_conexion()
    cursor = conexion.cursor(cursor_factory=RealDictCursor)

    cursor.execute("""
        SELECT id_cliente, nombre, cedula, telefono, correo
        FROM clientes
        ORDER BY id_cliente DESC
    """)

    lista_clientes = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        "clientes.html",
        titulo="Clientes registrados",
        clientes=lista_clientes
    )

# Ruta para registrar clientes
@app.route("/clientes/nuevo", methods=["GET", "POST"])
@login_required
def nuevo_cliente():

    form = ClienteForm()

    if form.validate_on_submit():

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            """
            INSERT INTO clientes (
                nombre,
                cedula,
                telefono,
                correo
            )
            VALUES (%s, %s, %s, %s)
            """,
            (
                form.nombre.data,
                form.cedula.data,
                form.telefono.data,
                form.correo.data
            )
        )

        conexion.commit()

        cursor.close()
        conexion.close()

        print("CLIENTE GUARDADO EN POSTGRESQL")

        flash(
            "Cliente guardado correctamente.",
            "success"
        )

        return redirect(url_for("clientes"))

    return render_template(
        "formulario_cliente.html",
        form=form
    )

# Ruta para editar cliente
@app.route("/clientes/editar/<int:id_cliente>", methods=["GET", "POST"])
@login_required
def editar_cliente(id_cliente):

    conexion = obtener_conexion()
    cursor = conexion.cursor(cursor_factory=RealDictCursor)

    # Buscar el cliente por ID
    cursor.execute("""
        SELECT id_cliente, nombre, cedula, telefono, correo
        FROM clientes
        WHERE id_cliente = %s
    """, (id_cliente,))

    cliente = cursor.fetchone()

    if cliente is None:
        cursor.close()
        conexion.close()
        return "Cliente no encontrado", 404

    form = ClienteForm()

    # Cargar los datos actuales del cliente
    if request.method == "GET":
        form.nombre.data = cliente["nombre"]
        form.cedula.data = cliente["cedula"]
        form.telefono.data = cliente["telefono"]
        form.correo.data = cliente["correo"]

    # Guardar los cambios
    if form.validate_on_submit():

        cursor.execute("""
            UPDATE clientes
            SET nombre = %s,
                cedula = %s,
                telefono = %s,
                correo = %s
            WHERE id_cliente = %s
        """, (
            form.nombre.data,
            form.cedula.data,
            form.telefono.data,
            form.correo.data,
            id_cliente
        ))

        conexion.commit()

        cursor.close()
        conexion.close()

        flash("Cliente actualizado correctamente.", "success")

        return redirect(url_for("clientes"))

    cursor.close()
    conexion.close()

    return render_template(
        "formulario_cliente.html",
        form=form,
        titulo="Editar cliente"
    )
    
# Ruta para eliminar cliente
@app.route("/clientes/eliminar/<int:id_cliente>", methods=["POST"])
@login_required
def eliminar_cliente(id_cliente):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        """
        DELETE FROM clientes
        WHERE id_cliente = %s
        """,
        (id_cliente,)
    )

    conexion.commit()

    cursor.close()
    conexion.close()

    flash("Cliente eliminado correctamente.", "success")

    return redirect(url_for("clientes"))

# Ruta de proveedores
@app.route("/proveedores")
@login_required
def proveedores():

    conexion = obtener_conexion()
    cursor = conexion.cursor(cursor_factory=RealDictCursor)

    cursor.execute("""
        SELECT id_proveedor, nombre, telefono, correo
        FROM proveedores
        ORDER BY id_proveedor DESC
    """)

    lista_proveedores = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        "proveedores.html",
        titulo="Proveedores registrados",
        proveedores=lista_proveedores
    )


# Ruta para registrar proveedores
@app.route("/proveedores/nuevo", methods=["GET", "POST"])
@login_required
def nuevo_proveedor():

    form = ProveedorForm()

    if form.validate_on_submit():

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            """
            INSERT INTO proveedores (
                nombre,
                telefono,
                correo
            )
            VALUES (%s, %s, %s)
            """,
            (
                form.nombre.data,
                form.telefono.data,
                form.correo.data
            )
        )

        conexion.commit()

        cursor.close()
        conexion.close()

        print("PROVEEDOR GUARDADO EN POSTGRESQL")

        flash(
            "Proveedor guardado correctamente.",
            "success"
        )

        return redirect(url_for("proveedores"))

    return render_template(
        "formulario_proveedor.html",
        form=form
    )
    
# Ruta para editar proveedor
@app.route("/proveedores/editar/<int:id_proveedor>", methods=["GET", "POST"])
@login_required
def editar_proveedor(id_proveedor):

    conexion = obtener_conexion()
    cursor = conexion.cursor(cursor_factory=RealDictCursor)

    # Buscar proveedor por ID
    cursor.execute("""
        SELECT id_proveedor, nombre, telefono, correo
        FROM proveedores
        WHERE id_proveedor = %s
    """, (id_proveedor,))

    proveedor = cursor.fetchone()

    if proveedor is None:
        cursor.close()
        conexion.close()
        return "Proveedor no encontrado", 404

    form = ProveedorForm()

    # Cargar datos actuales
    if request.method == "GET":
        form.nombre.data = proveedor["nombre"]
        form.telefono.data = proveedor["telefono"]
        form.correo.data = proveedor["correo"]

    # Guardar cambios
    if form.validate_on_submit():

        cursor.execute("""
            UPDATE proveedores
            SET nombre = %s,
                telefono = %s,
                correo = %s
            WHERE id_proveedor = %s
        """, (
            form.nombre.data,
            form.telefono.data,
            form.correo.data,
            id_proveedor
        ))

        conexion.commit()

        cursor.close()
        conexion.close()

        flash(
            "Proveedor actualizado correctamente.",
            "success"
        )

        return redirect(url_for("proveedores"))

    cursor.close()
    conexion.close()

    return render_template(
        "formulario_proveedor.html",
        form=form,
        titulo="Editar proveedor"
    )
# Ruta para eliminar proveedor
@app.route("/proveedores/eliminar/<int:id_proveedor>", methods=["POST"])
@login_required
def eliminar_proveedor(id_proveedor):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        """
        DELETE FROM proveedores
        WHERE id_proveedor = %s
        """,
        (id_proveedor,)
    )

    conexion.commit()

    cursor.close()
    conexion.close()

    flash(
        "Proveedor eliminado correctamente.",
        "success"
    )

    return redirect(url_for("proveedores"))

# Ruta de facturación
@app.route("/facturacion")
@login_required
def facturacion():

    conexion = obtener_conexion()
    cursor = conexion.cursor(cursor_factory=RealDictCursor)

    cursor.execute("""
        SELECT
            f.id_factura,
            c.nombre AS cliente,
            p.nombre AS producto,
            f.cantidad,
            f.total,
            f.estado
        FROM facturas f
        INNER JOIN clientes c
            ON f.id_cliente = c.id_cliente
        INNER JOIN productos p
            ON f.id_producto = p.id_producto
        ORDER BY f.id_factura DESC
    """)

    lista_facturas = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        "facturacion.html",
        titulo="Registro de facturación",
        facturas=lista_facturas
    )



# Ruta para registrar facturación
@app.route("/facturacion/nueva", methods=["GET", "POST"])
@login_required
def nueva_facturacion():

    form = FacturacionForm()

    conexion = obtener_conexion()
    cursor = conexion.cursor(cursor_factory=RealDictCursor)

    # Obtener clientes
    cursor.execute("""
        SELECT id_cliente, nombre
        FROM clientes
        ORDER BY nombre
    """)

    clientes = cursor.fetchall()

    form.cliente.choices = [
        (0, "-- Seleccione un cliente --")
    ] + [
        (cliente["id_cliente"], cliente["nombre"])
        for cliente in clientes
    ]

    # Obtener productos
    cursor.execute("""
        SELECT id_producto, nombre
        FROM productos
        WHERE disponible = TRUE
        ORDER BY nombre
    """)

    productos = cursor.fetchall()

    form.producto.choices = [
        (0, "-- Seleccione un producto --")
    ] + [
        (producto["id_producto"], producto["nombre"])
        for producto in productos
    ]

    # Procesar formulario
    if form.validate_on_submit():

        # Obtener precio del producto seleccionado
        cursor.execute("""
            SELECT precio
            FROM productos
            WHERE id_producto = %s
        """, (form.producto.data,))

        producto_seleccionado = cursor.fetchone()

        if producto_seleccionado is None:
            cursor.close()
            conexion.close()

            flash("Producto no encontrado.", "danger")

            return redirect(url_for("nueva_facturacion"))

        # Calcular total automáticamente
        precio = producto_seleccionado["precio"]
        total_calculado = precio * form.cantidad.data

        # Guardar factura
        cursor.execute("""
            INSERT INTO facturas
            (id_cliente, id_producto, cantidad, total, estado)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            form.cliente.data,
            form.producto.data,
            form.cantidad.data,
            total_calculado,
            form.estado.data
        ))

        conexion.commit()

        cursor.close()
        conexion.close()

        flash(
            "Factura registrada correctamente.",
            "success"
        )

        return redirect(url_for("facturacion"))

    cursor.close()
    conexion.close()

    return render_template(
        "formulario_facturacion.html",
        form=form
    )
    

# Ruta para editar facturación
@app.route("/facturacion/editar/<int:id_factura>", methods=["GET", "POST"])
@login_required
def editar_facturacion(id_factura):

    form = FacturacionForm()

    conexion = obtener_conexion()
    cursor = conexion.cursor(cursor_factory=RealDictCursor)

    # Buscar factura
    cursor.execute("""
        SELECT
            id_factura,
            id_cliente,
            id_producto,
            cantidad,
            estado
        FROM facturas
        WHERE id_factura = %s
    """, (id_factura,))

    factura = cursor.fetchone()

    if factura is None:
        cursor.close()
        conexion.close()
        return "Factura no encontrada", 404

    # Obtener clientes
    cursor.execute("""
        SELECT id_cliente, nombre
        FROM clientes
        ORDER BY nombre
    """)

    clientes = cursor.fetchall()

    form.cliente.choices = [
        (0, "-- Seleccione un cliente --")
    ] + [
        (cliente["id_cliente"], cliente["nombre"])
        for cliente in clientes
    ]

    # Obtener productos
    cursor.execute("""
        SELECT id_producto, nombre
        FROM productos
        WHERE disponible = TRUE
        ORDER BY nombre
    """)

    productos = cursor.fetchall()

    form.producto.choices = [
        (0, "-- Seleccione un producto --")
    ] + [
        (producto["id_producto"], producto["nombre"])
        for producto in productos
    ]

    # Cargar datos actuales
    if request.method == "GET":

        form.cliente.data = factura["id_cliente"]
        form.producto.data = factura["id_producto"]
        form.cantidad.data = factura["cantidad"]
        form.estado.data = factura["estado"]

    # Guardar cambios
    if form.validate_on_submit():

        # Obtener precio actual del producto
        cursor.execute("""
            SELECT precio
            FROM productos
            WHERE id_producto = %s
        """, (form.producto.data,))

        producto_seleccionado = cursor.fetchone()

        if producto_seleccionado is None:
            cursor.close()
            conexion.close()

            flash("Producto no encontrado.", "danger")

            return redirect(
                url_for(
                    "editar_facturacion",
                    id_factura=id_factura
                )
            )

        # Recalcular total
        precio = producto_seleccionado["precio"]
        total_calculado = precio * form.cantidad.data

        # Actualizar factura
        cursor.execute("""
            UPDATE facturas
            SET id_cliente = %s,
                id_producto = %s,
                cantidad = %s,
                total = %s,
                estado = %s
            WHERE id_factura = %s
        """, (
            form.cliente.data,
            form.producto.data,
            form.cantidad.data,
            total_calculado,
            form.estado.data,
            id_factura
        ))

        conexion.commit()

        cursor.close()
        conexion.close()

        flash(
            "Factura actualizada correctamente.",
            "success"
        )

        return redirect(url_for("facturacion"))

    cursor.close()
    conexion.close()

    return render_template(
        "formulario_facturacion.html",
        form=form,
        titulo="Editar factura"
    )

# Ruta para eliminar facturación
@app.route("/facturacion/eliminar/<int:id_factura>", methods=["POST"])
@login_required
def eliminar_facturacion(id_factura):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        """
        DELETE FROM facturas
        WHERE id_factura = %s
        """,
        (id_factura,)
    )

    conexion.commit()

    cursor.close()
    conexion.close()

    flash(
        "Factura eliminada correctamente.",
        "success"
    )

    return redirect(url_for("facturacion"))

# Ejecutar aplicación
if __name__ == "__main__":
    
    app.run(debug=True)