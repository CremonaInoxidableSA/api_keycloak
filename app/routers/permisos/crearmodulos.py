from fastapi import APIRouter, HTTPException, Depends

from app.schemas.create_module import CreateModuleRequest
from app.services.gestionpermisos.crearmodulos import crear_modulo
from app.security.permissions import require_role
from app.schemas.authenticated_user import AuthenticatedUser
from app.security.dependencies import get_current_user

router = APIRouter(
    prefix="/modulos",
    tags=["Permisos"]
)

@router.post(
    "/crear",
    dependencies=[Depends(require_role("PERMISO_CREAR_MODULOS"))]
)
async def create_new_module(
    data: CreateModuleRequest,
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    """
    Crea un nuevo módulo.
    """

    try:
        resultado = await crear_modulo(
            nombre=data.nombre,
            subdominio=data.subdominio,
            path=data.path,
            icono=data.icono
        )

        return resultado

    except Exception as e:
        error_str = str(e)
        
        if "debe contar con 'MODULO_' de prefijo" in error_str:
            raise HTTPException(status_code=400, detail=error_str)
        elif "ya existe en Keycloak" in error_str:
            raise HTTPException(status_code=409, detail=error_str)
        elif "ya existe en la base de datos" in error_str:
            raise HTTPException(status_code=409, detail=error_str)
        elif "Error en Keycloak" in error_str or "Error en base de datos" in error_str:
            raise HTTPException(status_code=500, detail=error_str)
        else:
            raise HTTPException(status_code=500, detail=error_str)
