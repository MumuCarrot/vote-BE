from datetime import datetime
from typing import Optional

from sqlalchemy import String, ForeignKey, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base
from app.utils.id_mixin import IdMixin


class ElectionResultsCache(IdMixin, Base):
    __tablename__ = "election_results_cache"

    election_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("elections.id"),
        unique=True,
        nullable=False
    )
    results_json: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, default=None, nullable=True)

    def __repr__(self):
        return f"<ElectionResultsCache(id={self.id}, election_id={self.election_id})>"

