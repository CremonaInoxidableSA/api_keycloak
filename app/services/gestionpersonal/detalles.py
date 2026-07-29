import httpx
from app.schemas.authenticated_user import AuthenticatedUser
from app.services.keycloak_admin import (
    get_admin_base_url,
    get_admin_token
)

async def procesar_detalles(user: AuthenticatedUser):
    """
    Procesa los datos del usuario autenticado para retornar
    información estructurada sobre módulos, submódulos y permisos.
    También obtiene los grupos a los cuales pertenece el usuario.
    
    Args:
        user: Usuario autenticado con sus roles
    
    Returns:
        Dict con información procesada del usuario
    """
    
    roles = user.roles if user.roles else []
    
    modulos = []
    submodulos = []
    permisos = []
    
    for rol in roles:
        if rol.startswith("MODULO_"):
            modulos.append(rol)
        elif rol.startswith("SUBMODULO_"):
            submodulos.append(rol)
        elif rol.startswith("PERMISO_"):
            permisos.append(rol)
    
    grupos = []
    try:
        token = await get_admin_token()
        
        headers = {
            "Authorization": f"Bearer {token}"
        }
        
        grupos_url = (
            f"{get_admin_base_url()}"
            f"/users/{user.id}/groups"
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
    
    except Exception as e:
        grupos = []
    
    return {
        "email": user.email,
        "nombre": user.first_name,
        "apellido": user.last_name,
        "legajo": 1231512,
        "dni": 95218923,
        "grupos": grupos,
        "modulos": modulos,
        "submodulos": submodulos,
        "permisos": permisos
    }
