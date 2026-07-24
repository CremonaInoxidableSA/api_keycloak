from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.config.db import Base
from .grupos_modulos import grupos_modulos


class Modulos(Base):
    __tablename__ = "modulos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False, unique=True)
    subdominio = Column(String(255), nullable=False)
    path = Column(String(255), nullable=False, unique=True)
    icono = Column(String(255), nullable=True)

    submodulos = relationship("Submodulos", back_populates="modulo", cascade="all, delete-orphan")
    grupos = relationship("Grupos", secondary=grupos_modulos, back_populates="modulos")