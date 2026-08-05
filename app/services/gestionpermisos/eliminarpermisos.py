import httpx

from app.services.funcioneskeycloak.get_admin_base_url import get_admin_base_url
from app.services.funcioneskeycloak.get_admin_token import get_admin_token

async def eliminar_permiso(nombre_permiso: str):
    """
    Elimina un permiso de Keycloak.
    """
    
    try:
        token = await get_admin_token()
        
        headers = {
            "Authorization": f"Bearer {token}"
        }
        
        # Obtener el rol (permiso) de Keycloak
        permiso_url = f"{get_admin_base_url()}/roles/{nombre_permiso}"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                permiso_url,
                headers=headers
            )
            
            response.raise_for_status()
            
            # Eliminar el rol
            delete_response = await client.delete(
                permiso_url,
                headers=headers
            )
            
            delete_response.raise_for_status()
        
        return {"detail": f"Permiso '{nombre_permiso}' eliminado exitosamente"}
    
    except Exception as e:
        error_str = str(e)
        if "404" in error_str or "not found" in error_str.lower():
            raise Exception(f"El permiso '{nombre_permiso}' no existe.")
        raise Exception(f"Error al eliminar permiso: {error_str}")
