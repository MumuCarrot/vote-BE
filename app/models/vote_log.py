from datetime import datetime
from typing import Optional

from sqlalchemy import String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base
from app.utils.id_mixin import IdMixin


class VoteLog(IdMixin, Base):
    __tablename__ = "vote_logs"

    vote_id: Mapped[str] = mapped_column(String(36), ForeignKey("votes.id"), nullable=False)
    action: Mapped[str] = mapped_column(String, nullable=False)
    timestamp: Mapped[Optional[datetime]] = mapped_column(DateTime, default=None, nullable=True)

    def __repr__(self):
        return f"<VoteLog(id={self.id}, vote_id={self.vote_id}, action='{self.action}')>"

