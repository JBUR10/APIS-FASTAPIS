from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

import seguridad
from database import db

router = APIRouter(prefix="/productos", tags=["Productos"])


class ProductoEntrada(BaseModel):
    nombre: str
    precio: float
    categoria_id: int


@router.get("")
def listar_productos():
    conexion = db.obtener_conexion()

    cursor = conexion.cursor()
    cursor.execute("""
        SELECT
            productos.id,
            productos.nombre,
            productos.precio,
            productos.categoria_id,
            categorias.nombre AS categoria
        FROM productos
        JOIN categorias
            ON productos.categoria_id = categorias.id
    """)

    filas = cursor.fetchall()

    conexion.close()

    return [dict(fila) for fila in filas]


@router.get("/{producto_id}")
def obtener_producto(producto_id: int):
    conexion = db.obtener_conexion()

    cursor = conexion.cursor()
    cursor.execute(
        """
        SELECT
            productos.id,
            productos.nombre,
            productos.precio,
            productos.categoria_id,
            categorias.nombre AS categoria
        FROM productos
        JOIN categorias
            ON productos.categoria_id = categorias.id
        WHERE productos.id = ?
    """,
        (producto_id,),
    )

    fila = cursor.fetchone()

    conexion.close()

    if fila is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    return dict(fila)


@router.post("", status_code=201)
def crear_producto(
    datos: ProductoEntrada, usuario: dict = Depends(seguridad.obtener_usuario_actual)
):
    conexion = db.obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("SELECT id FROM categorias WHERE id = ?", (datos.categoria_id,))

    categoria = cursor.fetchone()

    if categoria is None:
        conexion.close()

        raise HTTPException(status_code=400, detail="La categoría no existe")

    cursor.execute(
        """
        INSERT INTO productos (nombre, precio, categoria_id)
        VALUES (?, ?, ?)
    """,
        (datos.nombre, datos.precio, datos.categoria_id),
    )

    conexion.commit()

    nuevo_id = cursor.lastrowid

    cursor.execute(
        """
        SELECT
            productos.id,
            productos.nombre,
            productos.precio,
            productos.categoria_id,
            categorias.nombre AS categoria
        FROM productos
        JOIN categorias
            ON productos.categoria_id = categorias.id
        WHERE productos.id = ?
    """,
        (nuevo_id,),
    )

    fila = cursor.fetchone()

    conexion.close()

    return {
        "mensaje": "Producto creado",
        "producto": dict(fila),
        "creado_por": usuario["username"],
    }


@router.put("/{producto_id}")
def actualizar_producto(
    producto_id: int,
    datos: ProductoEntrada,
    usuario: dict = Depends(seguridad.obtener_usuario_actual),
):
    conexion = db.obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("SELECT id FROM categorias WHERE id = ?", (datos.categoria_id,))

    categoria = cursor.fetchone()

    if categoria is None:
        conexion.close()

        raise HTTPException(status_code=400, detail="La categoría no existe")

    cursor.execute(
        """
        UPDATE productos
        SET nombre = ?,
            precio = ?,
            categoria_id = ?
        WHERE id = ?
    """,
        (datos.nombre, datos.precio, datos.categoria_id, producto_id),
    )

    conexion.commit()

    filas_modificadas = cursor.rowcount

    if filas_modificadas == 0:
        conexion.close()

        raise HTTPException(status_code=404, detail="Producto no encontrado")

    cursor.execute(
        """
        SELECT
            productos.id,
            productos.nombre,
            productos.precio,
            productos.categoria_id,
            categorias.nombre AS categoria
        FROM productos
        JOIN categorias
            ON productos.categoria_id = categorias.id
        WHERE productos.id = ?
    """,
        (producto_id,),
    )

    fila = cursor.fetchone()

    conexion.close()

    return {
        "mensaje": "Producto actualizado",
        "producto": dict(fila),
        "actualizado_por": usuario["username"],
    }


@router.delete("/{producto_id}")
def eliminar_producto(
    producto_id: int, admin: dict = Depends(seguridad.requerir_admin)
):
    conexion = db.obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("DELETE FROM productos WHERE id = ?", (producto_id,))

    conexion.commit()

    filas_eliminadas = cursor.rowcount

    if filas_eliminadas == 0:
        conexion.close()

        raise HTTPException(status_code=404, detail="Producto no encontrado")

    conexion.close()

    return {
        "mensaje": "Producto eliminado",
        "producto_id": producto_id,
        "eliminado_por": admin["username"],
    }
