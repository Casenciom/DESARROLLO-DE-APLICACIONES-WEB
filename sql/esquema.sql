-- =========================================
-- D'PATTY CONFECCIONES
-- Base de datos PostgreSQL
-- =========================================

-- La base de datos dpatty_db debe crearse
-- previamente desde PostgreSQL o pgAdmin.


-- =========================================
-- TABLA PROVEEDORES
-- =========================================

CREATE TABLE proveedores (
    id_proveedor SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    telefono VARCHAR(20),
    correo VARCHAR(100)
);


-- =========================================
-- TABLA PRODUCTOS
-- =========================================

CREATE TABLE productos (
    id_producto SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion VARCHAR(255),
    precio DECIMAL(10,2) NOT NULL,
    disponible BOOLEAN NOT NULL DEFAULT TRUE,
    id_proveedor INTEGER,

    FOREIGN KEY (id_proveedor)
        REFERENCES proveedores(id_proveedor)
);


-- =========================================
-- TABLA CLIENTES
-- =========================================

CREATE TABLE clientes (
    id_cliente SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    cedula VARCHAR(20) NOT NULL,
    telefono VARCHAR(20),
    correo VARCHAR(100)
);


-- =========================================
-- TABLA FACTURAS
-- =========================================

CREATE TABLE facturas (
    id_factura SERIAL PRIMARY KEY,
    id_cliente INTEGER NOT NULL,
    id_producto INTEGER NOT NULL,
    cantidad INTEGER NOT NULL DEFAULT 1,
    fecha TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    total DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    estado VARCHAR(20) NOT NULL DEFAULT 'Pendiente',

    FOREIGN KEY (id_cliente)
        REFERENCES clientes(id_cliente),

    FOREIGN KEY (id_producto)
        REFERENCES productos(id_producto)
);


-- =========================================
-- TABLA USUARIOS
-- =========================================

CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    usuario VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);


-- =========================================
-- CONSULTA CON JOIN
-- Relación PRODUCTOS - PROVEEDORES
-- =========================================

SELECT
    p.id_producto,
    p.nombre AS producto,
    pr.nombre AS proveedor
FROM productos p
LEFT JOIN proveedores pr
    ON p.id_proveedor = pr.id_proveedor
ORDER BY p.id_producto;


-- =========================================
-- CONSULTA CON JOIN
-- Relación FACTURAS - CLIENTES - PRODUCTOS
-- =========================================

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
ORDER BY f.id_factura;