from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class PasswordResetTokenBase(BaseModel):
    """Base schema for PasswordResetToken with common fields."""
    token: str = Field(..., min_length=1, description="Reset token")
    expires_at: datetime


class PasswordResetTokenCreate(PasswordResetTokenBase):
    """Schema for creating a new password reset token."""
    user_id: str


class PasswordResetTokenUpdate(BaseModel):
    """Schema for updating password reset token."""
    token: Optional[str] = Field(None, min_length=1, description="Reset token")
    expires_at: Optional[datetime] = None


class PasswordResetTokenResponse(PasswordResetTokenBase):
    """Schema for password reset token response."""
    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: str
    created_at: Optional[datetime] = None

