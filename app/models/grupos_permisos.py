from sqlalchemy import Table, Column, Integer, ForeignKey
from app.config.db import Base

grupos_permisos = Table(
    "grupos_permisos",
    Base.metadata,
    Column("grupo_id", Integer, ForeignKey("grupos.id", ondelete="CASCADE"), primary_key=True),
    Column("permiso_id", Integer, ForeignKey("permisos.id", ondelete="CASCADE"), primary_key=True),
)
