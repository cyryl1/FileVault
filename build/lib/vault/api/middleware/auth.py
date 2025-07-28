from fastapi import HTTPException, Depends, Header
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Dict, Optional, Any
from vault.services.auth import AuthService
import logging

logger = logging.getLogger(__name__)
security = HTTPBasic()

def get_current_user(auth_service: AuthService = Depends(lambda: AuthService()), x_token: Optional[str] = Header(None)) -> Dict[str, Any]:
    """Get current user from X-Token header"""
    if not x_token:
        raise HTTPException(status_code=401, detail="Authentication token required")
    
    user = auth_service.get_current_user(x_token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    return user

async def basic_auth(credentials: HTTPBasicCredentials = Depends(security)):
    """Validate HTTP Basic Auth"""
    auth_service = AuthService()
    token = auth_service.login(credentials.username, credentials.password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"id": auth_service.get_user_id(token), "token": token}