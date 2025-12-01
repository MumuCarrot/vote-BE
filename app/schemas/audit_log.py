from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class AuditLogBase(BaseModel):
    """Base schema for AuditLog with common fields."""
    action: str = Field(..., min_length=1, description="Action performed")
    entity_type: Optional[str] = None
    entity_id: Optional[str] = None


class AuditLogCreate(AuditLogBase):
    """Schema for creating a new audit log."""
    user_id: Optional[str] = None


class AuditLogUpdate(BaseModel):
    """Schema for updating audit log."""
    action: Optional[str] = Field(None, min_length=1, description="Action performed")
    entity_type: Optional[str] = None
    entity_id: Optional[str] = None
    user_id: Optional[str] = None


class AuditLogResponse(AuditLogBase):
    """Schema for audit log response."""
    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: Optional[str] = None
    timestamp: Optional[datetime] = None

