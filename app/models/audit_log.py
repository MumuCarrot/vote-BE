from datetime import datetime
from typing import Optional

from sqlalchemy import String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base
from app.utils.id_mixin import IdMixin


class AuditLog(IdMixin, Base):
    __tablename__ = "audit_logs"

    user_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("users.id"), nullable=True)
    action: Mapped[str] = mapped_column(String, nullable=False)
    entity_type: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    entity_id: Mapped[Optional[str]] = mapped_column(String(36), nullable=True)
    timestamp: Mapped[Optional[datetime]] = mapped_column(DateTime, default=None, nullable=True)

    def __repr__(self):
        return f"<AuditLog(id={self.id}, action='{self.action}', user_id={self.user_id})>"

