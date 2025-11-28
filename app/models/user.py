from datetime import datetime
from typing import Optional, TYPE_CHECKING

from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base
from app.utils.id_mixin import IdMixin

if TYPE_CHECKING:
    from app.models.user_profile import UserProfile
    from app.models.user_role_link import UserRoleLink
    from app.models.vote import Vote
    from app.models.election_access import ElectionAccess
    from app.models.attachment import Attachment
    from app.models.audit_log import AuditLog
    from app.models.notification import Notification
    from app.models.login_attempt import LoginAttempt
    from app.models.password_reset_token import PasswordResetToken


class User(IdMixin, Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    phone: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    first_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, default=None, nullable=True)

    # Relationships
    profile: Mapped[Optional["UserProfile"]] = relationship("UserProfile", back_populates="user", uselist=False)
    role_links: Mapped[list["UserRoleLink"]] = relationship("UserRoleLink", back_populates="user")
    votes: Mapped[list["Vote"]] = relationship("Vote", back_populates="voter", foreign_keys="Vote.voter_id")
    election_accesses: Mapped[list["ElectionAccess"]] = relationship("ElectionAccess", back_populates="user")
    attachments: Mapped[list["Attachment"]] = relationship("Attachment", back_populates="user")
    audit_logs: Mapped[list["AuditLog"]] = relationship("AuditLog", back_populates="user")
    notifications: Mapped[list["Notification"]] = relationship("Notification", back_populates="user")
    login_attempts: Mapped[list["LoginAttempt"]] = relationship("LoginAttempt", back_populates="user")
    password_reset_tokens: Mapped[list["PasswordResetToken"]] = relationship("PasswordResetToken", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}')>"
