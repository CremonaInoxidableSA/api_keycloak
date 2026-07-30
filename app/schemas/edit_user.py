from pydantic import BaseModel
from typing import Optional, List

class UpdateUserRequest(BaseModel):

    email: Optional[str] = None

    nombre: Optional[str] = None

    apellido: Optional[str] = None
    
    legajo: Optional[int] = None
    
    dni: Optional[int] = None
    
    grupos: Optional[List[str]] = None
    
    habilitado: Optional[bool] = None
    
    cambiar_contraseña: Optional[bool] = None