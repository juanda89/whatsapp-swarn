import os
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import JSON

# Configuración de la base de datos PostgreSQL
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://jdvs:-dadada-@localhost:5432/whatsapp_swarn")
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# Modelo para la memoria conversacional persistente
class ConversationMemory(Base):
    __tablename__ = "conversation_memories"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)       # identificador del usuario (ej: número de WhatsApp)
    agent_name = Column(String, index=True)    # nombre del agente
    messages = Column(JSON)                    # historial de mensajes en formato JSON (lista de {"role": ..., "content": ...})

# Crear tablas (si no existen)
Base.metadata.create_all(bind=engine)
