from fastapi import APIRouter, HTTPException
from app.schemas.user_schema import UserSchema
from app.services.mongo.user import get_user_by_id

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