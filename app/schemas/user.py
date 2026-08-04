from pydantic import BaseModel, EmailStr
from typing import Optional, List


class CreateUserRequest(BaseModel):

    email: EmailStr

    nombre: str

    apellido: str

    password: str

    dni: int | None = None

    legajo: int | None = None

    habilitado: bool = True

    grupos: Optional[List[str]] = None