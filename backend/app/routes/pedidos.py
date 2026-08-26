from fastapi import APIRouter

from app.database import pedidos_collection

from app.models.pedido import Pedido


router = APIRouter(
    prefix="/pedidos",
    tags=["Pedidos"]
)


@router.post("/")
async def crear_pedido(pedido: Pedido):

    resultado = await pedidos_collection.insert_one(
        pedido.model_dump()
    )

    return {

        "mensaje":
            "Pedido registrado correctamente",

        "id":
            str(resultado.inserted_id)

    }


@router.get("/")
async def obtener_pedidos():

    pedidos = pedidos_collection.find()

    resultado = []


    async for pedido in pedidos:

        resultado.append({

            "id":
                str(pedido["_id"]),

            "nombre_completo":
                pedido["nombre_completo"],

            "cedula":
                pedido["cedula"],

            "celular":
                pedido["celular"],

            "correo":
                pedido["correo"],

            "direccion":
                pedido["direccion"],

            "ciudad":
                pedido["ciudad"],

            "notas":
                pedido.get("notas", ""),

            "productos":
                pedido["productos"],

            "total":
                pedido["total"]

        })


    return resultado