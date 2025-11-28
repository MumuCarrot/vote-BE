from sqlalchemy.ext.asyncio import AsyncSession

from app.models.password_reset_token import PasswordResetToken
from app.repository.base_repository import BaseRepository


class PasswordResetTokenRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(model=PasswordResetToken, session=session, log_data_name="PasswordResetToken")

