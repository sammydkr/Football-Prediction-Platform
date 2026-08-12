from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.models.auth import User
from app.services.auth import get_current_user

SessionDep = Depends(get_session)
CurrentUserDep = Depends(get_current_user)


async def session_dependency(session: AsyncSession = SessionDep) -> AsyncSession:
    return session


async def current_user_dependency(user: User = CurrentUserDep) -> User:
    return user

