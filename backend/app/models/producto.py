from pydantic import BaseModel, Field


class Producto(BaseModel):

    nombre: str

    descripcion: str

    precio: float = Field(ge=0)

    categoria: str

    stock: int = Field(ge=0)

    imagen: str = ""