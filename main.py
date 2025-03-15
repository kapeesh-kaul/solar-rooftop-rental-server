from fastapi import FastAPI
from contextlib import asynccontextmanager
from mongoengine import connect, disconnect
from app.core.config import settings
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints.bill_upload import router as bill_router
from app.api.endpoints.user.validate import router as user_router
from app.api.endpoints.user.get import router as user_get_router
from app.api.endpoints.moderate_user import router as moderate_user_router
from app.api.endpoints.sam_process import router as sam_process_router
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

origins = ["*"]  # Allow all origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows specific origins
    allow_credentials=True,  # Allows cookies/auth headers
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

app.include_router(bill_router)
app.include_router(user_router)
app.include_router(user_get_router)
app.include_router(moderate_user_router)
app.include_router(sam_process_router)

