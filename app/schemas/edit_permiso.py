from pydantic import BaseModel
from typing import Optional

class EditPermisoRequest(BaseModel):
    
    nombre: Optional[str] = None
    
    descripcion: Optional[str] = None
