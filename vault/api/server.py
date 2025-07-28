from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from vault.api.routes.auth_routes import auth_router  # Use specific router name
from vault.api.routes.file_routes import file_router  # Use specific router name
from vault.repositories.user_repository import UserRepository
from vault.repositories.file_repository import FileRepository
from vault.api.models import StatusResponse, StatsResponse
from fastapi.exceptions import HTTPException
import logging
import uvicorn

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="FileVault API",
    description="A secure file management system with folders, visibility controls, and background processing",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers with prefixes to avoid conflicts
app.include_router(auth_router, prefix="/auth", tags=["authentication"])
app.include_router(file_router, prefix="/files", tags=["files"])

@app.get("/status", response_model=StatusResponse)
async def get_status():
    """Get system status"""
    return StatusResponse(status="OK")

@app.get("/stats", response_model=StatsResponse)
async def get_stats():
    """Get system statistics"""
    try:
        user_repo = UserRepository()
        file_repo = FileRepository()
        return StatsResponse(
            users=user_repo.count(),
            files=file_repo.count()
        )
    except Exception as e:
        logger.error(f"Error retrieving stats: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving stats: {str(e)}")

def main():
    """Main function to start the server"""
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
if __name__ == "__main__":
    main()