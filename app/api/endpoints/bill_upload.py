from fastapi import APIRouter, HTTPException
from app.schemas.user_schema import UserSchema
from app.services.ollama.handler import LLMHandler
from app.services.ollama.prompts import prompts
from app.core.config import settings
from app.services.mongo.user import insert_user
from app.utils import extract_text_from_pdf_url_ocr


router = APIRouter(prefix="/bill", tags=["bill"])

@router.post("/upload-url")
async def get_bill_details(pdf_url: str):
    """
    Fetch a PDF bill from a URL, extract text using OCR, and obtain user details via LLM.
    """
    if not pdf_url.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Invalid URL. Only URLs pointing to PDF files are allowed.")

    pdf_text = extract_text_from_pdf_url_ocr(pdf_url)

    handler = LLMHandler(model=settings.OLLAMA_MODEL)

    user_details = handler.run_prompt(
        prompts.extract_details,
        pdf_text
    )

    try:
        user_details = UserSchema(**user_details)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid user details: {e}")

    # insert_id = await insert_user(user_details)
    # if not insert_id:
    #     raise HTTPException(status_code=500, detail="Failed to insert user details into the database.")
    insert_id = await insert_user(user_details)
    return {
        "insert_id": insert_id,
        "user_details": user_details.model_dump()
    }
