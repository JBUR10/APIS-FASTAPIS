from pydantic import BaseModel

class ProductoEntrada(BaseModel):
    nombre: str
    precio: float
    categoria: str
    proveedor: str