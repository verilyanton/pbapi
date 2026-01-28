import os
import sys

from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, os.path.dirname(__file__))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from src.adapters.rest.fastapi_routes import HealthRouter, UserRouter, HomeRouter

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Plant-Based API",
    description="All things vegan and plant-based API",
    version="0.0.1",
)

app.include_router(HealthRouter)
app.include_router(UserRouter)
app.include_router(HomeRouter)

# Enable CORS for dashboard
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
