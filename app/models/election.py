from datetime import datetime
from typing import Optional, TYPE_CHECKING

from sqlalchemy import String, DateTime, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base
from app.utils.id_mixin import IdMixin

if TYPE_CHECKING:
    from app.models.election_setting import ElectionSetting
    from app.models.candidates import Candidate
    from app.models.vote import Vote
    from app.models.election_access import ElectionAccess
    from app.models.election_results_cache import ElectionResultsCache
    from app.models.attachment import Attachment


class Election(IdMixin, Base):
    __tablename__ = "elections"

    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    start_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    is_public: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, default=None, nullable=True)

    # Relationships
    settings: Mapped[Optional["ElectionSetting"]] = relationship("ElectionSetting", back_populates="election", uselist=False)
    candidates: Mapped[list["Candidate"]] = relationship("Candidate", back_populates="election")
    votes: Mapped[list["Vote"]] = relationship("Vote", back_populates="election")
    accesses: Mapped[list["ElectionAccess"]] = relationship("ElectionAccess", back_populates="election")
    results_cache: Mapped[Optional["ElectionResultsCache"]] = relationship("ElectionResultsCache", back_populates="election", uselist=False)
    attachments: Mapped[list["Attachment"]] = relationship("Attachment", back_populates="election")

    def __repr__(self):
        return f"<Election(id={self.id}, title='{self.title}')>"
