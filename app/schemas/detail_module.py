from pydantic import BaseModel
from typing import Optional


class DetailModuleResponse(BaseModel):
    """
    Esquema de respuesta para detalles de un módulo.
    Contiene nombre, subdominio, path e icono.
    """
    nombre: str
    subdominio: str
    path: str
    icono: Optional[str] = None

    class Config:
        from_attributes = True
