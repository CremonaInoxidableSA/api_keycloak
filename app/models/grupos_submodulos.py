from sqlalchemy import Table, Column, Integer, ForeignKey
from app.config.db import Base

grupos_submodulos = Table(
    "grupos_submodulos",
    Base.metadata,
    Column("grupo_id", Integer, ForeignKey("grupos.id", ondelete="CASCADE"), primary_key=True),
    Column("submodulo_id", Integer, ForeignKey("submodulos.id", ondelete="CASCADE"), primary_key=True)
)