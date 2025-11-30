from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ElectionBase(BaseModel):
    """Base schema for Election with common fields."""
    title: str = Field(..., min_length=1, description="Election title")
    description: Optional[str] = None
    start_date: datetime
    end_date: datetime
    is_public: bool = True


class ElectionCreate(ElectionBase):
    """Schema for creating a new election."""
    pass


class ElectionUpdate(BaseModel):
    """Schema for updating election."""
    title: Optional[str] = Field(None, min_length=1, description="Election title")
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    is_public: Optional[bool] = None


class ElectionResponse(ElectionBase):
    """Schema for election response."""
    model_config = ConfigDict(from_attributes=True)

    id: str
    created_at: Optional[datetime] = None

