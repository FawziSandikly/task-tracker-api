# Health check endpoint for verifying API availability
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(tags=["health"])


class HealthResponse(BaseModel):
    """Response schema for health check endpoint"""
    status: str
    message: str


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint. Returns 200 OK with status message.
    Used to verify API is running and responsive.
    """
    return HealthResponse(
        status="healthy",
        message="Task Tracker API is running"
    )