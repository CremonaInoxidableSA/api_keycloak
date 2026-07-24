from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.config.db import Base
from .grupos_permisos import grupos_permisos


class Permisos(Base):
    __tablename__ = "permisos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False, unique=True)
    descripcion = Column(String(255), nullable=False, unique=True)

    grupos = relationship("Grupos", secondary=grupos_permisos, back_populates="permisos")