from datetime import datetime
from typing import Optional

from sqlalchemy import String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base
from app.utils.id_mixin import IdMixin


class ElectionAccess(IdMixin, Base):
    __tablename__ = "election_access"

    election_id: Mapped[str] = mapped_column(String(36), ForeignKey("elections.id"), nullable=False)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False)
    granted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, default=None, nullable=True)

    def __repr__(self):
        return f"<ElectionAccess(id={self.id}, election_id={self.election_id}, user_id={self.user_id})>"

