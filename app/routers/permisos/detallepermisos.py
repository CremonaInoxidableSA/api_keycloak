from fastapi import APIRouter, HTTPException, Depends, Query

from app.services.gestionpermisos.detallepermisos import obtener_detalles_permiso
from app.security.permissions import require_role
from app.security.dependencies import get_current_user
from app.schemas.authenticated_user import AuthenticatedUser

router = APIRouter(
    prefix="/permisos",
    tags=["Permisos"]
)


@router.get(
    "/detalle",
    dependencies=[Depends(require_role("PERMISO_CONSULTAR_PERMISOS"))]
)
async def get_detalles_permiso(
    nombre: str = Query(..., description="Nombre del permiso a consultar:"),
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    """
    Obtiene los detalles de un permiso específico.
    """
    
    try:
        detalles = await obtener_detalles_permiso(nombre)
        return detalles
    
    except Exception as e:
        error_str = str(e)
        
        if "no existe" in error_str:
            raise HTTPException(
                status_code=404,
                detail=error_str
            )
        
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener detalles del permiso: {error_str}"
        )
