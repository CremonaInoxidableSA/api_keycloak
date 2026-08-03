from pydantic import BaseModel
from typing import Optional, List


class EditGroupRequest(BaseModel):
    
    permisos: Optional[List[str]] = None
    
    modulos: Optional[List[str]] = None
    
    submodulos: Optional[List[str]] = None
