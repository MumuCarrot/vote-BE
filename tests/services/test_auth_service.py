from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import Request, Response

from app.exceptions.user import InvalidCredentialsError, UserNotFoundError
from app.schemas.auth import LoginRequest, RegisterRequest
from app.schemas.user import UserResponse
from app.services.auth import AuthService


def _build_request_with_ip(ip: str = "127.0.0.1") -> Request:
    scope = {"type": "http", "client": (ip, 12345)}
    return Request(scope)


@pytest.mark.asyncio
async def test_register_success(async_session_mock):
    register_data = RegisterRequest(
        email="test@example.com",
        phone="123456789",
        password="password123",
        first_name="John",
        last_name="Doe",
    )

    created_user_response = UserResponse(
        id="user-id-1",
        email=register_data.email,
        phone=register_data.phone,
        first_name=register_data.first_name,
        last_name=register_data.last_name,
        created_at=None,
    )

    user_model = SimpleNamespace(
        id="user-id-1",
        email=register_data.email,
        password_hash="hashed",
    )

    tokens = {
        "access_token": "access",
        "refresh_token": "refresh",
        "token_type": "bearer",
    }

    with patch(
        "app.services.auth.UserService.create_user",
        new=AsyncMock(return_value=created_user_response),
    ) as create_user_mock, patch(
        "app.services.auth.UserService.get_user_by_email",
        new=AsyncMock(return_value=user_model),
    ) as get_user_mock, patch(
        "app.services.auth.create_pair_tokens", return_value=tokens
    ) as create_tokens_mock:
        request = _build_request_with_ip()

        user, token_response = await AuthService.register(
            request, async_session_mock, register_data
        )

        create_user_mock.assert_awaited_once()
        get_user_mock.assert_awaited_once()
        create_tokens_mock.assert_called_once()

        assert user.id == created_user_response.id
        assert token_response.access_token == tokens["access_token"]


@pytest.mark.asyncio
async def test_register_user_not_found_after_create(async_session_mock):
    register_data = RegisterRequest(
        email="test@example.com",
        phone="123456789",
        password="password123",
        first_name="John",
        last_name="Doe",
    )

    created_user_response = UserResponse(
        id="user-id-1",
        email=register_data.email,
        phone=register_data.phone,
        first_name=register_data.first_name,
        last_name=register_data.last_name,
        created_at=None,
    )

    with patch(
        "app.services.auth.UserService.create_user",
        new=AsyncMock(return_value=created_user_response),
    ), patch(
        "app.services.auth.UserService.get_user_by_email",
        new=AsyncMock(return_value=None),
    ):
        request = _build_request_with_ip()

        with pytest.raises(UserNotFoundError):
            await AuthService.register(request, async_session_mock, register_data)


@pytest.mark.asyncio
async def test_login_success(async_session_mock):
    login_data = LoginRequest(email="test@example.com", password="password123")

    user_model = SimpleNamespace(
        id="user-id-1", email=login_data.email, password_hash="hashed"
    )
    tokens = {
        "access_token": "access",
        "refresh_token": "refresh",
        "token_type": "bearer",
    }

    with patch(
        "app.services.auth.UserService.get_user_by_email",
        new=AsyncMock(return_value=user_model),
    ) as get_user_mock, patch(
        "app.services.auth.LoginAttemptRepository"
    ) as login_attempt_repo_cls, patch(
        "app.services.auth.verify_password", return_value=True
    ) as verify_password_mock, patch(
        "app.services.auth.create_pair_tokens", return_value=tokens
    ) as create_tokens_mock:
        login_repo = AsyncMock()
        login_attempt_repo_cls.return_value = login_repo

        request = _build_request_with_ip()

        user_response, token_response = await AuthService.login(
            request, async_session_mock, login_data
        )

        get_user_mock.assert_awaited_once()
        verify_password_mock.assert_called_once()
        login_repo.create.assert_awaited()
        create_tokens_mock.assert_called_once()

        assert user_response.id == user_model.id
        assert token_response.access_token == tokens["access_token"]


@pytest.mark.asyncio
async def test_login_invalid_email(async_session_mock):
    login_data = LoginRequest(email="missing@example.com", password="password123")

    with patch(
        "app.services.auth.UserService.get_user_by_email",
        new=AsyncMock(return_value=None),
    ), patch(
        "app.services.auth.LoginAttemptRepository"
    ) as login_attempt_repo_cls:
        login_repo = AsyncMock()
        login_attempt_repo_cls.return_value = login_repo

        request = _build_request_with_ip()

        with pytest.raises(InvalidCredentialsError):
            await AuthService.login(request, async_session_mock, login_data)

        login_repo.create.assert_awaited_once()


