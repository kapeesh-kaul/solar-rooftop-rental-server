import requests
from fastapi import HTTPException
from io import BytesIO
import fitz
import pytesseract
from PIL import Image

def extract_text_from_pdf_url_ocr(pdf_url: str) -> str:
    """
    Extract text from a PDF file fetched via URL using OCR.
    """
    response = requests.get(pdf_url)

    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to download PDF from URL.")

    pdf_bytes = BytesIO(response.content)
    pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")

    full_text = ""

    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        pix = page.get_pixmap(dpi=300)
        
        img_bytes = pix.tobytes("png")
        image = Image.open(BytesIO(img_bytes))

        text = pytesseract.image_to_string(image)
        full_text += text

    return full_text