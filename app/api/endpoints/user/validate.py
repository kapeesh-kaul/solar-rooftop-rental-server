from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.mongo.user import verify_user
from bson import ObjectId

router = APIRouter(prefix="/user", tags=["user"])

from app.services.mongo.user import ValidatePayload

@router.post("/validate")
async def validate_user_endpoint(payload : ValidatePayload):
    """
    Validate a user by ID.
    \nExample payload:
    {
        "user_id": "67d5e2ebae111aed46b77428",
        "name": "John Doe",
        "address": "123 Solar Street, CA",
        "satellite_image_url": "https://example.com/path/to/image.jpg",
        "area_square_feet": 1500,
        "latitude": 37.7749,
        "longitude": -122.4194,
    }
    """
    if not ObjectId.is_valid(payload.user_id):
        raise HTTPException(status_code=400, detail="Invalid user ID format.")

    result = await verify_user(payload)
    if not result:
        raise HTTPException(status_code=500, detail="Failed to validate user.")
    
    return {"message": "User validated successfully."}
