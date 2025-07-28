from fastapi import APIRouter, Depends, Header
from vault.api.controllers.auth_controllers import AuthController
from vault.api.middleware.auth import basic_auth, get_current_user
from vault.api.models import (
    UserAuth, UserResponse, LoginResponse
)

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

controller = AuthController()

@auth_router.post("", response_model=UserResponse)
async def register(user_data: UserAuth):
    """Register a new user"""
    return await controller.register(user_data)

@auth_router.get("/login", response_model=LoginResponse)
async def login(user=Depends(basic_auth)):
    """Login user via HTTP Basic Auth"""
    return await controller.login(user)

@auth_router.get("/logout")
async def logout(user=Depends(get_current_user), x_token: str = Header(None)):
    """Logout current user"""
    return await controller.logout(user, x_token)

@auth_router.get("/user/me", response_model=UserResponse)
async def get_profile(user=Depends(get_current_user)):
    """Get current user profile"""
    return await controller.get_profile(user)
