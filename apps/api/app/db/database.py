# Connecting Database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL=os.getenv("DATABASE_URL")

engine=create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    connect_args={"keepalives": 1, "keepalives_idle": 30, "keepalives_interval": 10, "keepalives_count": 5}
)

SessionLocal=sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)