from .models import Post

from sqlalchemy.future import select
from database.database import async_session_maker
from sqlalchemy.exc import SQLAlchemyError


class BaseDAO:
    @classmethod
    async def find_by_id(cls, data_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=data_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()
    
    @classmethod
    async def find(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
           
            result = await session.execute(query)
            return result.scalar()

    @classmethod
    async def add(cls, **values):
        async with async_session_maker() as session:
            async with session.begin():
                new_instance = cls.model(**values)
                session.add(new_instance)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return new_instance


 
class PostDAO(BaseDAO):
    model = Post
