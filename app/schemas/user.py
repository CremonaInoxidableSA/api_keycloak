from pydantic import BaseModel, EmailStr


class CreateUserRequest(BaseModel):

    email: EmailStr

    nombre: str

    apellido: str

    password: str