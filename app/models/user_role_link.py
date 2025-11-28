from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base
from app.utils.id_mixin import IdMixin


class UserRoleLink(IdMixin, Base):
    __tablename__ = "user_role_links"

    user_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("users.id"),
        nullable=False
    )
    role_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("user_roles.id"),
        nullable=False
    )

    def __repr__(self):
        return f"<UserRoleLink(id={self.id}, user_id={self.user_id}, role_id={self.role_id})>"
