from fastapi import APIRouter, HTTPException, Request
from app.schemas.user_schema import ModerationStatus
from app.services.mongo.user import get_user_by_id, get_all_users, get_by_moderation_status

router = APIRouter(prefix="/user", tags=["user"])

@router.post("/get_by_id")
async def get_user_by_id_endpoint(payload: dict):
    """
    Get user details by ID.
    \nExample payload:
    {
        "user_id": "1234567890abcdef"
    }
    """
    user_id = payload.get("user_id")
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

@router.post("/get_by_moderation_status")
async def get_user_by_moderation_status_endpoint(payload: dict):
    """
    Get users by moderation status.
    \nExample payload:
    {
        "moderation_status": "approved"
    }
    """
    moderation_status = payload.get("moderation_status")
    if not moderation_status:
        raise HTTPException(status_code=400, detail="Moderation status is required.")

    users = await get_by_moderation_status(moderation_status)
    if not users:
        raise HTTPException(status_code=404, detail="No users found with the specified moderation status.")
    
    return {"users": users}
