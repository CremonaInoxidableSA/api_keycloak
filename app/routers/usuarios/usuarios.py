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

        user_id = await crear_usuario(
            username=data.email,
            email=data.email,
            first_name=data.nombre,
            last_name=data.apellido,
            password=data.password
        )

        return {
            "message": "Usuario creado correctamente",
            "id": user_id,
            "email": data.email
        }

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@router.put(
    "/{user_id}",
    dependencies=[Depends(require_role("EDITAR_USUARIOS"))]
)
async def update_user(
    user_id: str,
    data: UpdateUserRequest,
    current_user: AuthenticatedUser = Depends(get_current_user)
):

    await update_user_keycloak(
        user_id=user_id,
        data=data
    )

    return {
        "message": "Usuario actualizado correctamente"
    }