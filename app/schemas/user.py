from pydantic import BaseModel, EmailStr


class CreateUserRequest(BaseModel):

    email: EmailStr

    nombre: str

    apellido: str

    password: str

    dni: int | None = None

    legajo: int | None = None

    habilitado: bool = True