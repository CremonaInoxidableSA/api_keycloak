from sqlalchemy import Table, Column, Integer, ForeignKey
from app.config.db import Base

grupos_modulos = Table(
    "grupos_modulos",
    Base.metadata,
    Column("grupo_id", Integer, ForeignKey("grupos.id", ondelete="CASCADE"), primary_key=True),
    Column("modulo_id", Integer, ForeignKey("modulos.id", ondelete="CASCADE"), primary_key=True)
)