from pydantic import BaseModel
from typing import Optional

class EditSubmoduleRequest(BaseModel):
    
    modulo_padre: Optional[str] = None
    
    path: Optional[str] = None
    
    icono: Optional[str] = None
