from app.schemas.user_schema import UserSchema
from app.utils.db import get_db
from logging import getLogger
from bson import ObjectId

logger = getLogger(__name__)

async def insert_user(user: UserSchema):
    db = await get_db()
    user_dict = user.model_dump()  # Ensure Pydantic v2, else use .dict()
    try:
        result = await db["users"].insert_one(user_dict)
        if not result.acknowledged:
            logger.error("Failed to insert user into the database.")
            raise Exception("User insertion was not acknowledged")
        logger.info(f"User inserted with ID: {result.inserted_id}")
        return str(result.inserted_id)
    except Exception as e:
        logger.exception(f"Insertion error: {e}")
        raise

async def get_user_by_id(user_id: str):
    db = await get_db()
    try:
        user = await db["users"].find_one({"_id": ObjectId(user_id)})
        if not user:
            logger.warning(f"User with ID {user_id} not found.")
            return None
        logger.info(f"User found: {user}")
        user["_id"] = str(user["_id"])  # convert ObjectId to str for schema compatibility
        return UserSchema(**user)
    except Exception as e:
        logger.exception(f"Fetching user error: {e}")
        raise

async def verify_user(user_id: str):
    db = await get_db()
    try:
        result = await db["users"].update_one({"_id": ObjectId(user_id)}, {"$set": {"verified": True}})
        if result.modified_count == 0:
            logger.error(f"No document updated for user ID {user_id}.")
            return False
        logger.info(f"User with ID {user_id} has been verified.")
        return True
    except Exception as e:
        logger.exception(f"Verification update error: {e}")
        raise

async def moderate_user(user_id: str):
    db = await get_db()
    try:
        result = await db["users"].update_one({"_id": ObjectId(user_id)}, {"$set": {"moderated": True}})
        if result.modified_count == 0:
            logger.error(f"No document updated for user ID {user_id}.")
            return False
        logger.info(f"User with ID {user_id} has been moderated.")
        return True
    except Exception as e:
        logger.exception(f"Moderation update error: {e}")
        raise
