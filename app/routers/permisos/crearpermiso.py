from fastapi import APIRouter, HTTPException, Depends

from app.schemas.create_permiso import CreatePermisoRequest
from app.services.gestionpermisos.crearpermisos import crear_permiso
from app.security.permissions import require_role
from app.schemas.authenticated_user import AuthenticatedUser
from app.security.dependencies import get_current_user

router = APIRouter(
    prefix="/permisos",
    tags=["Permisos"]
)

@router.post(
    "/crear-permiso",
    dependencies=[Depends(require_role("CREAR_PERMISOS"))]
)
async def create_new_permiso(
    data: CreatePermisoRequest,
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    """
    Crea un nuevo permiso.
    """

    try:
        resultado = await crear_permiso(
            nombre=data.nombre,
            descripcion=data.descripcion or ""
        )

        return resultado

    except Exception as e:
        error_str = str(e)
        
        if "debe contar con 'PERMISO_' de prefijo" in error_str:
            raise HTTPException(status_code=400, detail=error_str)
        elif "ya existe en Keycloak" in error_str:
            raise HTTPException(status_code=409, detail=error_str)
        else:
            raise HTTPException(status_code=500, detail=error_str)
