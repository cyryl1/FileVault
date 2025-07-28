from typing import Dict, Any
from fastapi import Depends, HTTPException, Header
from vault.services.auth import AuthService
from vault.api.middleware.auth import basic_auth, get_current_user
from vault.api.models import UserAuth, LoginResponse, UserResponse

class AuthController:
    def __init__(self, auth_service: AuthService = None):
        self.auth_service = auth_service or AuthService()

    async def register(self, user_data: UserAuth) -> UserResponse:
        """Register a new user"""
        try:
            user = self.auth_service.register(user_data.email, user_data.password)
            return UserResponse(**user)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def login(self, user: UserAuth) -> LoginResponse:
        """Login user"""
        try:
            token = self.auth_service.login(user.email, user.password)

            return LoginResponse(token)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def logout(self, x_token: str):
        """Logout user"""
        self.auth_service.logout(x_token)
        return {"message": "Logged out successfully"}

    async def get_profile(self, user: Dict[str, Any] = Depends(get_current_user)) -> UserResponse:
        """Get user profile"""
        return UserResponse(**user)