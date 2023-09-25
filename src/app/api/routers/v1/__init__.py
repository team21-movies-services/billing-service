from fastapi import APIRouter

from .pay_systems import router as pay_system_router
from .status import router as status_router
from .subscriptions import router as subscription_router

v1_router = APIRouter(prefix="/v1")

v1_router.include_router(status_router)
v1_router.include_router(pay_system_router)
v1_router.include_router(subscription_router)
