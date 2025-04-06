from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()  # 👈 ESTO ES CRUCIAL para que lea el .env

DATABASE_URL = os.getenv("DATABASE_URL")

print("🔍 DATABASE_URL usada por SQLAlchemy:", DATABASE_URL)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
