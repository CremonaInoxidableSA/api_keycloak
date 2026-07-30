from fastapi import APIRouter, HTTPException, Depends
import re

from app.schemas.edit_user import UpdateUserRequest
from app.services.gestionusuarios.editarusuario import editar_usuario as editar_usuario_servicio
from app.security.permissions import require_role
from app.security.dependencies import get_current_user
from app.schemas.authenticated_user import AuthenticatedUser

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)

def validar_email(email: str) -> bool:
    """
    Valida que el email tenga un formato correcto.
    """
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(patron, email) is not None

@router.put(
    "/editar",
    dependencies=[Depends(require_role("EDITAR_USUARIOS"))]
)
async def editar_usuario(
    user_id: str,
    data: UpdateUserRequest,
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    # Validar formato de email si se proporciona
    if data.email is not None and data.email != "":
        if not validar_email(data.email):
            raise HTTPException(
                status_code=400,
                detail="El formato del correo electrónico es inválido"
            )
    
    try:
        resultado = await editar_usuario_servicio(
            user_id=user_id,
            email=data.email,
            nombre=data.nombre,
            apellido=data.apellido,
            legajo=data.legajo,
            dni=data.dni,
            grupos=data.grupos,
            cambiar_contraseña=data.cambiar_contraseña
        )
        
        return resultado
    
    except Exception as e:
        error_str = str(e)
        
        if "no encontrado" in error_str:
            raise HTTPException(
                status_code=404,
                detail=error_str
            )
        
        raise HTTPException(
            status_code=500,
            detail=f"Error al editar usuario: {error_str}"
        )
