import logging
import logging.config
import os

from fastapi import FastAPI
from app.routers import tables, reservations

log_config_path = os.path.join(os.path.dirname(__file__), "core/logging.conf")
logging.config.fileConfig(log_config_path, disable_existing_loggers=False)
logger = logging.getLogger("uvicorn")

app = FastAPI(title="Async Restaurant Booking API")

app.include_router(tables.router)
app.include_router(reservations.router)
