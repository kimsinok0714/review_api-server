from contextlib import asynccontextmanager
import logging
from dotenv import load_dotenv
from app.gemini_client import ReviewAnalyzer
from app.schemas import ReviewRequest, ReviewResponse
from pathlib import Path

env_path = Path(__file__).resolve().parent

print(env_path)



