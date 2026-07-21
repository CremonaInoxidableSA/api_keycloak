from pydantic import BaseModel
from typing import Optional

class EstadoUserRequest(BaseModel):

    habilitado: bool = None