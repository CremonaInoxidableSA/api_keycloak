from pydantic import BaseModel, Field


class ChangePasswordRequest(BaseModel):
    """
    Schema para cambiar la contraseña del usuario autenticado.
    """
    
    password: str = Field(
        description="Nueva contraseña"
    )
    
    password_confirmation: str = Field(
        description="Confirmación de la nueva contraseña"
    )
