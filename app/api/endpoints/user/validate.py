from fastapi import APIRouter, HTTPException
from app.services.mongo.user import verify_user

router = APIRouter(prefix="/user", tags=["user"])

@router.post("/validate")
async def validate_user_endpoint(user_id: str):
    """
    Validate a user by ID.
    """
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required.")

    result = await verify_user(user_id)
    if not result:
        raise HTTPException(status_code=500, detail="Failed to validate user.")
    
    return {"message": "User validated successfully."}