@pytest.mark.asyncio
async def test_login_invalid_password(async_session_mock):
    login_data = LoginRequest(email="test@example.com", password="wrongpass")

    user_model = SimpleNamespace(
        id="user-id-1", email=login_data.email, password_hash="hashed"
    )

    with patch(
        "app.services.auth.UserService.get_user_by_email",
        new=AsyncMock(return_value=user_model),
    ), patch(
        "app.services.auth.LoginAttemptRepository"
    ) as login_attempt_repo_cls, patch(
        "app.services.auth.verify_password", return_value=False
    ) as verify_password_mock:
        login_repo = AsyncMock()
        login_attempt_repo_cls.return_value = login_repo

        request = _build_request_with_ip()

        with pytest.raises(InvalidCredentialsError):
            await AuthService.login(request, async_session_mock, login_data)

        verify_password_mock.assert_called_once()
        login_repo.create.assert_awaited_once()


@pytest.mark.asyncio
async def test_refresh_token_success(async_session_mock):
    refresh_token = "valid-refresh"
    tokens = {
        "access_token": "new-access",
        "refresh_token": "new-refresh",
        "token_type": "bearer",
    }
    user_model = SimpleNamespace(id="user-id-1")

    with patch(
        "app.services.auth.is_token_blacklisted",
        new=AsyncMock(return_value=False),
    ) as blacklist_check_mock, patch(
        "app.services.auth.get_token_subject", return_value="user-id-1"
    ) as get_subject_mock, patch(
        "app.services.auth.UserService.get_user_by_id",
        new=AsyncMock(return_value=user_model),
    ) as get_user_mock, patch(
        "app.services.auth.blacklist_token",
        new=AsyncMock(),
    ) as blacklist_token_mock, patch(
        "app.services.auth.create_pair_tokens", return_value=tokens
    ) as create_tokens_mock:
        result = await AuthService.refresh_token(async_session_mock, refresh_token)

        blacklist_check_mock.assert_awaited_once()
        get_subject_mock.assert_called_once_with(refresh_token)
        get_user_mock.assert_awaited_once()
        blacklist_token_mock.assert_awaited_once_with(refresh_token)
        create_tokens_mock.assert_called_once()

        assert result.access_token == tokens["access_token"]


@pytest.mark.asyncio
async def test_refresh_token_blacklisted(async_session_mock):
    refresh_token = "blacklisted-refresh"

    with patch(
        "app.services.auth.is_token_blacklisted",
        new=AsyncMock(return_value=True),
    ):
        with pytest.raises(InvalidCredentialsError):
            await AuthService.refresh_token(async_session_mock, refresh_token)


@pytest.mark.asyncio
async def test_logout_clears_tokens(async_session_mock):
    access_token = "access-token"
    request = _build_request_with_ip()
    request._cookies = {"refresh_token": "refresh-token"}

    with patch(
        "app.services.auth.blacklist_token",
        new=AsyncMock(),
    ) as blacklist_token_mock:
        result = await AuthService.logout(request, async_session_mock, access_token)

        assert result is True
        assert blacklist_token_mock.await_count >= 1


def test_set_tokens_in_cookies():
    response = Response()
    tokens = SimpleNamespace(
        access_token="access",
        refresh_token="refresh",
    )

    with patch("app.services.auth.settings") as settings_mock:
        settings_mock.app_settings.APP_SECURE_COOKIES = False
        settings_mock.auth_settings.ACCESS_TOKEN_EXPIRE_MINUTES = 5
        settings_mock.auth_settings.REFRESH_TOKEN_EXPIRE_DAYS = 1

        AuthService.set_tokens_in_cookies(response, tokens)

        raw_headers = [h for h in response.raw_headers if h[0].lower() == b"set-cookie"]
        decoded = [value.decode("latin1") for _, value in raw_headers]

        assert any("access_token=" in h for h in decoded)
        assert any("refresh_token=" in h for h in decoded)


def test_clear_tokens_in_cookies():
    response = Response()
    response.set_cookie("access_token", "access")
    response.set_cookie("refresh_token", "refresh")

    with patch("app.services.auth.settings") as settings_mock:
        settings_mock.app_settings.APP_SECURE_COOKIES = False

        AuthService.clear_tokens_in_cookies(response)

        assert response.headers is not None


