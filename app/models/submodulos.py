from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.config.db import Base
from .grupos_submodulos import grupos_submodulos


class Submodulos(Base):
    __tablename__ = "submodulos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    modulo_id = Column(Integer, ForeignKey("modulos.id", ondelete="CASCADE"), nullable=False)
    nombre = Column(String(100), nullable=False)
    path = Column(String(255), nullable=False, unique=True)
    icono = Column(String(255), nullable=True)

    modulo = relationship("Modulos", back_populates="submodulos")
    grupos = relationship("Grupos", secondary=grupos_submodulos, back_populates="submodulos")