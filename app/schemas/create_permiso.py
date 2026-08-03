from pydantic import BaseModel


class CreatePermisoRequest(BaseModel):
    
    nombre: str
