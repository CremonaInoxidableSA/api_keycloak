from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.config.db import Base
from .usuarios_grupos import usuarios_grupos
from .grupos_modulos import grupos_modulos
from .grupos_submodulos import grupos_submodulos
from .grupos_permisos import grupos_permisos


class Grupos(Base):
    __tablename__ = "grupos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False, unique=True)

    usuarios = relationship("Usuarios", secondary=usuarios_grupos, back_populates="grupos")
    modulos = relationship("Modulos", secondary=grupos_modulos, back_populates="grupos")
    submodulos = relationship("Submodulos", secondary=grupos_submodulos, back_populates="grupos")
    permisos = relationship("Permisos", secondary=grupos_permisos, back_populates="grupos")