from fastapi import APIRouter, HTTPException, Depends

from app.schemas.estado_user import EstadoUserRequest

from app.services.keycloak_admin import get_user

from app.services.gestionusuarios.estadousuario import estado_user_keycloak

from app.security.permissions import require_role
from app.schemas.authenticated_user import AuthenticatedUser
from app.security.dependencies import get_current_user

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)

@router.put(
    "/{user_id}/habilitar",
    dependencies=[Depends(require_role("HABILITAR_USUARIOS"))]
)
async def enable_user(
    user_id: str,
    current_user: AuthenticatedUser = Depends(get_current_user)
):

    try:
        user_data = await get_user(user_id)
        
        if user_data.get("enabled", False):
            return {
                "message": "El usuario ya se encuentra habilitado"
            }
        
        from app.schemas.estado_user import EstadoUserRequest as UpdateRequest
        
        enable_data = UpdateRequest(habilitado=True)
        
        await estado_user_keycloak(
            user_id=user_id,
            data=enable_data
        )

        return {
            "message": "Usuario habilitado correctamente",
            "user_id": user_id
        }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.put(
    "/{user_id}/deshabilitar",
    dependencies=[Depends(require_role("DESHABILITAR_USUARIOS"))]
)
async def disable_user(
    user_id: str,
    current_user: AuthenticatedUser = Depends(get_current_user)
):

    try:
        user_data = await get_user(user_id)
        
        if not user_data.get("enabled", False):
            return {
                "message": "El usuario ya se encuentra deshabilitado"
            }
        
        realm_roles = user_data.get("realm_roles", [])
        if "SUPERADMIN" in realm_roles:
            raise HTTPException(
                status_code=403,
                detail="No se puede deshabilitar un usuario con rol SUPERADMIN"
            )
        
        from app.schemas.estado_user import EstadoUserRequest as UpdateRequest
        
        disable_data = UpdateRequest(habilitado=False)
        
        await estado_user_keycloak(
            user_id=user_id,
            data=disable_data
        )

        return {
            "message": "Usuario deshabilitado correctamente",
            "user_id": user_id
        }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )