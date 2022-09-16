from typing import Generic, Optional, Type, TypeVar, Union

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel, select

ModelType = TypeVar("ModelType", bound=SQLModel)
CreateModelType = TypeVar("CreateModelType", bound=SQLModel)
UpdateModelType = TypeVar("UpdateModelType", bound=SQLModel)


class CRUDBase(Generic[ModelType, CreateModelType, UpdateModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(
        self,
        session: AsyncSession,
        *,
        id: int,
    ) -> Optional[ModelType]:
        obj = await session.get(self.model, id)
        return obj

    async def get_batch(
        self,
        session: AsyncSession,
        *,
        offset: int = 0,
        limit: int = 100,
    ) -> list[ModelType]:
        statement = select(self.model).limit(limit).offset(offset)
        result = await session.execute(statement)
        return result.scalars().all()

    async def create(
        self,
        session: AsyncSession,
        *,
        obj: CreateModelType,
    ) -> ModelType:
        db_obj = self.model.from_orm(obj)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(
        self,
        session: AsyncSession,
        *,
        db_obj: ModelType,
        obj: Union[UpdateModelType, dict],
    ) -> ModelType:
        if isinstance(obj, dict):
            update_data = obj
        else:
            update_data = obj.dict(exclude_unset=True)

        for key, value in update_data.items():
            setattr(db_obj, key, value)

        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def delete(
        self,
        session: AsyncSession,
        *,
        id: int,
    ) -> Optional[ModelType]:
        db_obj = await self.get(session, id=id)

        if not db_obj:
            return None

        await session.delete(db_obj)
        await session.commit()
        return db_obj
