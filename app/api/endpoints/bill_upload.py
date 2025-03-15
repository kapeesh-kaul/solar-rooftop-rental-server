from fastapi import APIRouter, UploadFile, File, HTTPException
from app.schemas.user_schema import UserSchema
from app.services.ollama.handler import LLMHandler
from app.services.ollama.prompts import prompts
from app.core.config import settings
import PyPDF2

router = APIRouter(prefix="/bill", tags=["bill"])

def extract_text_from_pdf(file: UploadFile) -> str:
    """"
    "Extract text from a PDF file."
    """
    pdf_reader = PyPDF2.PdfReader(file.file)
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text

@router.post("/upload")
async def upload_bill(file: UploadFile = File(...)):
    """
    Upload a PDF bill and extract user details.
    This endpoint accepts a PDF file, extracts text from it, and uses an LLM to extract user details from the text.
    The extracted details are returned in JSON format.    
    """
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF files are allowed.")
    
    pdf_text = extract_text_from_pdf(file)

    handler = LLMHandler(model=settings.OLLAMA_MODEL)
    
    user_details = handler.run_prompt(
        prompts.extract_details, 
        pdf_text
    )

    # Validate the extracted user details against the UserSchema
    try:
        user_details = UserSchema(**user_details)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid user details: {e}")
    
    return user_details
