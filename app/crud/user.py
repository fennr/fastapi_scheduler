from fastapi import status
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.exceptions import UserNotFound
from app.models.user import User, UserCreate, UserUpdate

from .base import CRUDBase


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    async def get_tg_user(
        self,
        session: AsyncSession,
        *,
        tg: str,
    ) -> User:
        statement = select(self.model).where(self.model.tg == tg)
        result = await session.execute(statement)
        try:
            return result.scalars().one()
        except NoResultFound:
            raise UserNotFound(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'User with tg={tg} not found',
            )

    async def get_vk_user(
        self,
        session: AsyncSession,
        *,
        vk: str,
    ) -> User:
        statement = select(self.model).where(self.model.vk == vk)
        result = await session.execute(statement)
        try:
            return result.scalars().one()
        except NoResultFound:
            raise UserNotFound(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'User with tg={vk} not found',
            )


user = CRUDUser(User)
