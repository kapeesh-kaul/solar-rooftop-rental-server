from io import BytesIO
from supabase import create_client, Client
from app.core.config import settings  # Import Settings

class SupabaseService:
    def __init__(self):
        """Initialize the Supabase client using settings."""
        self.client: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY)

    def upload_image_from_memory(self, img_bytes: BytesIO, destination_path: str = "output.jpg") -> str:
        """
        Uploads an image directly from memory (BytesIO) to Supabase storage.

        Args:
            img_bytes (BytesIO): Image data in memory.
            destination_path (str): The destination file path in Supabase storage.

        Returns:
            str: The public URL of the uploaded image.
        """
        # Ensure the bucket exists (use your bucket name)
        bucket_name = "rooftop-images"

        # Reset the file pointer
        img_bytes.seek(0)

        # Upload the image
        response = self.client.storage.from_(bucket_name).upload(
            path=destination_path, 
            file=img_bytes, 
            file_options={"content-type": "image/jpeg"}  # Ensure correct content type
        )

        if response:
            public_url = f"{settings.SUPABASE_URL}/storage/v1/object/public/{bucket_name}/{destination_path}"
            return public_url
        else:
            raise Exception("Failed to upload image to Supabase.")
