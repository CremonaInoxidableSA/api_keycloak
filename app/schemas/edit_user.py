from pydantic import BaseModel
from typing import Optional

class UpdateUserRequest(BaseModel):

    email: Optional[str] = None

    nombre: Optional[str] = None

    apellido: Optional[str] = None