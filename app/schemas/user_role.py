from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class UserRoleBase(BaseModel):
    """Base schema for UserRole with common fields."""
    name: str = Field(..., min_length=1, description="Role name")


class UserRoleCreate(UserRoleBase):
    """Schema for creating a new user role."""
    pass


class UserRoleUpdate(BaseModel):
    """Schema for updating user role."""
    name: Optional[str] = Field(None, min_length=1, description="Role name")


class UserRoleResponse(UserRoleBase):
    """Schema for user role response."""
    model_config = ConfigDict(from_attributes=True)

    id: str

