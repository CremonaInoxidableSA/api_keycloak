from pydantic import BaseModel
from typing import Optional


class DetailPermisoResponse(BaseModel):
    """
    Esquema de respuesta para detalles de un permiso.
    Contiene nombre y descripción del permiso.
    """
    nombre: str
    descripcion: Optional[str] = None

    class Config:
        from_attributes = True
