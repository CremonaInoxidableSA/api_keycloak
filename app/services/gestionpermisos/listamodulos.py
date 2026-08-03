import httpx
from app.services.keycloak_admin import (
    get_admin_base_url,
    get_admin_token
)

async def obtener_modulos_realm(numero_pagina: int = 1, filtro: str = None):
    """
    Obtiene la lista de módulos del realm que comienzan con "MODULO_" con paginación y filtro.
    
    Args:
        numero_pagina: Número de página (empezando desde 1)
        filtro: String para filtrar módulos por nombre
    
    Returns:
        Tupla con (lista de módulos, total de módulos que coinciden)
    """
    
    if numero_pagina < 1:
        numero_pagina = 1
    
    modulos_por_pagina = 10
    skip = (numero_pagina - 1) * modulos_por_pagina
    
    try:
        token = await get_admin_token()
        
        headers = {
            "Authorization": f"Bearer {token}"
        }
        
        roles_url = f"{get_admin_base_url()}/roles"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                roles_url,
                headers=headers
            )
            
            response.raise_for_status()
        
        roles_data = response.json()
        
        modulos_procesados = []
        
        for rol in roles_data:
            if not rol["name"].startswith("MODULO_"):
                continue
            
            if filtro:
                nombre = rol.get("name", "").lower()
                filtro_lower = filtro.lower()
                
                if filtro_lower not in nombre:
                    continue
            
            modulo_procesado = {
                "nombre": rol.get("name")
            }
            
            modulos_procesados.append(modulo_procesado)
        
        modulos_paginados = modulos_procesados[skip:skip + modulos_por_pagina]
        
        return modulos_paginados, len(modulos_procesados)
    
    except httpx.HTTPError as e:
        error_detail = str(e)
        if hasattr(e, 'response') and e.response:
            try:
                error_detail = e.response.text
            except:
                pass
        raise Exception(f"Error al conectar con Keycloak: {error_detail}")
    except Exception as e:
        raise Exception(f"Error al obtener lista de módulos: {str(e)}")
