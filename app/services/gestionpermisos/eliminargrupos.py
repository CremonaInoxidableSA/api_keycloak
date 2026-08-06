import httpx

from app.services.funcioneskeycloak.get_admin_base_url import get_admin_base_url
from app.services.funcioneskeycloak.get_admin_token import get_admin_token


async def eliminar_grupo(grupo_nombre: str):
    """
    Elimina un grupo de Keycloak.
    """
    
    try:
        token = await get_admin_token()
        
        headers = {
            "Authorization": f"Bearer {token}"
        }
        
        grupos_url = f"{get_admin_base_url()}/groups"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                grupos_url,
                headers=headers
            )
            
            response.raise_for_status()
        
        grupos_data = response.json()
        
        grupo_encontrado = None
        for grupo in grupos_data:
            if grupo["name"] == grupo_nombre:
                grupo_encontrado = grupo
                break
        
        if not grupo_encontrado:
            raise Exception(f"El grupo '{grupo_nombre}' no existe.")
        
        if grupo_nombre == "GRUPO_SUPERADMIN":
            raise Exception(f"No se puede eliminar el grupo '{grupo_nombre}'.")
        
        grupo_id = grupo_encontrado["id"]
        
        delete_url = f"{get_admin_base_url()}/groups/{grupo_id}"
        
        async with httpx.AsyncClient() as client:
            response = await client.delete(
                delete_url,
                headers=headers
            )
            
            response.raise_for_status()
        
        return {"detail": f"Grupo '{grupo_nombre}' eliminado exitosamente"}
    
    except Exception as e:
        raise Exception(f"Error al eliminar grupo: {str(e)}")
