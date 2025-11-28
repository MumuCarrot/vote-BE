from datetime import datetime
from typing import Optional

from sqlalchemy import String, ForeignKey, Text, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base
from app.utils.id_mixin import IdMixin


class Notification(IdMixin, Base):
    __tablename__ = "notifications"

    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, default=None, nullable=True)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"<Notification(id={self.id}, user_id={self.user_id}, is_read={self.is_read})>"

