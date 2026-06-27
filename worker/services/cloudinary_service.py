import cloudinary
import cloudinary.uploader
from config.settings import settings
from loguru import logger

cloudinary.config(
  cloud_name=settings.CLOUDINARY_CLOUD_NAME,
  api_key=settings.CLOUDINARY_API_KEY,
  api_secret=settings.CLOUDINARY_API_SECRET
)

class CloudinaryService:
    def upload(self, file_path: str, resource_type: str = "video") -> str:
        """
        Uploads a file to Cloudinary and returns the secure URL.
        Use resource_type="video" for mp4 and "raw" for code files.
        """
        try:
            response = cloudinary.uploader.upload(
                file_path,
                folder="Manimx",
                resource_type=resource_type
            )
            return response.get("secure_url")
        except Exception as e:
            logger.error(f"Failed to upload {file_path} to Cloudinary: {e}")
            return ""

cloudinary_service = CloudinaryService()
