from sqlalchemy.ext.asyncio import AsyncSession

from app.models.election_access import ElectionAccess
from app.repository.base_repository import BaseRepository


class ElectionAccessRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(model=ElectionAccess, session=session, log_data_name="ElectionAccess")

