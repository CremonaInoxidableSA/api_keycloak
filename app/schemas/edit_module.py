from pydantic import BaseModel
from typing import Optional

class EditModuleRequest(BaseModel):
    
    subdominio: Optional[str] = None
    
    path: Optional[str] = None
    
    icono: Optional[str] = None
