from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class AttachmentBase(BaseModel):
    """Base schema for Attachment with common fields."""
    file_url: str = Field(..., min_length=1, description="URL of the attached file")


class AttachmentCreate(AttachmentBase):
    """Schema for creating a new attachment."""
    user_id: Optional[str] = None
    election_id: Optional[str] = None
    candidate_id: Optional[str] = None


class AttachmentUpdate(BaseModel):
    """Schema for updating attachment."""
    file_url: Optional[str] = Field(None, min_length=1, description="URL of the attached file")
    user_id: Optional[str] = None
    election_id: Optional[str] = None
    candidate_id: Optional[str] = None


class AttachmentResponse(AttachmentBase):
    """Schema for attachment response."""
    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: Optional[str] = None
    election_id: Optional[str] = None
    candidate_id: Optional[str] = None
    uploaded_at: Optional[datetime] = None

