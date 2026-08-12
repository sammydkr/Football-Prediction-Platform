from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.schemas.auth import LoginRequest, RefreshRequest, RegisterRequest, TokenPair, UserRead
from app.services.auth import (
    authenticate,
    get_current_user,
    issue_token_pair,
    register_user,
    rotate_refresh_token,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=201)
async def register(payload: RegisterRequest, session: AsyncSession = Depends(get_session)):
    return await register_user(session, payload.email, payload.password)


@router.post("/login", response_model=TokenPair)
async def login(payload: LoginRequest, session: AsyncSession = Depends(get_session)):
    user = await authenticate(session, payload.email, payload.password)
    access_token, refresh_token = await issue_token_pair(session, user)
    return TokenPair(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh", response_model=TokenPair)
async def refresh(payload: RefreshRequest, session: AsyncSession = Depends(get_session)):
    access_token, refresh_token = await rotate_refresh_token(session, payload.refresh_token)
    return TokenPair(access_token=access_token, refresh_token=refresh_token)


@router.get("/me", response_model=UserRead)
async def me(user=Depends(get_current_user)):
    return user

