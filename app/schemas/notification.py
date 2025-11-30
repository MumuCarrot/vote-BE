from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class NotificationBase(BaseModel):
    """Base schema for Notification with common fields."""
    message: str = Field(..., min_length=1, description="Notification message")
    is_read: bool = False


class NotificationCreate(NotificationBase):
    """Schema for creating a new notification."""
    user_id: str


class NotificationUpdate(BaseModel):
    """Schema for updating notification."""
    message: Optional[str] = Field(None, min_length=1, description="Notification message")
    is_read: Optional[bool] = None


class NotificationResponse(NotificationBase):
    """Schema for notification response."""
    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: str
    created_at: Optional[datetime] = None

