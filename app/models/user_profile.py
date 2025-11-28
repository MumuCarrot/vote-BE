from datetime import date, datetime
from typing import Optional

from sqlalchemy import String, ForeignKey, DateTime, Date
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base
from app.utils.id_mixin import IdMixin


class UserProfile(IdMixin, Base):
    __tablename__ = "user_profiles"

    user_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("users.id"),
        unique=True,
        nullable=False
    )
    birth_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    avatar_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    address: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, default=None, nullable=True)

    def __repr__(self):
        return f"<UserProfile(id={self.id}, user_id={self.user_id})>"
