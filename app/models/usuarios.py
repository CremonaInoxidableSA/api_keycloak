from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.config.db import Base
from .usuarios_grupos import usuarios_grupos


class Usuarios(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), nullable=True, unique=True, index=True)
    username = Column(String(100), nullable=True, unique=True, index=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    habilitado = Column(Boolean, nullable=False, default=True)
    legajo = Column(Integer, nullable=True, unique=True)
    dni = Column(Integer, nullable=True)
    cambiar_contra = Column(Boolean, nullable=False, default=False)

    grupos = relationship("Grupos", secondary=usuarios_grupos, back_populates="usuarios")