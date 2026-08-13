from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import sqlite3

import seguridad
from database import db

router = APIRouter(
    prefix="/categorias",
    tags=["Categorias"]
)


class CategoriaEntrada(BaseModel):
    nombre: str


@router.get("")
def listar_categorias():
    conexion = db.obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT *
        FROM Categoria
    """)

    filas = cursor.fetchall()

    conexion.close()

    return [dict(fila) for fila in filas]


@router.get("/{categoria_id}")
def obtener_categoria(categoria_id: int):
    conexion = db.obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT *
        FROM Categoria
        WHERE id = ?
    """, (categoria_id,))

    fila = cursor.fetchone()

    conexion.close()

    if fila is None:
        raise HTTPException(
            status_code=404,
            detail="Categoria no encontrada"
        )

    return dict(fila)


@router.post("", status_code=201)
def crear_categoria(
    datos: CategoriaEntrada,
    usuario: dict = Depends(seguridad.obtener_usuario_actual)
):
    conexion = db.obtener_conexion()
    cursor = conexion.cursor()

    try:
        cursor.execute("""
            INSERT INTO Categoria (nombre)
            VALUES (?)
        """, (datos.nombre,))

        conexion.commit()

        nueva_id = cursor.lastrowid

    except sqlite3.IntegrityError:
        conexion.close()

        raise HTTPException(
            status_code=400,
            detail="La categoria ya existe"
        )

    cursor.execute("""
        SELECT *
        FROM Categoria
        WHERE id = ?
    """, (nueva_id,))

    fila = cursor.fetchone()

    conexion.close()

    return {
        "mensaje": "Categoria creada",
        "categoria": dict(fila),
        "creado_por": usuario["username"]
    }


@router.put("/{categoria_id}")
def actualizar_categoria(
    categoria_id: int,
    datos: CategoriaEntrada,
    usuario: dict = Depends(seguridad.obtener_usuario_actual)
):
    conexion = db.obtener_conexion()
    cursor = conexion.cursor()

    # Comprobar qué categoría existe antes de actualizar
    cursor.execute("""
        SELECT *
        FROM Categoria
        WHERE id = ?
    """, (categoria_id,))

    categoria_antes = cursor.fetchone()

    print(
        "[PUT] Antes:",
        dict(categoria_antes) if categoria_antes else None
    )

    try:
        cursor.execute("""
            UPDATE Categoria
            SET nombre = ?
            WHERE id = ?
        """, (
            datos.nombre,
            categoria_id
        ))

        print("[PUT] ID:", categoria_id)
        print("[PUT] Nuevo nombre:", datos.nombre)
        print("[PUT] Filas afectadas:", cursor.rowcount)

        conexion.commit()

    except sqlite3.IntegrityError:
        conexion.close()

        raise HTTPException(
            status_code=400,
            detail="La categoria ya existe"
        )

    if cursor.rowcount == 0:
        conexion.close()

        raise HTTPException(
            status_code=404,
            detail="Categoria no encontrada"
        )

    cursor.execute("""
        SELECT *
        FROM Categoria
        WHERE id = ?
    """, (categoria_id,))

    fila = cursor.fetchone()

    print(
        "[PUT] Después:",
        dict(fila) if fila else None
    )

    conexion.close()

    return {
        "mensaje": "Categoria actualizada",
        "categoria": dict(fila),
        "actualizado_por": usuario["username"]
    }


@router.delete("/{categoria_id}")
def eliminar_categoria(
    categoria_id: int,
    admin: dict = Depends(seguridad.requerir_admin)
):
    conexion = db.obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM Producto
        WHERE id_categoria = ?
    """, (categoria_id,))

    cantidad_productos = cursor.fetchone()[0]

    if cantidad_productos > 0:
        conexion.close()

        raise HTTPException(
            status_code=400,
            detail="No se puede eliminar la categoria porque tiene productos asociados"
        )

    cursor.execute("""
        DELETE FROM Categoria
        WHERE id = ?
    """, (categoria_id,))

    conexion.commit()

    if cursor.rowcount == 0:
        conexion.close()

        raise HTTPException(
            status_code=404,
            detail="Categoria no encontrada"
        )

    conexion.close()

    return {
        "mensaje": "Categoria eliminada",
        "categoria_id": categoria_id,
        "eliminado_por": admin["username"]
    }


@router.get("/{categoria_id}/productos")
def obtener_productos_categoria(categoria_id: int):
    conexion = db.obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT *
        FROM Categoria
        WHERE id = ?
    """, (categoria_id,))

    categoria = cursor.fetchone()

    if categoria is None:
        conexion.close()

        raise HTTPException(
            status_code=404,
            detail="Categoria no encontrada"
        )

    cursor.execute("""
        SELECT
            p.id,
            p.nombre,
            p.precio,
            p.id_categoria,
            p.id_proveedor,
            pr.nombre AS proveedor
        FROM Producto p
        JOIN Proveedor pr
            ON p.id_proveedor = pr.id
        WHERE p.id_categoria = ?
    """, (categoria_id,))

    productos = [dict(fila) for fila in cursor.fetchall()]

    conexion.close()

    return {
        "id": categoria["id"],
        "nombre": categoria["nombre"],
        "productos": productos
    }