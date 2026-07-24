from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.config.db import Base

class Modulos(Base):
    __tablename__ = "modulos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False, unique=True)
    subdominio = Column(String(255), nullable=False)
    path = Column(String(255), nullable=False, unique=True)
    icono = Column(String(255), nullable=True)