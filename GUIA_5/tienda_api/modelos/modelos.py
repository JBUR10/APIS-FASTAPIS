from pydantic import BaseModel

class ProductoEntrada(BaseModel):
    nombre: str
    precio: float
    id_categoria: int
    id_proveedor: int

    