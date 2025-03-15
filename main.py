from fastapi import FastAPI
from contextlib import asynccontextmanager
from mongoengine import connect, disconnect
from app.core.config import settings
from app.api.endpoints.bill_upload import router as bill_router
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup actions
    # Check if connection is successful
    try:
        connect(host=settings.MONGO_URI)
    except Exception as e:
        logger.error(f"Failed to connect to the database: {e}")
        raise
    logger.info("Database Connected.")
    yield
    # Shutdown actions
    disconnect()
    logger.info("Database Disconnected.")

app = FastAPI(
    title="solar-rooftop-rental-server",
    description="API for solar rooftop rental.",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(bill_router)
