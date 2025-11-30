from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class VoteLogBase(BaseModel):
    """Base schema for VoteLog with common fields."""
    action: str = Field(..., min_length=1, description="Action performed on the vote")


class VoteLogCreate(VoteLogBase):
    """Schema for creating a new vote log."""
    vote_id: str


class VoteLogUpdate(BaseModel):
    """Schema for updating vote log."""
    action: Optional[str] = Field(None, min_length=1, description="Action performed on the vote")


class VoteLogResponse(VoteLogBase):
    """Schema for vote log response."""
    model_config = ConfigDict(from_attributes=True)

    id: str
    vote_id: str
    timestamp: Optional[datetime] = None

