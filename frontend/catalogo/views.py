import json

import requests

from django.shortcuts import render, redirect


API_URL = "http://127.0.0.1:8000"


def productos(request):

    productos_data = []

    error = None


    try:

        respuesta = requests.get(
            f"{API_URL}/productos/",
            timeout=5
        )


        if respuesta.status_code == 200:

            productos_data = respuesta.json()

        else:

            error = (
                "No fue posible obtener "
                "los productos desde la API."
            )


    except requests.exceptions.RequestException:

        error = (
            "No se pudo conectar con la API. "
            "Verifica que FastAPI esté ejecutándose."
        )


    return render(
        request,
        "catalogo/productos.html",
        {
            "productos": productos_data,
            "error": error,
        },
    )


def checkout(request):

    return render(
        request,
        "catalogo/checkout.html"
    )


def crear_pedido(request):

    if request.method != "POST":

        return redirect("productos")


    try:

        nombre_completo = request.POST.get(
            "nombre_completo"
        )

        cedula = request.POST.get(
            "cedula"
        )

        celular = request.POST.get(
            "celular"
        )

        correo = request.POST.get(
            "correo"
        )

        direccion = request.POST.get(
            "direccion"
        )

        ciudad = request.POST.get(
            "ciudad"
        )

        notas = request.POST.get(
            "notas",
            ""
        )


        productos = json.loads(
            request.POST.get(
                "productos",
                "[]"
            )
        )


        total = float(
            request.POST.get(
                "total",
                0
            )
        )


        pedido = {

            "nombre_completo":
                nombre_completo,

            "cedula":
                cedula,

            "celular":
                celular,

            "correo":
                correo,

            "direccion":
                direccion,

            "ciudad":
                ciudad,

            "notas":
                notas,

            "productos":
                productos,

            "total":
                total

        }


        respuesta = requests.post(

            f"{API_URL}/pedidos/",

            json=pedido,

            timeout=10

        )


        if respuesta.status_code in [200, 201]:

            resultado = respuesta.json()


            return render(

                request,

                "catalogo/pedido_exitoso.html",

                {

                    "pedido": {

                        "id":
                            resultado.get("id"),

                        "total":
                            total

                    }

                }

            )


        return render(

            request,

            "catalogo/checkout.html",

            {

                "error":
                    "No fue posible registrar "
                    "el pedido."

            }

        )


    except (
        ValueError,
        json.JSONDecodeError,
        requests.exceptions.RequestException
    ):

        return render(

            request,

            "catalogo/checkout.html",

            {

                "error":
                    "Ocurrió un error al "
                    "procesar el pedido."

            }

        )