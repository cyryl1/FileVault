from typing import Dict, Any, List, Optional
from fastapi import Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from vault.services.file_service import FileService
from vault.config import Config, FileType, Visibility
from vault.api.middleware.auth import get_current_user
from vault.api.models import FileMetadata, FileUploadResponse, FolderCreateResponse

class FileController:
    def __init__(self, file_service: FileService = None):
        self.file_service = file_service or FileService()

    async def create_file_or_folder(self, name: str, type: str, parent_id: Optional[str] = None, data: Optional[UploadFile] = None, user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
        """Upload a file or create a folder"""
        try:
            if type == FileType.FOLDER.value:
                result = self.file_service.create_folder(user["id"], name, parent_id)
                return FolderCreateResponse(**result)
            elif type in [FileType.FILE.value, FileType.IMAGE.value]:
                if not data:
                    raise HTTPException(status_code=400, detail="File data required")
                result = self.file_service.upload_file(user["id"], data, parent_id)
                return FileUploadResponse(**result)
            else:
                raise ValueError("Invalid type. Must be 'file', 'folder', or 'image'")
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        
    async def list_files(self, parent_id: Optional[str] = None, user: Dict[str, Any] = Depends(get_current_user)) -> List[FileMetadata]:
        """List files for user"""
        files = self.file_service.list_files(user["id"], parent_id)
        return [FileMetadata(**f) for f in files]
    
    async def publish(self, file_id: str, user: Dict[str, Any] = Depends(get_current_user)):
        """Make file public"""
        success = self.file_service.set_visibility(file_id, user["id"], Visibility.PUBLIC)
        if not success:
            raise HTTPException(status_code=404, detail="Fail not found")
        return {"message": "File publish successfully"}
    
    async def unpublish(self, file_id: str, user: Dict[str, Any] = Depends(get_current_user)):
        """Make file private"""
        success = self.file_service.set_visibility(file_id, user["id"], Visibility.PRIVATE)
        if not success:
            raise HTTPException(status_code=404, detail="File not found")
        return {"message": "File unpublished succesfully"}
    
    async def get_file(self, file_id: str, user: Optional[Dict[str, Any]] = Depends(get_current_user)):
        """Download file data"""
        try:
            user_id = user["id"] if user else None
            file_path = self.file_service.get_file_path(file_id)
            file_info = self.file_service.get_file_info(file_id, user_id)
            return FileResponse(
                path=file_path,
                filename=file_info["filename"],
                media_type='application/octet-stream'
            )
        except FileNotFoundError:
            raise HTTPException(status_code=404, detail="File not found")
        except PermissionError:
            raise HTTPException(status_code=403, detail="Access denied")
        
    async def get_thumbnail(self, file_id: str, user: Optional[Dict[str, Any]] = Depends(get_current_user)):
        """Download thumbnail"""
        try:
            user_id = user["id"] if user else None
            thumbnail_path = self.file_service.get_thumbnail_path(file_id, user_id)
            return FileResponse(
                path=thumbnail_path,
                filename=f"{file_id}_thumbnail.jpg",
                media_type='image/jpg'
            )
        except FileNotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))
        except PermissionError:
            raise HTTPException(status_code=403, detail="Access denied")
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

