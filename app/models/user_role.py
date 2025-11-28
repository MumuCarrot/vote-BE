from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base
from app.utils.id_mixin import IdMixin


class UserRole(IdMixin, Base):
    __tablename__ = "user_roles"

    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    def __repr__(self):
        return f"<UserRole(id={self.id}, name='{self.name}')>"
