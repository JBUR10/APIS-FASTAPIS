import sqlite3
import bcrypt

DB_NAME = "store.db"


def obtener_conexion():
    conexion = sqlite3.connect(DB_NAME, check_same_thread=False)
    conexion.row_factory = sqlite3.Row
    conexion.execute("PRAGMA foreign_keys = ON")
    return conexion


def crear_tablas():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Categoria (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE
        )
        """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Producto (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE,
            precio REAL NOT NULL,
            id_categoria INTEGER NOT NULL,
            id_proveedor INTEGER NOT NULL,
            FOREIGN KEY (id_categoria) REFERENCES Categoria(id),
            FOREIGN KEY (id_proveedor) REFERENCES Proveedor(id)
        )
        """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Proveedor (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE,
            telefono TEXT,
            correo TEXT
        )
        """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Usuario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            nombre TEXT NOT NULL,
            password TEXT NOT NULL,
            rol TEXT NOT NULL
        )
        """)

    conexion.commit()
    conexion.close()

    print(f"[BD] Tablas verificadas en DB {DB_NAME}")

def sembrar_datos():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    # Usuarios
    cursor.execute("SELECT COUNT(*) FROM Usuario")
    cantidad_usuarios = cursor.fetchone()[0]

    if cantidad_usuarios == 0:

        password_admin = bcrypt.hashpw(
            "admin123".encode(),
            bcrypt.gensalt()
        ).decode()

        password_joel = bcrypt.hashpw(
            "joel123".encode(),
            bcrypt.gensalt()
        ).decode()

        cursor.execute("""
            INSERT INTO Usuario
            (username, nombre, password, rol)
            VALUES (?, ?, ?, ?)
        """, (
            "admin",
            "Administrador",
            password_admin,
            "admin"
        ))

        cursor.execute("""
            INSERT INTO Usuario
            (username, nombre, password, rol)
            VALUES (?, ?, ?, ?)
        """, (
            "joel",
            "Joel Cliente",
            password_joel,
            "cliente"
        ))

    # Categorías
    cursor.execute("SELECT COUNT(*) FROM Categoria")
    cantidad_categorias = cursor.fetchone()[0]

    if cantidad_categorias == 0:
        cursor.execute(
            "INSERT INTO Categoria (nombre) VALUES (?)",
            ("Perifericos",)
        )

        cursor.execute(
            "INSERT INTO Categoria (nombre) VALUES (?)",
            ("Pantallas",)
        )

        cursor.execute(
            "INSERT INTO Categoria (nombre) VALUES (?)",
            ("Audio",)
        )

    # Proveedores
    cursor.execute("SELECT COUNT(*) FROM Proveedor")
    cantidad_proveedores = cursor.fetchone()[0]

    if cantidad_proveedores == 0:
        cursor.execute("""
            INSERT INTO Proveedor
            (nombre, telefono, correo)
            VALUES (?, ?, ?)
        """, (
            "Manzana (Apol)",
            "3001234567",
            "contacto@apol.com"
        ))

        cursor.execute("""
            INSERT INTO Proveedor
            (nombre, telefono, correo)
            VALUES (?, ?, ?)
        """, (
            "Distribuciones Metrio",
            "3109876543",
            "ventas@metrio.com"
        ))

        cursor.execute("""
            INSERT INTO Proveedor
            (nombre, telefono, correo)
            VALUES (?, ?, ?)
        """, (
            "Flamingo",
            "3204567890",
            "info@flamingo.com"
        ))

    conexion.commit()
    conexion.close()