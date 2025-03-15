from fastapi import APIRouter, HTTPException
from app.schemas.user_schema import UserSchema, ModerationStatus
from app.services.mongo.user import get_user_by_id, get_all_users, get_by_moderation_status

router = APIRouter(prefix="/user", tags=["user"])

@router.get("/get_by_id")
async def get_user_by_id_endpoint(user_id: str):
    """
    Get user details by ID.
    """
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required.")

    user = await get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    
    return {"user": user}

@router.get("/get_all")
async def get_all_users_endpoint():
    """
    Get all users.
    """
    users = await get_all_users()
    if not users:
        raise HTTPException(status_code=404, detail="No users found.")
    
    return {"users": users}

@router.get("/get_by_modearation_status")
async def get_user_by_moderation_status_endpoint(moderation_status: ModerationStatus):
    """
    Get users by moderation status.
    """
    if not moderation_status:
        raise HTTPException(status_code=400, detail="Moderation status is required.")

    users = await get_by_moderation_status(moderation_status)
    if not users:
        raise HTTPException(status_code=404, detail="No users found with the specified moderation status.")
    
    return {"users": users}
