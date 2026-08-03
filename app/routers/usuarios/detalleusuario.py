from fastapi import APIRouter, HTTPException, Depends

from app.services.gestionusuarios.detalleusuario import procesar_detalles_usuario_por_id
from app.security.permissions import require_role
from app.security.dependencies import get_current_user
from app.schemas.authenticated_user import AuthenticatedUser

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)

@router.get(
    "/detalles",
    dependencies=[Depends(require_role("PERMISO_CONSULTAR_USUARIOS"))]
)
async def obtener_detalles_usuario(
    user_id: str,
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    """
    Obtiene los detalles de un usuario específico por su ID.
    Retorna información sobre módulos, submódulos, permisos, 
    grupos y datos de legajo/DNI.
    """
    try:
        detalles = await procesar_detalles_usuario_por_id(user_id)
        return detalles
    
    except Exception as e:
        error_str = str(e)
        
        if "no encontrado" in error_str:
            raise HTTPException(
                status_code=404,
                detail=error_str
            )
        
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener detalles del usuario: {error_str}"
        )
