from celery import Celery
from vault.config import Config
from PIL import Image
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Celery app with proper configuration
app = Celery('vault')
app.conf.update(
    broker_url=Config.CELERY_BROKER_URL,
    result_backend=Config.CELERY_RESULT_BACKEND,
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

@app.task
def generate_thumbnail(file_id: str, file_path: str):
    """Generate a thumbnail for an image file"""
    try:
        logger.info(f"Generating thumbnail for file_id: {file_id}, path: {file_path}")
        source_path = Path(file_path)
        if not source_path.exists():
            logger.error(f"File not found: {file_path}")
            raise FileNotFoundError(f"File not found: {file_path}")

        thumbnail_dir = Path(Config.THUMBNAILS_DIR)
        thumbnail_dir.mkdir(exist_ok=True)
        thumbnail_path = thumbnail_dir / f"{file_id}.jpg"

        with Image.open(source_path) as img:
            if img.mode != 'RGB':
                img = img.convert('RGB')
            img.thumbnail((128, 128))
            img.save(thumbnail_path, 'JPEG', quality=90)
            
        logger.info(f"Thumbnail generated: {thumbnail_path}")
        return str(thumbnail_path)
        
    except Exception as e:
        logger.error(f"Failed to generate thumbnail for {file_id}: {str(e)}")
        raise