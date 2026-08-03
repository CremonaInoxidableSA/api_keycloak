from pydantic import BaseModel


class CreateModuleRequest(BaseModel):
    
    nombre: str
    
    subdominio: str
    
    path: str
    
    icono: str | None = None
