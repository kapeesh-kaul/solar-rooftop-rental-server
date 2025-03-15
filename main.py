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
    connect(host=settings.MONGO_URI)
    logger.info("Database Connected.")
    yield
    # Shutdown actions
    disconnect()
    logger.info("Database Disconnected.")

app = FastAPI(lifespan=lifespan)

app.include_router(bill_router)
