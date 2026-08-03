from fastapi import APIRouter, HTTPException, Depends
import httpx

from app.schemas.estado_user import EstadoUserRequest

from app.services.keycloak_admin import get_user, get_admin_base_url, get_admin_token

from app.services.gestionusuarios.estadousuario import estado_user_keycloak

from app.security.permissions import require_role
from app.schemas.authenticated_user import AuthenticatedUser
from app.security.dependencies import get_current_user

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)

async def obtener_grupos_usuario(user_id: str, token: str):
    """
    Obtiene los grupos de un usuario específico.
    """
    try:
        headers = {
            "Authorization": f"Bearer {token}"
        }
        
        grupos_url = f"{get_admin_base_url()}/users/{user_id}/groups"
        
        async with httpx.AsyncClient() as client:
            grupos_response = await client.get(
                grupos_url,
                headers=headers
            )
            
            grupos_response.raise_for_status()
        
        grupos = [
            grupo["name"]
            for grupo in grupos_response.json()
        ]
        return grupos
    
    except Exception:
        return []

@router.put(
    "/habilitar-usuarios",
    dependencies=[Depends(require_role("PERMISO_HABILITAR_USUARIOS"))]
)
async def enable_user(
    user_id: str,
    current_user: AuthenticatedUser = Depends(get_current_user)
):

    try:
        user_data = await get_user(user_id)
        
        if user_data.get("enabled", False):
            return {
                "detail": "El usuario ya se encuentra habilitado"
            }
        
        from app.schemas.estado_user import EstadoUserRequest as UpdateRequest
        
        enable_data = UpdateRequest(habilitado=True)
        
        await estado_user_keycloak(
            user_id=user_id,
            data=enable_data
        )

        return {
            "detail": "Usuario habilitado correctamente",
            "user_id": user_id
        }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.put(
    "/deshabilitar-usuarios",
    dependencies=[Depends(require_role("PERMISO_DESHABILITAR_USUARIOS"))]
)
async def disable_user(
    user_id: str,
    current_user: AuthenticatedUser = Depends(get_current_user)
):

    try:
        user_data = await get_user(user_id)
        
        if not user_data.get("enabled", False):
            return {
                "detail": "El usuario ya se encuentra deshabilitado"
            }
        
        token = await get_admin_token()
        grupos = await obtener_grupos_usuario(user_id, token)
        
        if "GRUPO_SUPERADMIN" in grupos:
            raise HTTPException(
                status_code=403,
                detail="No se puede deshabilitar un usuario con el grupo SUPERADMIN"
            )
        
        from app.schemas.estado_user import EstadoUserRequest as UpdateRequest
        
        disable_data = UpdateRequest(habilitado=False)
        
        await estado_user_keycloak(
            user_id=user_id,
            data=disable_data
        )

        return {
            "detail": "Usuario deshabilitado correctamente",
            "user_id": user_id
        }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )