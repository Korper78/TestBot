import asyncio
# from db_tools.models import TGBase
# target_metadata = TGBase.metadata

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
# from sqlalchemy.orm import declarative_base
from db_tools.models import TGBase

DATABASE_URI: str = 'sqlite+aiosqlite:///zbk.db'

engine = create_async_engine(DATABASE_URI)


def create_session(func):
    async def wrapper(**kwargs):
        async with AsyncSession(bind=engine) as session:
            return await func(**kwargs, session=session)
    return wrapper


# class MySession:
#     def __int__(self):
#         self.session = AsyncSession(bind=engine)


class DbCRUD:
    # session = AsyncSession(bind=engine)

    @staticmethod
    @create_session
    async def add(db_object: TGBase, session: AsyncSession = None) -> int | None:
        session.add(db_object)
        try:
            await session.commit()
            await session.refresh(db_object)
        except IntegrityError as e:
            print(e)
            return None
        return db_object.id

    @staticmethod
    @create_session
    async def get_all(db_object: TGBase, session: AsyncSession = None) -> list | None:
        obj = await session.execute(select(db_object))
        return obj.all()

    @staticmethod
    @create_session
    async def get_one(db_object: TGBase, obj_id: int, session: AsyncSession = None) -> TGBase | None:
        # obj = await session.execute(select(db_object).where(db_object.id == id))
        # return obj.first()
        return await session.get(db_object, obj_id)

    @staticmethod
    @create_session
    async def update(db_object: TGBase, obj_id: int, session: AsyncSession = None, **kwargs):
        await session.execute(update(db_object).where(db_object.id == obj_id).values(**kwargs))
        await session.commit()

    @staticmethod
    @create_session
    async def delete(db_object: TGBase, session: AsyncSession = None):
        await session.delete(db_object)
        await session.commit()
