from sqlalchemy import Table, Column, Integer, ForeignKey
from app.config.db import Base

usuarios_grupos = Table(
    "usuarios_grupos",
    Base.metadata,
    Column("usuario_id", Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), primary_key=True),
    Column("grupo_id", Integer, ForeignKey("grupos.id", ondelete="CASCADE"), primary_key=True),
)
