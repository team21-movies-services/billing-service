from fastapi import APIRouter

from .status import router as status_router

v1_router = APIRouter(prefix="/v1")

v1_router.include_router(status_router)
