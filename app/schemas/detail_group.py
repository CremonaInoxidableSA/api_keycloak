from pydantic import BaseModel
from typing import Optional, List


class DetailGroupResponse(BaseModel):
    """
    Esquema de respuesta para detalles de un grupo.
    Contiene el nombre del grupo, permisos, módulos y submódulos asociados.
    """
    nombre: str
    permisos: List[str]
    modulos: List[str]
    submodulos: List[str]

    class Config:
        from_attributes = True
