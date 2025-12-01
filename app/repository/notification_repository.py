from sqlalchemy.ext.asyncio import AsyncSession

from app.models.notification import Notification
from app.repository.base_repository import BaseRepository


class NotificationRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(model=Notification, session=session, log_data_name="Notification")

