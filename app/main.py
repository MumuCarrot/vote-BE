import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.middleware import LoggingMiddleware, RequestContextMiddleware
from app.core.logging_config import get_logger, setup_logging
from app.core.settings import settings
from app.routers.healthcheck import router as healthcheck_router

setup_logging()
logger = get_logger("app")

app = FastAPI(
    title="Election Backend",
    description="Backend for the Election System",
    version="0.1.0",
    docs_url="/docs",
)

logger.info("Application starting up...")

app.add_middleware(RequestContextMiddleware)
app.add_middleware(LoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.app_settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info("Middleware configuration completed")

app.include_router(healthcheck_router)

logger.info("Routers configuration completed")

if __name__ == "__main__":
    logger.info(f"Starting application on {settings.APP_HOST}:{settings.APP_PORT}")
    uvicorn.run(
        "app.main:app",
        host=settings.app_settings.APP_HOST,
        port=settings.app_settings.APP_PORT,
        reload=False,
        workers=1,
    )
