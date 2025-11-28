from datetime import datetime
from typing import Optional

from sqlalchemy import String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base
from app.utils.id_mixin import IdMixin


class LoginAttempt(IdMixin, Base):
    __tablename__ = "login_attempts"

    user_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("users.id"), nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    ip_address: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    success: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    timestamp: Mapped[Optional[datetime]] = mapped_column(DateTime, default=None, nullable=True)

    def __repr__(self):
        return f"<LoginAttempt(id={self.id}, email='{self.email}', success={self.success})>"

