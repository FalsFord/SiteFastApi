from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import User
from app.schemas import SUserRegister


async def get_users(session: AsyncSession) -> list[User]:
    stmt = select(User).order_by(User.username)
    result: Result = await session.execute(stmt)
    users = result.scalars().all()
    return list(users)


async def get_user(
    session: AsyncSession, username: str = None, email: EmailStr = None
) -> User | None:
    stmt = None
    if username is not None:
        stmt = select(User).where(User.username == username)
    elif email is not None:
        stmt = select(User).where(User.email == email)
    result = await session.execute(stmt)
    return result.scalars().first()


async def create_user(session: AsyncSession, user_in: SUserRegister) -> User:
    user = User(**user_in.model_dump())
    session.add(user)
    print(f"Attempting to create user: {user_in.model_dump()}")
    await session.commit()
    # await session.refresh(user)
    return user
