from fastapi import APIRouter, HTTPException, Depends, Query

from app.services.gestionusuarios.eliminarusuario import eliminar_usuario
from app.security.permissions import require_role
from app.security.dependencies import get_current_user
from app.schemas.authenticated_user import AuthenticatedUser

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)

@router.delete(
    "/eliminar",
    dependencies=[Depends(require_role("PERMISO_ELIMINAR_USUARIOS"))]
)
async def delete_usuario(
    user_id: str = Query(..., description="ID del usuario a eliminar"),
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    """
    Elimina un usuario de Keycloak y BD.
    """
    
    try:
        resultado = await eliminar_usuario(user_id)
        return resultado
    
    except Exception as e:
        error_str = str(e)
        
        if "no existe" in error_str:
            raise HTTPException(
                status_code=404,
                detail=error_str
            )
        
        raise HTTPException(
            status_code=500,
            detail=f"Error al eliminar usuario: {error_str}"
        )
