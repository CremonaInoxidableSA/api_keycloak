import httpx
import asyncio

from app.services.funcioneskeycloak.get_admin_base_url import get_admin_base_url
from app.services.funcioneskeycloak.get_admin_token import get_admin_token
from app.services.funcioneskeycloak.get_user import get_user

from app.config.db import SessionLocal
from app.models.usuarios import Usuarios

async def obtener_grupos_usuario(client: httpx.AsyncClient, user_id: str, headers: dict):
    """
    Obtiene los grupos de un usuario específico.
    """
    grupos_url = f"{get_admin_base_url()}/users/{user_id}/groups"
    
    try:
        response = await client.get(
            grupos_url,
            headers=headers
        )
        response.raise_for_status()
        
        grupos = [
            {"nombre": grupo.get("name")}
            for grupo in response.json()
        ]
        return grupos
    except Exception:
        return []

def obtener_datos_db(user_id: str):
    """
    Obtiene datos de la base de datos del usuario (legajo, dni).
    """
    legajo = 0
    dni = 0
    
    try:
        db = SessionLocal()
        usuario_db = db.query(Usuarios).filter(Usuarios.id == user_id).first()
        db.close()
        
        if usuario_db:
            legajo = usuario_db.legajo if usuario_db.legajo is not None else 0
            dni = usuario_db.dni if usuario_db.dni is not None else 0
    
    except Exception:
        pass
    
    return legajo, dni

async def procesar_detalles_usuario_por_id(user_id: str):
    """
    Obtiene los detalles de un usuario específico por su ID.
    """
    
    try:
        usuario_keycloak = await get_user(user_id)
    except Exception as e:
        raise Exception(f"Usuario con ID {user_id} no encontrado en Keycloak")
    
    roles = usuario_keycloak.get("realm_roles", [])
    
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
    
    required_actions = usuario_keycloak.get("requiredActions", [])
    cambiar_password = "UPDATE_PASSWORD" in required_actions
    
    token = await get_admin_token()
    
    grupos, (legajo, dni) = await asyncio.gather(
        obtener_grupos_usuario(httpx.AsyncClient(), user_id, {"Authorization": f"Bearer {token}"}),
        asyncio.to_thread(obtener_datos_db, user_id)
    )
    
    return {
        "id": user_id,
        "nombre": usuario_keycloak.get("firstName", ""),
        "apellido": usuario_keycloak.get("lastName", ""),
        "legajo": legajo,
        "dni": dni,
        "email": usuario_keycloak.get("email", ""),
        "grupos": grupos,
        "habilitado": usuario_keycloak.get("enabled", False),
        "cambiar_password": cambiar_password
    }