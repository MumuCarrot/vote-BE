from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user_role_link import UserRoleLink
from app.repository.base_repository import BaseRepository


class UserRoleLinkRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(model=UserRoleLink, session=session, log_data_name="UserRoleLink")

