from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

import seguridad
from database import db

router = APIRouter(prefix="/productos", tags=["Productos"])


class ProductoEntrada(BaseModel):
    nombre: str
    precio: float
    id_categoria: int
    id_proveedor: int


@router.get("")
def listar_productos():
    conexion = db.obtener_conexion()

    cursor = conexion.cursor()
    cursor.execute("""
        SELECT
            p.id,
            p.nombre,
            p.precio,
            p.id_categoria,
            c.nombre AS categoria,
            p.id_proveedor,
            pr.nombre AS proveedor
        FROM Producto p
        JOIN Categoria c
            ON p.id_categoria = c.id
        JOIN Proveedor pr
            ON p.id_proveedor = pr.id
    """)

    filas = cursor.fetchall()

    conexion.close()

    return [dict(fila) for fila in filas]


@router.get("/{producto_id}")
def obtener_producto(producto_id: int):
    conexion = db.obtener_conexion()

    cursor = conexion.cursor()
    cursor.execute("""
        SELECT
            p.id,
            p.nombre,
            p.precio,
            p.id_categoria,
            c.nombre AS categoria,
            p.id_proveedor,
            pr.nombre AS proveedor
        FROM Producto p
        JOIN Categoria c
            ON p.id_categoria = c.id
        JOIN Proveedor pr
            ON p.id_proveedor = pr.id
        WHERE p.id = ?
    """, (producto_id,))

    fila = cursor.fetchone()

    conexion.close()

    if fila is None:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )

    return dict(fila)


@router.post("", status_code=201)
def crear_producto(
    datos: ProductoEntrada,
    usuario: dict = Depends(seguridad.obtener_usuario_actual)
):
    conexion = db.obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        "SELECT id FROM Categoria WHERE id = ?",
        (datos.id_categoria,)
    )

    categoria = cursor.fetchone()

    if categoria is None:
        conexion.close()

        raise HTTPException(
            status_code=400,
            detail="La categoría no existe"
        )

    cursor.execute(
        "SELECT id FROM Proveedor WHERE id = ?",
        (datos.id_proveedor,)
    )

    proveedor = cursor.fetchone()

    if proveedor is None:
        conexion.close()

        raise HTTPException(
            status_code=400,
            detail="El proveedor no existe"
        )

    cursor.execute("""
        INSERT INTO Producto
        (nombre, precio, id_categoria, id_proveedor)
        VALUES (?, ?, ?, ?)
    """, (
        datos.nombre,
        datos.precio,
        datos.id_categoria,
        datos.id_proveedor
    ))

    conexion.commit()

    nuevo_id = cursor.lastrowid

    cursor.execute("""
        SELECT
            p.id,
            p.nombre,
            p.precio,
            p.id_categoria,
            c.nombre AS categoria,
            p.id_proveedor,
            pr.nombre AS proveedor
        FROM Producto p
        JOIN Categoria c
            ON p.id_categoria = c.id
        JOIN Proveedor pr
            ON p.id_proveedor = pr.id
        WHERE p.id = ?
    """, (nuevo_id,))

    fila = cursor.fetchone()

    conexion.close()

    return {
        "mensaje": "Producto creado",
        "producto": dict(fila),
        "creado_por": usuario["username"]
    }


@router.put("/{producto_id}")
def actualizar_producto(
    producto_id: int,
    datos: ProductoEntrada,
    usuario: dict = Depends(seguridad.obtener_usuario_actual)
):
    conexion = db.obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        "SELECT id FROM Categoria WHERE id = ?",
        (datos.id_categoria,)
    )

    if cursor.fetchone() is None:
        conexion.close()

        raise HTTPException(
            status_code=400,
            detail="La categoría no existe"
        )

    cursor.execute(
        "SELECT id FROM Proveedor WHERE id = ?",
        (datos.id_proveedor,)
    )

    if cursor.fetchone() is None:
        conexion.close()

        raise HTTPException(
            status_code=400,
            detail="El proveedor no existe"
        )

    cursor.execute("""
        UPDATE Producto
        SET nombre = ?,
            precio = ?,
            id_categoria = ?,
            id_proveedor = ?
        WHERE id = ?
    """, (
        datos.nombre,
        datos.precio,
        datos.id_categoria,
        datos.id_proveedor,
        producto_id
    ))

    conexion.commit()

    if cursor.rowcount == 0:
        conexion.close()

        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )

    cursor.execute("""
        SELECT
            p.id,
            p.nombre,
            p.precio,
            p.id_categoria,
            c.nombre AS categoria,
            p.id_proveedor,
            pr.nombre AS proveedor
        FROM Producto p
        JOIN Categoria c
            ON p.id_categoria = c.id
        JOIN Proveedor pr
            ON p.id_proveedor = pr.id
        WHERE p.id = ?
    """, (producto_id,))

    fila = cursor.fetchone()

    conexion.close()

    return {
        "mensaje": "Producto actualizado",
        "producto": dict(fila),
        "actualizado_por": usuario["username"]
    }


@router.delete("/{producto_id}")
def eliminar_producto(
    producto_id: int,
    admin: dict = Depends(seguridad.requerir_admin)
):
    conexion = db.obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        "DELETE FROM Producto WHERE id = ?",
        (producto_id,)
    )

    conexion.commit()

    if cursor.rowcount == 0:
        conexion.close()

        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )

    conexion.close()

    return {
        "mensaje": "Producto eliminado",
        "producto_id": producto_id,
        "eliminado_por": admin["username"]
    }