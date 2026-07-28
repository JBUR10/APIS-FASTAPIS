from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/categorias", tags=["Categorias"])

class CategoriaEntrada(BaseModel):
    nombre: str

categorias = [
    {"id": 1, "nombre": "Perifericos"},
    {"id": 2, "nombre": "Pantallas"},
    {"id": 3, "nombre": "Audio"},
]

@router.get("")
def listar_categorias():
    return categorias

@router.get("/{categoria_id}")
def obtener_categoria(categoria_id: int):
    for categoria in categorias:
        if categoria["id"] == categoria_id:
            return categoria
    raise HTTPException(status_code=404, detail="Categoria no encontrada")

@router.post("", status_code=201)
def crear_categoria(datos: CategoriaEntrada):
    nuevo_id = max((c["id"] for c in categorias), default=0) + 1
    nueva = {
        "id": nuevo_id,
        "nombre": datos.nombre
    }
    categorias.append(nueva)
    return {"mensaje": "Categoria creada", "categoria": nueva}

@router.put("/{categoria_id}")
def actualizar_categoria(categoria_id: int, datos: CategoriaEntrada):
    for categoria in categorias:
        if categoria["id"] == categoria_id:
            categoria["nombre"] = datos.nombre
            return {"mensaje": "Categoria actualizada", "categoria": categoria}
    raise HTTPException(status_code=404, detail="Categoria no encontrada")

@router.delete("/{categoria_id}")
def eliminar_categoria(categoria_id: int):
    for categoria in categorias:
        if categoria["id"] == categoria_id:
            categorias.remove(categoria)
            return {"mensaje": "Categoria eliminada", "categoria": categoria}
    raise HTTPException(status_code=404, detail="Categoria no encontrada")