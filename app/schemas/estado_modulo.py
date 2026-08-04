from pydantic import BaseModel


class EstadoModuloRequest(BaseModel):
    nombre: str

    habilitado: bool