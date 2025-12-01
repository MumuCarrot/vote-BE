from sqlalchemy.ext.asyncio import AsyncSession

from app.models.login_attempt import LoginAttempt
from app.repository.base_repository import BaseRepository


class LoginAttemptRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(model=LoginAttempt, session=session, log_data_name="LoginAttempt")

