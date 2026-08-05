import httpx
from app.services.keycloak_admin import (
    get_admin_base_url,
    get_admin_token,
    get_group_roles
)


async def obtener_detalles_grupo(nombre_grupo: str):
    """
    Obtiene los detalles de un grupo incluyendo:
    - nombre del grupo
    - permisos asignados (roles que comienzan con PERMISO_)
    - módulos asignados (roles que comienzan con MODULO_)
    - submódulos asignados (roles que comienzan con SUBMODULO_)
    
    Args:
        nombre_grupo: Nombre del grupo (ej: GRUPO_ADMINISTRADOR)
    
    Returns:
        dict con estructura {nombre, permisos, modulos, submodulos}
    
    Raises:
        Exception: Si el grupo no existe o hay error al obtener datos
    """
    
    try:
        token = await get_admin_token()
        
        headers = {
            "Authorization": f"Bearer {token}"
        }
        
        # Obtener el grupo por nombre
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
            if grupo["name"] == nombre_grupo:
                grupo_encontrado = grupo
                break
        
        if not grupo_encontrado:
            raise Exception(f"El grupo '{nombre_grupo}' no existe.")
        
        grupo_id = grupo_encontrado["id"]
        
        roles = await get_group_roles(grupo_id)
        
        permisos = []
        modulos = []
        submodulos = []
        
        for rol in roles:
            if rol.startswith("PERMISO_"):
                permisos.append(rol)
            elif rol.startswith("MODULO_"):
                modulos.append(rol)
            elif rol.startswith("SUBMODULO_"):
                submodulos.append(rol)
        
        return {
            "nombre": nombre_grupo,
            "permisos": permisos,
            "modulos": modulos,
            "submodulos": submodulos
        }
    
    except Exception as e:
        raise Exception(f"Error al obtener detalles del grupo: {str(e)}")
