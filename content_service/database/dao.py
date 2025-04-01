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

    @classmethod
    async def delete(cls, post_id):
        async with async_session_maker() as session:
            async with session.begin():
                post = await db.execute(
                    select(Post).where(Post.id == post_id)
                )
                post = post.scalar_one_or_none()
                # Удаляем посты
                session.delete(post)
                session.commit()
                return {"message": "Пост успешно удален"}
                
    @staticmethod
    async def update(url: str, date: str) -> None:
        """async with async_session_maker() as session:
            async with session.begin():
                stmt = (
                    update(DataBaseLinks)
                    .where(DataBaseLinks.link == url)
                    .values(last_link_upd=date)
                )
                result = await session.execute(stmt)
                return result.rowcount
                
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e"""
        pass


 
class PostDAO(BaseDAO):
    model = Post
