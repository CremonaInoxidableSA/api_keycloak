import httpx

from app.services.funcioneskeycloak.get_admin_base_url import get_admin_base_url
from app.services.funcioneskeycloak.get_admin_token import get_admin_token

async def obtener_grupos_realm(numero_pagina: int = 1, filtro: str = None):
    """
    Obtiene la lista de grupos del realm que comienzan con "GRUPO_" con paginación y filtro.
    """
    
    if numero_pagina < 1:
        numero_pagina = 1
    
    grupos_por_pagina = 10
    skip = (numero_pagina - 1) * grupos_por_pagina
    
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
        
        grupos_procesados = []
        
        for grupo in grupos_data:
            if not grupo["name"].startswith("GRUPO_"):
                continue
            
            if filtro:
                nombre = grupo.get("name", "").lower()
                filtro_lower = filtro.lower()
                
                if filtro_lower not in nombre:
                    continue
            
            grupo_procesado = {
                "nombre": grupo.get("name")
            }
            
            grupos_procesados.append(grupo_procesado)
        
        grupos_paginados = grupos_procesados[skip:skip + grupos_por_pagina]
        
        return grupos_paginados, len(grupos_procesados)
    
    except httpx.HTTPError as e:
        raise Exception(f"Error al conectar con Keycloak: {str(e)}")
    except Exception as e:
        raise Exception(f"Error al obtener lista de grupos: {str(e)}")
