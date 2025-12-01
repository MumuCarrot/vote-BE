from datetime import datetime
from typing import Optional, TYPE_CHECKING

from sqlalchemy import String, ForeignKey, DateTime, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base
from app.utils.id_mixin import IdMixin

if TYPE_CHECKING:
    from app.models.vote import Vote


class VoteLog(IdMixin, Base):
    __tablename__ = "vote_logs"

    vote_id: Mapped[str] = mapped_column(String(36), ForeignKey("votes.id"), nullable=False)
    action: Mapped[str] = mapped_column(String, nullable=False)
    timestamp: Mapped[Optional[datetime]] = mapped_column(DateTime, default=None, nullable=True)

    __table_args__ = (
        Index('idx_vote_log_vote_id', 'vote_id'),
        Index('idx_vote_log_timestamp', 'timestamp'),
    )

    # Relationships
    vote: Mapped["Vote"] = relationship("Vote", back_populates="logs")

    def __repr__(self):
        return f"<VoteLog(id={self.id}, vote_id={self.vote_id}, action='{self.action}')>"

