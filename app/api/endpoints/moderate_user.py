from fastapi import APIRouter, HTTPException
from app.services.mongo.user import moderate_user

router = APIRouter(prefix="/admin", tags=["admin"])

@router.post("/moderate")
async def moderate_user_endpoint(user_id: str):
    """
    moderate a user by ID.
    """
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required.")

    result = await moderate_user(user_id)
    if not result:
        raise HTTPException(status_code=500, detail="Failed to moderate user.")
    
    return {"message": "User moderated successfully."}
