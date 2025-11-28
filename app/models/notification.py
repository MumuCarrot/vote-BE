from datetime import datetime
from typing import Optional, TYPE_CHECKING

from sqlalchemy import String, ForeignKey, Text, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base
from app.utils.id_mixin import IdMixin

if TYPE_CHECKING:
    from app.models.user import User


class Notification(IdMixin, Base):
    __tablename__ = "notifications"

    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, default=None, nullable=True)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="notifications")

    def __repr__(self):
        return f"<Notification(id={self.id}, user_id={self.user_id}, is_read={self.is_read})>"

