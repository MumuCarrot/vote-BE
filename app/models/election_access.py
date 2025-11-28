from datetime import datetime
from typing import Optional, TYPE_CHECKING

from sqlalchemy import String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base
from app.utils.id_mixin import IdMixin

if TYPE_CHECKING:
    from app.models.election import Election
    from app.models.user import User


class ElectionAccess(IdMixin, Base):
    __tablename__ = "election_access"

    election_id: Mapped[str] = mapped_column(String(36), ForeignKey("elections.id"), nullable=False)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False)
    granted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, default=None, nullable=True)

    # Relationships
    election: Mapped["Election"] = relationship("Election", back_populates="accesses")
    user: Mapped["User"] = relationship("User", back_populates="election_accesses")

    def __repr__(self):
        return f"<ElectionAccess(id={self.id}, election_id={self.election_id}, user_id={self.user_id})>"

