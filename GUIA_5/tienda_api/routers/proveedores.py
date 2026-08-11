from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import seguridad

router = APIRouter(prefix="/proveedores", tags=["Proveedores"])


class ProveedorEntrada(BaseModel):
    nombre: str
    telefono: str
    correo: str


proveedores = [
    {
        "id": 1,
        "nombre": "Manzana (Apol)",
        "telefono": "3001234567",
        "correo": "contacto@apol.com",
    },
    {
        "id": 2,
        "nombre": "Distribuciones Metrio",
        "telefono": "3109876543",
        "correo": "ventas@metrio.com",
    },
    {
        "id": 3,
        "nombre": "Flamingo",
        "telefono": "3204567890",
        "correo": "info@flamingo.com",
    },
]


@router.get("")
def listar_proveedores():
    return proveedores


@router.get("/{proveedor_id}")
def obtener_proveedor(proveedor_id: int):
    for proveedor in proveedores:
        if proveedor["id"] == proveedor_id:
            return proveedor

    raise HTTPException(status_code=404, detail="Proveedor no encontrado")


@router.post("", status_code=201)
def crear_proveedor(
    datos: ProveedorEntrada, usuario: dict = Depends(seguridad.obtener_usuario_actual)
):
    nuevo_id = max((p["id"] for p in proveedores), default=0) + 1

    nuevo = {
        "id": nuevo_id,
        "nombre": datos.nombre,
        "telefono": datos.telefono,
        "correo": datos.correo,
    }

    proveedores.append(nuevo)

    return {
        "mensaje": "Proveedor creado",
        "proveedor": nuevo,
        "creado_por": usuario["username"],
    }


@router.put("/{proveedor_id}")
def actualizar_proveedor(
    proveedor_id: int,
    datos: ProveedorEntrada,
    usuario: dict = Depends(seguridad.obtener_usuario_actual),
):
    for proveedor in proveedores:
        if proveedor["id"] == proveedor_id:
            proveedor["nombre"] = datos.nombre
            proveedor["telefono"] = datos.telefono
            proveedor["correo"] = datos.correo

            return {
                "mensaje": "Proveedor actualizado",
                "proveedor": proveedor,
                "actualizado_por": usuario["username"],
            }

    raise HTTPException(status_code=404, detail="Proveedor no encontrado")


@router.delete("/{proveedor_id}")
def eliminar_proveedor(
    proveedor_id: int, admin: dict = Depends(seguridad.requerir_admin)
):
    for proveedor in proveedores:
        if proveedor["id"] == proveedor_id:
            proveedores.remove(proveedor)

            return {
                "mensaje": "Proveedor eliminado",
                "proveedor": proveedor,
                "eliminado_por": admin["username"],
            }

    raise HTTPException(status_code=404, detail="Proveedor no encontrado")
