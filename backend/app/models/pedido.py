from pydantic import BaseModel, Field

from typing import List


class ProductoPedido(BaseModel):

    producto_id: str

    cantidad: int = Field(gt=0)


class Pedido(BaseModel):

    nombre_completo: str = Field(
        min_length=3,
        max_length=100
    )

    cedula: str = Field(
        min_length=5,
        max_length=20
    )

    celular: str = Field(
        min_length=7,
        max_length=20
    )

    correo: str = Field(
        min_length=5,
        max_length=120
    )

    direccion: str = Field(
        min_length=5,
        max_length=200
    )

    ciudad: str = Field(
        min_length=2,
        max_length=80
    )

    notas: str = ""

    productos: List[ProductoPedido]

    total: float = Field(ge=0)