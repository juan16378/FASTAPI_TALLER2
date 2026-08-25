import requests

from django.shortcuts import render


API_URL = "http://127.0.0.1:8000/productos/"


def productos(request):
    productos_data = []
    error = None

    try:
        respuesta = requests.get(
            API_URL,
            timeout=10
        )

        print("STATUS FASTAPI:", respuesta.status_code)
        print("RESPUESTA FASTAPI:", respuesta.text)

        if respuesta.status_code == 200:
            productos_data = respuesta.json()
        else:
            error = (
                f"La API respondió con código "
                f"{respuesta.status_code}"
            )

    except requests.exceptions.RequestException as e:
        print("ERROR CONECTANDO CON FASTAPI:", e)

        error = f"Error de conexión: {e}"

    return render(
        request,
        "catalogo/productos.html",
        {
            "productos": productos_data,
            "error": error,
        },
    )