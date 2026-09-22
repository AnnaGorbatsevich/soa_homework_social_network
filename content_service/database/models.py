from sqlalchemy.orm import Mapped
from database.database import Base, str_uniq, int_pk, int_uniq, date_null_true, str_null_true

class Post(Base):
    id: Mapped[int_pk]
    name: Mapped[str]
    description: Mapped[str_null_true]
    user_id: Mapped[int]
    is_private: Mapped[bool]
    tags: Mapped[str]
    
class Comment(Base):
    id: Mapped[int_pk]
    source_type: Mapped[str]
    description: Mapped[str_null_true]
    source_id: Mapped[int]
    user_id: Mapped[int]
    
class Like(Base):
    id: Mapped[int_pk]
    source_type: Mapped[str]
    source_id: Mapped[int]
    user_id: Mapped[int]