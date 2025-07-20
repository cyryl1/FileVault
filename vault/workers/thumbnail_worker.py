from celery import Celery
from vault.config import Config
from PIL import Image
from pathlib import Path

celery_app = Celery(
    'filevault',
    broker=Config.CELERY_BROKER_URL,
    backend=Config.CELERY_RESULT_BACKEND
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

@celery_app.task
def generate_thumbnail(file_id: str, file_path: str):
    """Generate thumbnail for an image file"""
    try:
        with Image.open(file_path) as img:
            img.thumbnail((100, 100), Image.Resampling.LANCZOS)

            thumbnail_path = Path(Config.THUMBNAILS_DIR) / f"{file_id}.jpg"
            thumbnail_path.parent.mkdir(exist_ok=True)

            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            img.save(thumbnail_path, "JPEG", quality=85)
            return f"Thumbnail generated for {file_id}"
    except Exception as e:
        return f"Error generating thumbnail for {file_id}: {str(e)}"


