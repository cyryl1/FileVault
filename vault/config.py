from enum import Enum

class Config:
    """Configuration settings"""
    MONGODB_URI = "mongodb+srv://aribisalapraise12:Praise2020@vault.hre9qzn.mongodb.net/?retryWrites=true&w=majority&appName=Vault"
    DATABASE_NAME = "vaultdatabase"
    REDIS_HOST = "localhost"
    REDIS_PORT = 6379
    REDIS_DB = 0
    SESSION_TIMEOUT = 3600
    STORAGE_DIR = "storage"
    UPLOADS_DIR = "storage/uploads"
    THUMBNAILS_DIR = "storage/thumbnails"
    CELERY_BROKER_URL = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/0"

class FileType(Enum):
    FILE = "file"
    FOLDER = "folder"
    IMAGE = "image"

class Visibility(Enum):
    PRIVATE = "private"
    PUBLIC = "public"