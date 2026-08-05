import httpx
from sqlalchemy import text

from app.services.funcioneskeycloak.create_realm_role import create_realm_role
from app.services.funcioneskeycloak.get_admin_base_url import get_admin_base_url
from app.services.funcioneskeycloak.get_admin_token import get_admin_token
from app.services.funcioneskeycloak.get_realm_role import get_realm_role

from app.core.config import settings


async def crear_permiso(
    nombre: str,
    descripcion: str = ""
):
    """
    Crea un permiso en Keycloak.
    """
    
    if not nombre.startswith("PERMISO_"):
        raise Exception("El permiso debe contar con 'PERMISO_' de prefijo.")
    
    role_name = nombre.upper()
    
    try:
        await get_realm_role(role_name)
        raise Exception("El permiso ya existe.")
    except Exception as e:
        error_str = str(e)
        if "ya existe en Keycloak" in error_str:
            raise
    
    try:
        await create_realm_role(
            role_name=role_name,
            description=descripcion
        )
    except Exception as e:
        error_str = str(e)
        if "409" in error_str or "Conflict" in error_str:
            raise Exception("El permiso ya existe.")
        else:
            raise Exception(f"Error en Keycloak: {error_str}")
    
    return {
        "detail": "Permiso creado exitosamente"
    }
