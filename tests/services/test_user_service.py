from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import pytest

from app.exceptions.user import UserAlreadyExistsError, UserNotFoundError
from app.schemas.user import UserCreate, UserUpdate
from app.services.user import UserService


@pytest.mark.asyncio
async def test_create_user_success(async_session_mock):
    user_data = UserCreate(
        email="test@example.com",
        phone="123456789",
        password="password123",
        first_name="John",
        last_name="Doe",
    )

    created_user = SimpleNamespace(
        id="user-id-1",
        email=user_data.email,
        phone=user_data.phone,
        password_hash="hashed",
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        created_at=None,
    )

    with patch("app.services.user.UserRepository") as user_repo_cls, patch(
        "app.services.user.UserProfileRepository"
    ) as profile_repo_cls, patch(
        "app.services.user.hash_password", return_value="hashed"
    ) as hash_password_mock:
        user_repo = AsyncMock()
        user_repo.read_one.return_value = None
        user_repo.create.return_value = created_user
        user_repo_cls.return_value = user_repo

        profile_repo = AsyncMock()
        profile_repo.create.return_value = None
        profile_repo_cls.return_value = profile_repo

        result = await UserService.create_user(async_session_mock, user_data)

        hash_password_mock.assert_called_once_with(user_data.password)
        user_repo.read_one.assert_awaited_once()
        user_repo.create.assert_awaited_once()
        profile_repo.create.assert_awaited_once()

        assert result.id == created_user.id
        assert result.email == created_user.email


@pytest.mark.asyncio
async def test_create_user_already_exists(async_session_mock):
    user_data = UserCreate(
        email="existing@example.com",
        phone="123456789",
        password="password123",
        first_name="John",
        last_name="Doe",
    )

    existing_user = SimpleNamespace(id="user-id-existing", email=user_data.email)

    with patch("app.services.user.UserRepository") as user_repo_cls:
        user_repo = AsyncMock()
        user_repo.read_one.return_value = existing_user
        user_repo_cls.return_value = user_repo

        with pytest.raises(UserAlreadyExistsError):
            await UserService.create_user(async_session_mock, user_data)


@pytest.mark.asyncio
async def test_get_user_by_id_not_found(async_session_mock):
    with patch("app.services.user.UserRepository") as user_repo_cls:
        user_repo = AsyncMock()
        user_repo.read_one.return_value = None
        user_repo_cls.return_value = user_repo

        result = await UserService.get_user_by_id(async_session_mock, "missing-id")

        assert result is None
        user_repo.read_one.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_user_success(async_session_mock):
    user_id = "user-id-1"
    existing_user = SimpleNamespace(
        id=user_id,
        email="old@example.com",
        phone="123",
        first_name="Old",
        last_name="Name",
    )
    updated_user = SimpleNamespace(
        id=user_id,
        email="new@example.com",
        phone="456",
        first_name="New",
        last_name="Name",
    )

    update_data = UserUpdate(
        email="new@example.com",
        phone="456",
        first_name="New",
        last_name="Name",
    )

    with patch("app.services.user.UserRepository") as user_repo_cls, patch(
        "app.services.user.hash_password", return_value="hashed"
    ):
        user_repo = AsyncMock()
        user_repo.read_one.side_effect = [existing_user, None]
        user_repo.update.return_value = updated_user
        user_repo_cls.return_value = user_repo

        result = await UserService.update_user(async_session_mock, user_id, update_data)

        assert result.email == update_data.email
        assert result.phone == update_data.phone
        user_repo.update.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_user_not_found(async_session_mock):
    user_id = "missing-id"
    update_data = UserUpdate(first_name="New")

    with patch("app.services.user.UserRepository") as user_repo_cls:
        user_repo = AsyncMock()
        user_repo.read_one.return_value = None
        user_repo_cls.return_value = user_repo

        with pytest.raises(UserNotFoundError):
            await UserService.update_user(async_session_mock, user_id, update_data)


@pytest.mark.asyncio
async def test_delete_user_success(async_session_mock):
    user_id = "user-id-1"

    with patch("app.services.user.UserRepository") as user_repo_cls:
        user_repo = AsyncMock()
        user_repo.delete.return_value = True
        user_repo_cls.return_value = user_repo

        result = await UserService.delete_user(async_session_mock, user_id)

        assert result is True
        user_repo.delete.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_user_not_found(async_session_mock):
    user_id = "missing-id"

    with patch("app.services.user.UserRepository") as user_repo_cls:
        user_repo = AsyncMock()
        user_repo.delete.return_value = False
        user_repo_cls.return_value = user_repo

        with pytest.raises(UserNotFoundError):
            await UserService.delete_user(async_session_mock, user_id)


