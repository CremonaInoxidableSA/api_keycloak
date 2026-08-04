from pydantic import BaseModel


class EstadoSubmoduloRequest(BaseModel):
    nombre: str

    habilitado: bool