from app.schemas.user_schema import UserSchema
from app.utils.db import get_db
from logging import getLogger
from bson import ObjectId
from app.schemas.user_schema import ModerationStatus
from pydantic import BaseModel
from datetime import datetime
from app.core.config import settings

logger = getLogger(__name__)

class ValidatePayload(BaseModel):
    user_id: str
    name: str
    address: str
    satellite_image_url: str
    area_square_feet: int
    latitude: float
    longitude: float

class ProcessedImageSchema(BaseModel):
    user_id: str
    original_url: str
    processed_url: str
    highlighted_percentage: float
    timestamp: datetime = datetime.now()

async def insert_or_update_user(user: UserSchema):
    db = await get_db()
    user_dict = user.model_dump()  # Ensure Pydantic v2, else use .dict()
    try:
        result = await db["users"].update_one(
            {"email": user.email},
            {"$set": user_dict},
            upsert=True
        )
        if result.upserted_id:
            logger.info(f"User inserted with ID: {result.upserted_id}")
            return str(result.upserted_id)
        elif result.modified_count > 0:
            logger.info(f"User with email {user.email} updated.")
            updated_user = await db["users"].find_one({"email": user.email})
            return str(updated_user["_id"])
        else:
            logger.error("Failed to insert or update user in the database.")
            raise Exception("User insertion or update was not acknowledged")
    except Exception as e:
        logger.exception(f"Insertion or update error: {e}")
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

async def verify_user(payload: ValidatePayload):
    db = await get_db()
    try:
        result = await db["users"].update_one(
            {"_id": ObjectId(payload.user_id)}, {
                "$set": {
                    "verified": True,
                    "name": payload.name,
                    "address": payload.address,
                    "satellite_image_url": payload.satellite_image_url,
                    "area_square_feet": payload.area_square_feet,
                    "coordinates": [payload.latitude, payload.longitude],
                }
            }
        )
        if result.modified_count == 0:
            logger.error(f"No document updated for user ID {payload.user_id}.")
            return False
        logger.info(f"User with ID {payload.user_id} has been verified.")
        return True
    except Exception as e:
        logger.exception(f"Verification update error: {e}")
        raise

async def moderate_user(user_id: str, accepted: bool = True) -> bool:
    db = await get_db()
    try:
        if not accepted:
            moderation_status = ModerationStatus.rejected
        else:
            moderation_status = ModerationStatus.accepted
        result = await db["users"].update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"moderation_status": moderation_status}}
        )      
        if result.modified_count == 0:
            logger.error(f"No document updated for user ID {user_id}.")
            return False
        logger.info(f"User with ID {user_id} has been moderated.")
        return True
    except Exception as e:
        logger.exception(f"Moderation update error: {e}")
        raise

async def get_all_users():
    db = await get_db()
    try:
        users = await db["users"].find().to_list(length=None)
        if not users:
            logger.warning("No users found in the database.")
            return []
        for user in users:
            user["_id"] = str(user["_id"])  # convert ObjectId to str for schema compatibility
        logger.info(f"Total users fetched: {len(users)}")
        return [{"_id": user["_id"], **UserSchema(**user).model_dump()} for user in users]
    except Exception as e:
        logger.exception(f"Fetching all users error: {e}")
        raise

async def get_by_moderation_status(moderation_status: ModerationStatus):
    db = await get_db()
    try:
        users = await db["users"].find({"moderation_status": moderation_status.value}).to_list(length=None)
        if not users:
            logger.warning(f"No users found with moderation status {moderation_status}.")
            return []
        for user in users:
            user["_id"] = str(user["_id"])  # convert ObjectId to str for schema compatibility
        logger.info(f"Total users with moderation status {moderation_status}: {len(users)}")
        return [{"_id": user["_id"], **UserSchema(**user).model_dump()} for user in users]
    except Exception as e:
        logger.exception(f"Fetching users by moderation status error: {e}")
        raise