from fastapi import APIRouter

router = APIRouter(
    prefix="/categorias",
    tags=["Categorias"]
)

categorias = [
    {
        "id": 1,
        "nombre": "Perifericos"
    },
    {
        "id": 2,
        "nombre": "Pantallas"
    }
]


@router.get("")
def listar_categorias():
    return categorias