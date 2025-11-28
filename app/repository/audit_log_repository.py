from sqlalchemy.ext.asyncio import AsyncSession

from app.models.audit_log import AuditLog
from app.repository.base_repository import BaseRepository


class AuditLogRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(model=AuditLog, session=session, log_data_name="AuditLog")

