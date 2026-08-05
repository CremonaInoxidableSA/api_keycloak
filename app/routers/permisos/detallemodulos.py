from fastapi import APIRouter, HTTPException, Depends, Query

from app.services.gestionpermisos.detallemodulos import obtener_detalles_modulo
from app.security.permissions import require_role
from app.security.dependencies import get_current_user
from app.schemas.authenticated_user import AuthenticatedUser

router = APIRouter(
    prefix="/modulos",
    tags=["Permisos"]
)

@router.get(
    "/detalle",
    dependencies=[Depends(require_role("PERMISO_CONSULTAR_MODULOS"))]
)
async def get_detalles_modulo(
    nombre_modulo: str = Query(..., description="Nombre del módulo a consultar:"),
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    """
    Obtiene los detalles de un módulo específico.
    """
    
    try:
        detalles = await obtener_detalles_modulo(nombre_modulo)
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
            detail=f"Error al obtener detalles del módulo: {error_str}"
        )
