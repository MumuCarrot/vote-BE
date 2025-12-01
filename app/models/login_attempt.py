from datetime import datetime
from typing import Optional, TYPE_CHECKING

from sqlalchemy import String, ForeignKey, DateTime, Boolean, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base
from app.utils.id_mixin import IdMixin

if TYPE_CHECKING:
    from app.models.user import User


class LoginAttempt(IdMixin, Base):
    __tablename__ = "login_attempts"

    user_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("users.id"), nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    ip_address: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    success: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    timestamp: Mapped[Optional[datetime]] = mapped_column(DateTime, default=None, nullable=True)

    __table_args__ = (
        Index('idx_login_attempt_user_id', 'user_id'),
        Index('idx_login_attempt_email', 'email'),
        Index('idx_login_attempt_timestamp', 'timestamp'),
        Index('idx_login_attempt_success', 'success'),
        Index('idx_login_attempt_email_timestamp', 'email', 'timestamp'),
    )

    # Relationships
    user: Mapped[Optional["User"]] = relationship("User", back_populates="login_attempts")

    def __repr__(self):
        return f"<LoginAttempt(id={self.id}, email='{self.email}', success={self.success})>"

