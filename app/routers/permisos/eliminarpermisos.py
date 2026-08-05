from fastapi import APIRouter, HTTPException, Depends, Query

from app.services.gestionpermisos.eliminarpermisos import eliminar_permiso
from app.security.permissions import require_role
from app.security.dependencies import get_current_user
from app.schemas.authenticated_user import AuthenticatedUser

router = APIRouter(
    prefix="/permisos",
    tags=["Permisos"]
)

@router.delete(
    "/eliminar",
    dependencies=[Depends(require_role("PERMISO_ELIMINAR_PERMISOS"))]
)
async def delete_permiso(
    nombre_permiso: str = Query(..., description="Nombre del permiso a eliminar"),
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    """
    Elimina un permiso de Keycloak.
    """
    
    try:
        resultado = await eliminar_permiso(nombre_permiso)
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
            detail=f"Error al eliminar permiso: {error_str}"
        )
