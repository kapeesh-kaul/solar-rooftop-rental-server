from fastapi import APIRouter, UploadFile, File
from app.schemas.user_schema import UserSchema
from app.services.ollama_service import extract_user_details_from_bill

router = APIRouter(prefix="/bill", tags=["bill"])

@router.post("/upload")
async def upload_bill(file: UploadFile = File(...)):
    user_details = await extract_user_details_from_bill(file)
    return {"status": "success", "user": user_details}
