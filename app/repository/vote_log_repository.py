from sqlalchemy.ext.asyncio import AsyncSession

from app.models.vote_log import VoteLog
from app.repository.base_repository import BaseRepository


class VoteLogRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(model=VoteLog, session=session, log_data_name="VoteLog")

