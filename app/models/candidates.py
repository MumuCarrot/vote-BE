from typing import Optional

from sqlalchemy import String, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base
from app.utils.id_mixin import IdMixin


class Candidate(IdMixin, Base):
    __tablename__ = "candidates"

    election_id: Mapped[str] = mapped_column(String(36), ForeignKey("elections.id"), nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    def __repr__(self):
        return f"<Candidate(id={self.id}, name='{self.name}', election_id={self.election_id})>"
