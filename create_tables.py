# create_tables.py
from dotenv import load_dotenv
import os
from database import engine
from models import Base  # <--- AQUÍ está Base ahora

load_dotenv()
print("🔍 DATABASE_URL usada por SQLAlchemy:", os.getenv("DATABASE_URL"))

Base.metadata.create_all(bind=engine)
print("✅ Tablas creadas en la base de datos")

