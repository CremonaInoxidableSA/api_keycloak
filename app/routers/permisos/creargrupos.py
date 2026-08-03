from fastapi import APIRouter, HTTPException, Depends

from app.schemas.create_group import CreateGroupRequest
from app.services.gestionpermisos.creargrupos import crear_grupo
from app.security.permissions import require_role
from app.security.dependencies import get_current_user
from app.schemas.authenticated_user import AuthenticatedUser

router = APIRouter(
    prefix="/grupos",
    tags=["Permisos"]
)

@router.post(
    "/crear",
    dependencies=[Depends(require_role("PERMISO_CREAR_GRUPOS"))]
)
async def crear_grupo_endpoint(
    data: CreateGroupRequest,
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    """
    Crea un nuevo grupo en Keycloak con permisos, módulos y submódulos asignados.
    """
    
    try:
        resultado = await crear_grupo(
            nombre=data.nombre,
            permisos=data.permisos,
            modulos=data.modulos,
            submodulos=data.submodulos
        )
        
        return resultado
    
    except Exception as e:
        error_str = str(e)
        
        if "no existe" in error_str:
            raise HTTPException(
                status_code=404,
                detail=error_str
            )
        
        if "ya existe" in error_str:
            raise HTTPException(
                status_code=409,
                detail=error_str
            )
        
        raise HTTPException(
            status_code=500,
            detail=f"Error al crear grupo: {error_str}"
        )
