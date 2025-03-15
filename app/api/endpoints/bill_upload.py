from fastapi import APIRouter, HTTPException
from app.schemas.user_schema import UserSchema
from app.services.ollama.handler import LLMHandler
from app.services.ollama.prompts import prompts
from app.core.config import settings
from app.services.mongo.user import insert_or_update_user
from app.utils import extract_text_from_pdf_url_ocr


router = APIRouter(prefix="/bill", tags=["bill"])

@router.post("/upload-url")
async def get_bill_details(payload: dict):
    """
    Fetch a PDF bill from a URL provided in the payload, extract text using OCR, and obtain user details via LLM.
    \nexpected payload:
    { "bill_url": "https://xkeittwiexfgxxkllbck.supabase.co/storage/v1/object/public/bills//sample_bill.pdf", "email": "kapeeshkaul@gmail.com" }
    """
    bill_url = payload.get("bill_url")
    if not bill_url or not bill_url.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Invalid URL. Only URLs pointing to PDF files are allowed.")
    email = payload.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="Email is required.")

    pdf_text = extract_text_from_pdf_url_ocr(bill_url)

    handler = LLMHandler(model=settings.OLLAMA_MODEL)

    user_details = handler.run_prompt(
        prompts.extract_details,
        pdf_text
    )

    user_details['email'] = email
    user_details['bill_url'] = bill_url

    try:
        user_details = UserSchema(**user_details)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid user details: {e}")

    insert_id = await insert_or_update_user(user_details)
    return {
        "_id": insert_id,
        "user_details": user_details.model_dump()
    }
