from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging_config import get_logger
from app.dependencies.database import get_db
from app.dependencies.token import (
    get_access_token_from_cookie,
    validate_refresh_token,
)
from app.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
)
from app.schemas.user import UserResponse
from app.services.auth import auth_service

router = APIRouter(tags=["auth"])
logger = get_logger("auth_router")


@router.post("/register", status_code=201)
async def register(
    request: Request,
    response: Response,
    register_data: RegisterRequest,
    session: AsyncSession = Depends(get_db),
) -> JSONResponse:
    """
    Register a new user and return tokens.
    """
    logger.info(f"Registration request for email: {register_data.email}")

    user, tokens = await auth_service.register(request, session, register_data)
    auth_service.set_tokens_in_cookies(response, tokens)

    logger.info(f"User registered successfully: {user.id}")
    
    response_data = {
        "user": UserResponse.model_validate(user).model_dump(),
        "tokens": TokenResponse(**tokens.model_dump()).model_dump(),
    }
    
    return JSONResponse(content=response_data, status_code=201)


@router.post("/login")
async def login(
    request: Request,
    response: Response,
    login_data: LoginRequest,
    session: AsyncSession = Depends(get_db),
) -> JSONResponse:
    """
    Authenticate user and return tokens.
    """
    logger.info(f"Login request for email: {login_data.email}")

    user, tokens = await auth_service.login(request, session, login_data)
    auth_service.set_tokens_in_cookies(response, tokens)

    logger.info(f"User logged in successfully: {user.id}")
    
    response_data = {
        "user": UserResponse.model_validate(user).model_dump(),
        "tokens": TokenResponse(**tokens.model_dump()).model_dump(),
    }
    
    return JSONResponse(content=response_data)


@router.post("/refresh")
async def refresh(
    request: Request,
    response: Response,
    refresh_token: str = Depends(validate_refresh_token),
    session: AsyncSession = Depends(get_db),
) -> JSONResponse:
    """
    Refresh access token using refresh token.
    """
    logger.info("Token refresh request")

    tokens = await auth_service.refresh_token(session, refresh_token)
    auth_service.set_tokens_in_cookies(response, tokens)

    logger.info("Token refreshed successfully")
    
    return JSONResponse(content=tokens.model_dump())


@router.post("/logout")
async def logout(
    request: Request,
    response: Response,
    access_token: str = Depends(get_access_token_from_cookie),
    session: AsyncSession = Depends(get_db),
) -> JSONResponse:
    """
    Logout user by blacklisting tokens.
    """
    logger.info("Logout request")

    await auth_service.logout(request, session, access_token)
    auth_service.clear_tokens_in_cookies(response)

    logger.info("User logged out successfully")
    
    return JSONResponse(content={"detail": "Logged out successfully"})

