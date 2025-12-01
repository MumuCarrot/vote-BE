from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ElectionAccessBase(BaseModel):
    """Base schema for ElectionAccess with common fields."""
    election_id: str
    user_id: str


class ElectionAccessCreate(ElectionAccessBase):
    """Schema for creating a new election access."""
    pass


class ElectionAccessUpdate(BaseModel):
    """Schema for updating election access."""
    election_id: Optional[str] = None
    user_id: Optional[str] = None


class ElectionAccessResponse(ElectionAccessBase):
    """Schema for election access response."""
    model_config = ConfigDict(from_attributes=True)

    id: str
    granted_at: Optional[datetime] = None

