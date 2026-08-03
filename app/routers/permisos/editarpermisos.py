from fastapi import APIRouter, HTTPException, Depends

from app.schemas.edit_permiso import EditPermisoRequest
from app.services.gestionpermisos.editarpermisos import editar_permiso
from app.security.permissions import require_role
from app.security.dependencies import get_current_user
from app.schemas.authenticated_user import AuthenticatedUser

router = APIRouter(
    prefix="/permisos",
    tags=["Permisos"]
)

@router.put(
    "/editar",
    dependencies=[Depends(require_role("PERMISO_EDITAR_PERMISOS"))]
)
async def editar_permiso_endpoint(
    permiso_nombre: str,
    data: EditPermisoRequest,
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    """
    Edita un permiso existente.
    
    Parámetros:
    - permiso_nombre: Nombre actual del permiso en Keycloak
    - data: Datos a actualizar (todos opcionales)
    """
    
    try:
        resultado = await editar_permiso(
            permiso_nombre=permiso_nombre,
            nuevo_nombre=data.nombre,
            descripcion=data.descripcion
        )
        
        return resultado
    
    except Exception as e:
        error_str = str(e)
        
        if "no existe" in error_str:
            raise HTTPException(
                status_code=404,
                detail=error_str
            )
        
        if "ya existe" in error_str or "prefijo" in error_str:
            raise HTTPException(
                status_code=400,
                detail=error_str
            )
        
        if "Debe proporcionar" in error_str:
            raise HTTPException(
                status_code=400,
                detail=error_str
            )
        
        raise HTTPException(
            status_code=500,
            detail=f"Error al editar permiso: {error_str}"
        )
