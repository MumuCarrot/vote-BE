from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user_role import UserRole
from app.repository.base_repository import BaseRepository


class UserRoleRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(model=UserRole, session=session, log_data_name="UserRole")

