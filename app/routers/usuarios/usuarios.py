from fastapi import APIRouter, HTTPException, Depends

from app.schemas.user import CreateUserRequest
from app.schemas.edit_user import UpdateUserRequest

from app.services.keycloak_admin import get_user

from app.services.gestionusuarios.actualizarusuario import update_user_keycloak

from app.services.gestionusuarios.crearusuario import crear_usuario

from app.security.permissions import require_role
from app.schemas.authenticated_user import AuthenticatedUser
from app.security.dependencies import get_current_user

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)

@router.post(
    "/crear-usuario",
    dependencies=[Depends(require_role("CREAR_USUARIOS"))]
)
async def create_new_user(
    data: CreateUserRequest
):

    try:
        resultado = await crear_usuario(
            username=data.email,
            email=data.email,
            first_name=data.nombre,
            last_name=data.apellido,
            password=data.password,
            habilitado=data.habilitado,
            dni=data.dni,
            legajo=data.legajo
        )

        return resultado

    except Exception as e:
        error_str = str(e)
        
        if "Falla en creación general" in error_str:
            raise HTTPException(
                status_code=400,
                detail=error_str
            )
        elif "Falla en creación en base de datos" in error_str:
            raise HTTPException(
                status_code=400,
                detail=error_str
            )
        else:
            raise HTTPException(
                status_code=400,
                detail=str(e)
            )