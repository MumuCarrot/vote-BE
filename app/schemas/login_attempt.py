from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr


class LoginAttemptBase(BaseModel):
    """Base schema for LoginAttempt with common fields."""
    email: Optional[EmailStr] = None
    ip_address: Optional[str] = None
    success: bool = False


class LoginAttemptCreate(LoginAttemptBase):
    """Schema for creating a new login attempt."""
    user_id: Optional[str] = None


class LoginAttemptUpdate(BaseModel):
    """Schema for updating login attempt."""
    email: Optional[EmailStr] = None
    ip_address: Optional[str] = None
    success: Optional[bool] = None
    user_id: Optional[str] = None


class LoginAttemptResponse(LoginAttemptBase):
    """Schema for login attempt response."""
    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: Optional[str] = None
    timestamp: Optional[datetime] = None
