import httpx
from app.services.keycloak_admin import (
    get_admin_base_url,
    get_admin_token
)

async def obtener_grupos_realm():
    """
    Obtiene la lista de grupos del realm que comienzan con "GRUPO_".
    
    Returns:
        List con los nombres de los grupos disponibles
    """
    
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
    
    grupos = [
        {
            "id": g["id"],
            "nombre": g["name"]
        }
        for g in grupos_data
        if g["name"].startswith("GRUPO_")
    ]
    
    return grupos
