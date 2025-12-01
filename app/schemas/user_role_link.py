from typing import Optional

from pydantic import BaseModel, ConfigDict


class UserRoleLinkBase(BaseModel):
    """Base schema for UserRoleLink with common fields."""
    user_id: str
    role_id: str


class UserRoleLinkCreate(UserRoleLinkBase):
    """Schema for creating a new user role link."""
    pass


class UserRoleLinkUpdate(BaseModel):
    """Schema for updating user role link."""
    user_id: Optional[str] = None
    role_id: Optional[str] = None


class UserRoleLinkResponse(UserRoleLinkBase):
    """Schema for user role link response."""
    model_config = ConfigDict(from_attributes=True)

    id: str

