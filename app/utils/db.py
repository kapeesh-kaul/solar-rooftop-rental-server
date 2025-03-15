from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

class MongoDB:
    client: AsyncIOMotorClient = None

db = MongoDB()

async def get_db():
    if db.client is None:
        db.client = AsyncIOMotorClient(settings.MONGO_URI)
    return db.client[settings.MONGO_DB_NAME]