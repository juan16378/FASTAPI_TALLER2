from pydantic import BaseModel, Field
from typing import List


class ProductoPedido(BaseModel):
    producto_id: str
    cantidad: int = Field(gt=0)


class Pedido(BaseModel):
    cliente: str
    productos: List[ProductoPedido]
    total: float = Field(ge=0)