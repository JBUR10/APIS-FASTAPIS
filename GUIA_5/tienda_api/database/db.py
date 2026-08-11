import sqlite3

DB_NAME = "store.db"


def obtener_conexion():
    conexion = sqlite3.connect(DB_NAME, check_same_thread=False)
    conexion.row_factory = sqlite3.Row
    conexion.execute("PRAGMA foreign_keys = ON")
    return conexion


def crearTablas():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Categoria (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Nombre TEXT NOT NULL UNIQUE
        )
        """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Producto (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Nombre TEXT NOT NULL UNIQUE,
            Precio FLOAT,
            id_categoria INTEGER,
            FOREIGN KEY (id_categoria) REFERENCES Categoria(id)
        )
        """)

    conexion.commit()
    conexion.close()

    print(f"[BD] Tablas verificadas en DB {DB_NAME}")
