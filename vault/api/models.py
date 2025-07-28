from pydantic import BaseModel, EmailStr
from typing import Optional

class UserAuth(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    email: str

class LoginResponse(BaseModel):
    token: str

class StatusResponse(BaseModel):
    status: str

class StatsResponse(BaseModel):
    users: int
    files: int

class FileMetadata(BaseModel):
    file_id: str
    filename: str
    type: str
    size: int
    parent_id: Optional[str] = None
    visibility: str
    created_at: str

class FileUploadResponse(BaseModel):
    file_id: str
    filename: str
    size: int
    type: str
    upload_time: str

class FolderCreateResponse(BaseModel):
    folder_id: str
    name: str
