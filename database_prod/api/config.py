import os
from dotenv import load_dotenv
from sqlalchemy.engine import URL

# Load environment variables from .env file
load_dotenv()

url = URL.create(
    drivername="postgresql",
    username=os.getenv("POSTGRES_USERNAME"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_NETWORK"),
    port=5432,
    database=os.getenv("POSTGRES_DATABASE")
)

class Config:
    DATABASE_URL = url