from fastapi import APIRouter

from app.controllers import auth, email, user

router = APIRouter()

router.include_router(auth.router, tags=["Auth"])
router.include_router(user.router, tags=["Users"])
router.include_router(email.router, tags=["Email"])
