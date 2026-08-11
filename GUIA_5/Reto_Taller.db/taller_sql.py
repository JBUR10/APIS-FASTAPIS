import sqlite3

conexion = sqlite3.connect("taller.db")
cursor = conexion.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS estudiantes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        edad INTEGER,
        promedio REAL
    )
""")

conexion.commit()
cursor.execute(
    "INSERT INTO estudiantes (nombre, edad, promedio) VALUES (?, ?, ?)",
    ("Carlos", 20, 4.2),
)

estudiantes = [
    ("Joel", 22, 4.8),
    ("Luis", 19, 3.9),
    ("Sergio", 25, 4.5),
    ("Durman", 21, 3.7),
    ("Sebastian", 23, 4.9),
]

cursor.executemany(
    "INSERT INTO estudiantes (nombre, edad, promedio) VALUES (?, ?, ?)",
    estudiantes,
)

conexion.commit()

cursor.execute("SELECT * FROM estudiantes")
filas = cursor.fetchall()

print("\n--- TODOS LOS ESTUDIANTES ---")

for fila in filas:
    print(fila)


cursor.execute("SELECT * FROM estudiantes WHERE edad > 20")
filas = cursor.fetchall()

print("\n--- ESTUDIANTES MAYORES DE 20 ---")

for fila in filas:
    print(fila)


cursor.execute("SELECT * FROM estudiantes ORDER BY promedio DESC")
filas = cursor.fetchall()

print("\n--- ORDENADOS POR PROMEDIO ---")

for fila in filas:
    print(fila)


cursor.execute("SELECT * FROM estudiantes ORDER BY promedio DESC LIMIT 3")
filas = cursor.fetchall()

print("\n--- LOS 3 MEJORES PROMEDIOS ---")

for fila in filas:
    print(fila)


cursor.execute("SELECT * FROM estudiantes")
fila = cursor.fetchone()

print("\n--- FETCHONE ---")
print(fila)


cursor.execute(
    "UPDATE estudiantes SET promedio = ? WHERE id = ?",
    (4.7, 1),
)

print("\nFilas actualizadas:", cursor.rowcount)

conexion.commit()


cursor.execute(
    "DELETE FROM estudiantes WHERE id = ?",
    (2,),
)

print("Filas eliminadas:", cursor.rowcount)

conexion.commit()


conexion.row_factory = sqlite3.Row
cursor = conexion.cursor()

cursor.execute("SELECT * FROM estudiantes")
filas = cursor.fetchall()

print("\n--- USANDO sqlite3.Row ---")

for fila in filas:
    print("Nombre:", fila["nombre"])
    print("Edad:", fila["edad"])
    print("Promedio:", fila["promedio"])
    print("Como diccionario:", dict(fila))
    print()


dato = "' OR '1'='1"

consulta_insegura = f"""
    SELECT * FROM estudiantes
    WHERE nombre = '{dato}'
"""

print("--- CONSULTA INSEGURA ---")
print(consulta_insegura)

cursor.execute(consulta_insegura)
filas = cursor.fetchall()

for fila in filas:
    print(dict(fila))


consulta_segura = """
    SELECT * FROM estudiantes
    WHERE nombre = ?
"""

cursor.execute(consulta_segura, (dato,))
filas = cursor.fetchall()

print("\n--- CONSULTA SEGURA ---")
print("Resultado:")

for fila in filas:
    print(dict(fila))


conexion.close()

print("\nConexión cerrada.")
