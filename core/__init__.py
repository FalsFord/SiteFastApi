from fastapi import APIRouter

from app.router import router as user_router

router = APIRouter()
router.include_router(router=user_router)
