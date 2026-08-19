import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URI")

client = AsyncIOMotorClient(MONGODB_URL)

database = client.ambiente502

productos_collection = database.productos
pedidos_collection = database.pedidos


async def test_connection():
    try:
        await client.admin.command("ping")
        print("✅ Conexión exitosa con MongoDB Atlas")
    except Exception as e:
        print(f"❌ Error en la conexión: {e}")