from sqlalchemy.orm import Mapped
from .database import Base, str_uniq, int_pk, int_uniq, date_null_true, str_null_true

class Post(Base):
    id: Mapped[int_pk]
    name: Mapped[str]
    description: Mapped[str_null_true]
    user_id: Mapped[int_uniq]
    is_private: Mapped[bool]
    tags: Mapped[str]
