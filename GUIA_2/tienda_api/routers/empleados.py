from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/empleados", tags=["Empleados"])

class EmpleadoEntrada(BaseModel):
    nombre: str
    cargo: str
    salario: float

empleados = [
    {"id": 1, "nombre": "Sergio López", "cargo": "Administrador", "salario": 3500000},
    {"id": 2, "nombre": "Sebastian Ramirez", "cargo": "Vendedor", "salario": 1800000},
    {"id": 3, "nombre": "David Rosales", "cargo": "Cajero", "salario": 1600000},
]

@router.get("")
def listar_empleados():
    return empleados

@router.get("/{empleado_id}")
def obtener_empleado(empleado_id: int):
    for empleado in empleados:
        if empleado["id"] == empleado_id:
            return empleado
    raise HTTPException(status_code=404, detail="Empleado no encontrado")

@router.post("", status_code=201)
def crear_empleado(datos: EmpleadoEntrada):
    nuevo_id = max((e["id"] for e in empleados), default=0) + 1
    nuevo = {
        "id": nuevo_id,
        "nombre": datos.nombre,
        "cargo": datos.cargo,
        "salario": datos.salario
    }
    empleados.append(nuevo)
    return {"mensaje": "Empleado creado", "empleado": nuevo}

@router.put("/{empleado_id}")
def actualizar_empleado(empleado_id: int, datos: EmpleadoEntrada):
    for empleado in empleados:
        if empleado["id"] == empleado_id:
            empleado["nombre"] = datos.nombre
            empleado["cargo"] = datos.cargo
            empleado["salario"] = datos.salario
            return {"mensaje": "Empleado actualizado", "empleado": empleado}
    raise HTTPException(status_code=404, detail="Empleado no encontrado")

@router.delete("/{empleado_id}")
def eliminar_empleado(empleado_id: int):
    for empleado in empleados:
        if empleado["id"] == empleado_id:
            empleados.remove(empleado)
            return {"mensaje": "Empleado eliminado", "empleado": empleado}
    raise HTTPException(status_code=404, detail="Empleado no encontrado")