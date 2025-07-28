from fastapi import APIRouter, Depends, Header, Form, File, Query, UploadFile
from vault.api.controllers.file_controllers import FileController
from vault.api.middleware.auth import basic_auth, get_current_user
from vault.api.models import (
    FileMetadata, FileUploadResponse, FolderCreateResponse
)
from typing import List, Optional, Union

file_router = APIRouter(prefix="/files", tags=["Files"])

controller = FileController()

@file_router.post("", response_model=Union[FileUploadResponse, FolderCreateResponse])
async def create_file_or_folder(
    name: str = Form(...),
    type: str = Form(...),
    parentId: Optional[str] = Form(None),
    data: Optional[UploadFile] = File(None),
    user=Depends(get_current_user)
):
    """Upload a file or create a foler"""
    return await controller.create_file_or_folder(name, type, parentId, data, user)

@file_router.get("/{file_id}", response_model=FileMetadata)
async def get_file_metadata(file_id: str, user=Depends(get_current_user)):
    """Get file metadata"""
    return await controller.get_file_metadata(file_id, user)

@file_router.get("", response_model=List[FileMetadata])
async def list_files(parentId: Optional[str] = Query(None), user=Depends(get_current_user)):
    """List files for the current user"""
    return await controller.list_files(parentId, user)

@file_router.put("/{file_id}/publish")
async def publish(file_id: str, user=Depends(get_current_user)):
    """Make a file public"""
    return await controller.publish(file_id, user)

@file_router.put("/{file_id}/unpublish")
async def unpublish(file_id: str, user=Depends(get_current_user)):
    """Make a file private"""
    return await controller.unpublish(file_id, user)

@file_router.get("/{file_id}/data")
async def download_file(file_id: str, user=Depends(get_current_user)):
    """Download file data"""
    return await controller.get_file(file_id, user)

@file_router.get("/{file_id}/thumbnail")
async def download_thumbnail(file_id: str, user=Depends(get_current_user)):
    """Download thumbnail for an image file"""
    return await controller.get_thumbnail(file_id, user)

