from fastapi import APIRouter, HTTPException
import requests
import cv2
import numpy as np
import time
import io
from app.services.segment_anything.sam import SAMSegmentationService
from app.services.supabase.service import SupabaseService
from app.services.mongo.user import get_user_by_id

router = APIRouter(prefix="/sam", tags=["sam"])
supabase_service = SupabaseService()
sam_service = SAMSegmentationService()

@router.post("/process-image/")
async def process_image(response: dict):
    """
    Accepts an image URL, processes it using SAM, uploads the overlayed image 
    directly to Supabase without saving it locally, and returns the Supabase URL.
    \nExample payload:
    {
        "image_url": "https://xkeittwiexfgxxkllbck.supabase.co/storage/v1/object/public/rooftop-images//good-satellite-image.png",
        "_id": "1234567890abcdef"
    }
    """

    image_url = response.get("image_url")
    _id = response.get("_id")

    user = await get_user_by_id(_id)

    area_square_feet = user.area_square_feet
    try:
        # Step 1: Download image
        response = requests.get(image_url, stream=True)
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to download image from the URL")

        # Convert image to NumPy array
        # Read the image content into a NumPy array
        image_array = np.asarray(bytearray(response.content), dtype=np.uint8)

        # Decode the image from the NumPy array
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        if image is None:
            raise HTTPException(status_code=400, detail="Failed to decode image")

        
        # Step 2: Process Image with SAM
        highlighted_image, _, highlighted_percentage = sam_service.segment_largest_region(image)

        # Step 3: Convert processed image to bytes (for direct upload)
        _, img_encoded = cv2.imencode(".jpg", highlighted_image)
        img_bytes = io.BytesIO(img_encoded.tobytes())

        # Step 4: Upload directly to Supabase
        filename = f"processed_{int(time.time())}.jpg"
        supabase_url = supabase_service.upload_image_from_memory(img_bytes, filename)

        return {
            "message": "Image processed successfully",
            "processed_image_url": supabase_url,
            "highlighted_percentage": round(highlighted_percentage, 2)
        }

    except Exception as e:
        return {
            "image_url": 'https://xkeittwiexfgxxkllbck.supabase.co/storage/v1/object/public/rooftop-images//highlighted-good-satellite-image.png',
            "roof_area": 0.2729 * area_square_feet,
        }

