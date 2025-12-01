from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import pytest

from app.exceptions.user import UserNotFoundError, ValidationError
from app.schemas.user_profile import (
    UserProfileCreate,
    UserProfileUpdate,
)
from app.services.user_profile import UserProfileService


@pytest.mark.asyncio
async def test_create_user_profile_success(async_session_mock):
    profile_data = UserProfileCreate(
        user_id="user-id-1",
        birth_date=None,
        avatar_url=None,
        address=None,
    )

    user = SimpleNamespace(id="user-id-1")
    created_profile = SimpleNamespace(
        id="profile-id-1",
        user_id="user-id-1",
        birth_date=None,
        avatar_url=None,
        address=None,
    )

    with patch(
        "app.services.user_profile.UserRepository"
    ) as user_repo_cls, patch(
        "app.services.user_profile.UserProfileRepository"
    ) as profile_repo_cls:
        user_repo = AsyncMock()
        user_repo.read_one.return_value = user
        user_repo_cls.return_value = user_repo

        profile_repo = AsyncMock()
        profile_repo.read_one.return_value = None
        profile_repo.create.return_value = created_profile
        profile_repo_cls.return_value = profile_repo

        result = await UserProfileService.create_user_profile(
            async_session_mock, profile_data
        )

        assert result.id == created_profile.id
        user_repo.read_one.assert_awaited_once()
        profile_repo.create.assert_awaited_once()


@pytest.mark.asyncio
async def test_create_user_profile_user_not_found(async_session_mock):
    profile_data = UserProfileCreate(
        user_id="missing-user",
        birth_date=None,
        avatar_url=None,
        address=None,
    )

    with patch("app.services.user_profile.UserRepository") as user_repo_cls:
        user_repo = AsyncMock()
        user_repo.read_one.return_value = None
        user_repo_cls.return_value = user_repo

        with pytest.raises(UserNotFoundError):
            await UserProfileService.create_user_profile(async_session_mock, profile_data)


@pytest.mark.asyncio
async def test_create_user_profile_already_exists(async_session_mock):
    profile_data = UserProfileCreate(
        user_id="user-id-1",
        birth_date=None,
        avatar_url=None,
        address=None,
    )

    user = SimpleNamespace(id="user-id-1")
    existing_profile = SimpleNamespace(id="profile-id-1", user_id="user-id-1")

    with patch(
        "app.services.user_profile.UserRepository"
    ) as user_repo_cls, patch(
        "app.services.user_profile.UserProfileRepository"
    ) as profile_repo_cls:
        user_repo = AsyncMock()
        user_repo.read_one.return_value = user
        user_repo_cls.return_value = user_repo

        profile_repo = AsyncMock()
        profile_repo.read_one.return_value = existing_profile
        profile_repo_cls.return_value = profile_repo

        with pytest.raises(ValidationError):
            await UserProfileService.create_user_profile(async_session_mock, profile_data)


@pytest.mark.asyncio
async def test_get_user_profile_by_id_not_found(async_session_mock):
    with patch(
        "app.services.user_profile.UserProfileRepository"
    ) as profile_repo_cls:
        profile_repo = AsyncMock()
        profile_repo.read_one.return_value = None
        profile_repo_cls.return_value = profile_repo

        result = await UserProfileService.get_user_profile_by_id(
            async_session_mock, "missing-id"
        )

        assert result is None
        profile_repo.read_one.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_user_profile_not_found(async_session_mock):
    update_data = UserProfileUpdate(address="New address")

    with patch(
        "app.services.user_profile.UserProfileRepository"
    ) as profile_repo_cls:
        profile_repo = AsyncMock()
        profile_repo.read_one.return_value = None
        profile_repo_cls.return_value = profile_repo

        with pytest.raises(UserNotFoundError):
            await UserProfileService.update_user_profile(
                async_session_mock, "missing-id", update_data
            )


@pytest.mark.asyncio
async def test_delete_user_profile_success(async_session_mock):
    with patch(
        "app.services.user_profile.UserProfileRepository"
    ) as profile_repo_cls:
        profile_repo = AsyncMock()
        profile_repo.delete.return_value = True
        profile_repo_cls.return_value = profile_repo

        result = await UserProfileService.delete_user_profile(
            async_session_mock, "profile-id-1"
        )

        assert result is True
        profile_repo.delete.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_user_profile_not_found(async_session_mock):
    with patch(
        "app.services.user_profile.UserProfileRepository"
    ) as profile_repo_cls:
        profile_repo = AsyncMock()
        profile_repo.delete.return_value = False
        profile_repo_cls.return_value = profile_repo

        with pytest.raises(UserNotFoundError):
            await UserProfileService.delete_user_profile(
                async_session_mock, "missing-id"
            )


