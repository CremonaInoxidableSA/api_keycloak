from pydantic import BaseModel


class CreateSubmoduleRequest(BaseModel):
    
    modulo_padre: str

    nombre: str

    path: str
    
    icono: str | None = None