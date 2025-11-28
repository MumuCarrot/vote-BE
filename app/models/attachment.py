from datetime import datetime
from typing import Optional

from sqlalchemy import String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base
from app.utils.id_mixin import IdMixin


class Attachment(IdMixin, Base):
    __tablename__ = "attachments"

    user_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("users.id"), nullable=True)
    election_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("elections.id"), nullable=True)
    candidate_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("candidates.id"), nullable=True)
    file_url: Mapped[str] = mapped_column(String, nullable=False)
    uploaded_at: Mapped[Optional[datetime]] = mapped_column(DateTime, default=None, nullable=True)

    def __repr__(self):
        return f"<Attachment(id={self.id}, file_url='{self.file_url}')>"

