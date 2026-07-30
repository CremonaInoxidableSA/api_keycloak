from fastapi import APIRouter, HTTPException, Depends

from app.schemas.edit_user import UpdateUserRequest
from app.services.gestionusuarios.editarusuario import editar_usuario as editar_usuario_servicio
from app.security.permissions import require_role
from app.security.dependencies import get_current_user
from app.schemas.authenticated_user import AuthenticatedUser

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)

@router.put(
    "/editar",
    dependencies=[Depends(require_role("EDITAR_USUARIOS"))]
)
async def editar_usuario(
    user_id: str,
    data: UpdateUserRequest,
    current_user: AuthenticatedUser = Depends(get_current_user)
):
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
