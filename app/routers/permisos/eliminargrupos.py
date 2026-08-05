from fastapi import APIRouter, HTTPException, Depends, Query

from app.services.gestionpermisos.eliminargrupos import eliminar_grupo
from app.security.permissions import require_role
from app.security.dependencies import get_current_user
from app.schemas.authenticated_user import AuthenticatedUser

router = APIRouter(
    prefix="/grupos",
    tags=["Permisos"]
)


@router.delete(
    "/eliminar",
    dependencies=[Depends(require_role("PERMISO_ELIMINAR_GRUPOS"))]
)
async def delete_grupo(
    nombre_grupo: str = Query(..., description="Nombre del grupo a eliminar"),
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    """
    Elimina un grupo de Keycloak.
    """
    
    try:
        resultado = await eliminar_grupo(nombre_grupo)
        return resultado
    
    except Exception as e:
        error_str = str(e)
        
        if "no existe" in error_str:
            raise HTTPException(
                status_code=404,
                detail=error_str
            )
        
        if "No se puede eliminar" in error_str or "crítico" in error_str:
            raise HTTPException(
                status_code=400,
                detail=error_str
            )
        
        raise HTTPException(
            status_code=500,
            detail=f"Error al eliminar grupo: {error_str}"
        )
