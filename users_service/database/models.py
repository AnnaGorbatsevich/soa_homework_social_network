from sqlalchemy.orm import Mapped
from database.database import Base, str_uniq, int_pk, int_uniq, date_null_true, str_null_true

class User(Base):
    id: Mapped[int_pk]
    login: Mapped[str_uniq]
    email: Mapped[str_uniq]
    password: Mapped[str]
    
class Profile(Base):
    id: Mapped[int_pk]
    user_id: Mapped[int_uniq]
    first_name: Mapped[str_null_true]
    last_name: Mapped[str_null_true]
    date_of_birth: Mapped[date_null_true]
    email: Mapped[str_uniq]
    phone: Mapped[str_null_true]
    photo_url: Mapped[str_null_true]
    about_me: Mapped[str_null_true]
    location: Mapped[str_null_true]