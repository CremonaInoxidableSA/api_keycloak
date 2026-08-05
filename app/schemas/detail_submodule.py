from pydantic import BaseModel
from typing import Optional


class DetailSubmoduleResponse(BaseModel):
    """
    Esquema de respuesta para detalles de un submódulo.
    Contiene nombre, módulo padre, path e icono.
    """
    nombre: str
    modulo_padre: str
    path: str
    icono: Optional[str] = None

    class Config:
        from_attributes = True
