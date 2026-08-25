https://fastapi-taller2-kqhc.onrender.com/
# 🛍️ Proyecto Tienda - FASTAPI_TALLER2

Aplicación web para la gestión de una tienda en línea, desarrollada utilizando **FastAPI, Django, React y MongoDB**.

El proyecto permite gestionar productos, consultar el catálogo, administrar el stock y realizar pedidos mediante una API REST conectada a MongoDB.

---

## 📌 Tecnologías utilizadas

### Backend

- 🐍 Python
- ⚡ FastAPI
- 🚀 Uvicorn
- 🍃 MongoDB
- 🔗 PyMongo
- 📦 Pydantic

### Frontend

- ⚛️ React
- 🎨 Tailwind CSS
- 🌐 Django
- HTML5
- CSS3
- JavaScript

### Herramientas

- Git
- GitHub
- Postman
- MongoDB Atlas
- Visual Studio Code

---

# 📁 Estructura del proyecto

```text
proyecto-tienda/
│
├── backend/
│   │
│   ├── app/
│   │   ├── routes/
│   │   │   ├── productos.py
│   │   │   └── pedidos.py
│   │   │
│   │   ├── models/
│   │   │   ├── producto.py
│   │   │   └── pedido.py
│   │   │
│   │   ├── database.py
│   │   └── main.py
│   │
│   ├── .env
│   ├── requirements.txt
│   └── ...
│
├── frontend/
│   │
│   ├── src/
│   │   ├── components/
│   │   │   ├── ProductCard.jsx
│   │   │   └── ...
│   │   │
│   │   ├── pages/
│   │   │   ├── Productos.jsx
│   │   │   ├── Login.jsx
│   │   │   └── ...
│   │   │
│   │   └── App.jsx
│   │
│   ├── public/
│   ├── package.json
│   └── ...
│
├── manage.py
├── requirements.txt
└── README.md