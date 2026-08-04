from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.config.db import Base

class Submodulos(Base):
    __tablename__ = "submodulos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    modulo_padre = Column(String(100), ForeignKey("modulos.nombre", ondelete="CASCADE"), nullable=False)
    nombre = Column(String(100), nullable=False,  unique=True)
    path = Column(String(255), nullable=False)
    icono = Column(String(255), nullable=True)
    habilitado = Column(Boolean, default=True, nullable=False)