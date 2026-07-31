import httpx
from app.services.keycloak_admin import (
    get_admin_base_url,
    get_admin_token
)

async def obtener_permisos_realm(numero_pagina: int = 1, filtro: str = None):
    """
    Obtiene la lista de permisos del realm que comienzan con "PERMISO_" con paginación y filtro.
    
    Args:
        numero_pagina: Número de página (empezando desde 1)
        filtro: String para filtrar permisos por nombre
    
    Returns:
        Tupla con (lista de permisos, total de permisos que coinciden)
    """
    
    if numero_pagina < 1:
        numero_pagina = 1
    
    permisos_por_pagina = 10
    skip = (numero_pagina - 1) * permisos_por_pagina
    
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
        
        permisos_procesados = []
        
        for rol in roles_data:
            if not rol["name"].startswith("PERMISO_"):
                continue
            
            if filtro:
                nombre = rol.get("name", "").lower()
                filtro_lower = filtro.lower()
                
                if filtro_lower not in nombre:
                    continue
            
            permiso_procesado = {
                "nombre": rol.get("name")
            }
            
            permisos_procesados.append(permiso_procesado)
        
        permisos_paginados = permisos_procesados[skip:skip + permisos_por_pagina]
        
        return permisos_paginados, len(permisos_procesados)
    
    except httpx.HTTPError as e:
        # Intentar obtener el body de la respuesta para debugging
        error_detail = str(e)
        if hasattr(e, 'response') and e.response:
            try:
                error_detail = e.response.text
            except:
                pass
        raise Exception(f"Error al conectar con Keycloak: {error_detail}")
    except Exception as e:
        raise Exception(f"Error al obtener lista de permisos: {str(e)}")

