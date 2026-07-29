import httpx
from app.services.keycloak_admin import (
    get_admin_base_url,
    get_admin_token
)


async def obtener_lista_usuarios(numero_pagina: int = 1, filtro: str = None):
    """
    Obtiene la lista de usuarios de Keycloak con paginación y filtro.
    
    Args:
        numero_pagina: Número de página (empezando desde 1)
        filtro: String para filtrar usuarios por email, nombre o apellido
    
    Returns:
        Tupla con (lista de usuarios, total de usuarios que coinciden)
    
    Raises:
        Exception: Si hay error al conectar con Keycloak
    """
    
    # Validar que numero_pagina sea válido
    if numero_pagina < 1:
        numero_pagina = 1
    
    # Calcular skip basado en el número de página
    usuarios_por_pagina = 10
    skip = (numero_pagina - 1) * usuarios_por_pagina
    
    try:
        token = await get_admin_token()
        
        headers = {
            "Authorization": f"Bearer {token}"
        }
        
        # URL para obtener usuarios sin límite inicial (necesitamos filtrar en memoria)
        url = (
            f"{get_admin_base_url()}"
            f"/users"
        )
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url,
                headers=headers
            )
            
            response.raise_for_status()
            
            usuarios = response.json()
        
        # Procesar usuarios para incluir grupos
        usuarios_procesados = []
        
        for usuario in usuarios:
            # Aplicar filtro si se proporciona
            if filtro:
                email = usuario.get("email", "").lower()
                nombre = usuario.get("firstName", "").lower()
                apellido = usuario.get("lastName", "").lower()
                filtro_lower = filtro.lower()
                
                # Verificar si el filtro coincide en alguno de los campos
                if not (filtro_lower in email or filtro_lower in nombre or filtro_lower in apellido):
                    continue
            
            user_id = usuario.get("id")
            
            # Obtener grupos del usuario
            grupos_url = (
                f"{get_admin_base_url()}"
                f"/users/{user_id}/groups"
            )
            
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
            
            usuario_procesado = {
                "id": usuario.get("id"),
                "email": usuario.get("email"),
                "nombre": usuario.get("firstName"),
                "apellido": usuario.get("lastName"),
                "enabled": usuario.get("enabled"),
                "grupos": grupos
            }
            
            usuarios_procesados.append(usuario_procesado)
        
        # Aplicar paginación: retornar 10 usuarios de la página especificada
        usuarios_paginados = usuarios_procesados[skip:skip + usuarios_por_pagina]
        
        return usuarios_paginados, len(usuarios_procesados)
    
    except httpx.HTTPError as e:
        raise Exception(f"Error al conectar con Keycloak: {str(e)}")
    except Exception as e:
        raise Exception(f"Error al obtener lista de usuarios: {str(e)}")
