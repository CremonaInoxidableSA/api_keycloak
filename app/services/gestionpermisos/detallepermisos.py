import httpx

from app.services.funcioneskeycloak.get_admin_base_url import get_admin_base_url
from app.services.funcioneskeycloak.get_admin_token import get_admin_token
from app.services.funcioneskeycloak.get_realm_role import get_realm_role

async def obtener_detalles_permiso(nombre_permiso: str):
    """
    Obtiene los detalles de un permiso incluyendo:
    """
    
    try:
        rol = await get_realm_role(nombre_permiso)
        
        return {
            "nombre": rol.get("name", nombre_permiso),
            "descripcion": rol.get("description", "")
        }
    
    except Exception as e:
        raise Exception(f"Error al obtener detalles del permiso: {str(e)}")
