from fastapi import APIRouter, HTTPException
from app.services.mongo.user import moderate_user
from fastapi import APIRouter, HTTPException, Request

router = APIRouter(prefix="/admin", tags=["admin"])

@router.post("/moderate")
async def moderate_user_endpoint(request: dict):
    """
    moderate a user by ID.
    \nExpected payload:
    {
        "user_id": "user_id",
        "accepted": true
    }
    """
    # body = await request.json()
    user_id = request.get("user_id")
    accepted = request.get("accepted")

    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required.")
    if accepted is None:
        raise HTTPException(status_code=400, detail="Accepted status is required.")

    result = await moderate_user(user_id, accepted)
    if not result:
        raise HTTPException(status_code=500, detail="Failed to moderate user.")
    
    return {"message": "User moderated successfully."}
