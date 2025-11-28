from sqlalchemy import Integer, Boolean, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base
from app.utils.id_mixin import IdMixin


class ElectionSetting(IdMixin, Base):
    __tablename__ = "election_settings"

    election_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("elections.id"),
        unique=True,
        nullable=False
    )
    allow_revoting: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    max_votes: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    require_auth: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    def __repr__(self):
        return f"<ElectionSetting(id={self.id}, election_id={self.election_id})>"
