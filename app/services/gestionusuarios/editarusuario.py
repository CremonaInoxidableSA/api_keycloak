import httpx
from typing import Optional, List
from app.services.keycloak_admin import (
    get_admin_base_url,
    get_admin_token
)
from app.services.gestionpermisos.listagrupos import obtener_grupos_realm
from app.config.db import SessionLocal
from app.models.usuarios import Usuarios

async def editar_usuario(
    user_id: str,
    email: Optional[str] = None,
    nombre: Optional[str] = None,
    apellido: Optional[str] = None,
    legajo: Optional[int] = None,
    dni: Optional[int] = None,
    grupos: Optional[List[str]] = None,
    habilitado: Optional[bool] = None,
    cambiar_contraseña: Optional[bool] = None
):
    """
    Edita los datos de un usuario de forma selectiva.
    Solo actualiza los campos que se proporcionen.
    
    Args:
        user_id: ID del usuario en Keycloak
        email: Email del usuario
        nombre: Nombre del usuario
        apellido: Apellido del usuario
        legajo: Legajo (solo base de datos)
        dni: DNI (solo base de datos)
        grupos: Lista de grupos a asignar
        habilitado: Habilitar/deshabilitar usuario
        cambiar_contraseña: Agregar/quitar UPDATE_PASSWORD de requiredActions
    
    Returns:
        Dict con información del usuario actualizado
    """
    
    token = await get_admin_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    # Actualizar datos en Keycloak
    user_url = f"{get_admin_base_url()}/users/{user_id}"
    body = {}
    
    if email is not None:
        body["email"] = email
    
    if nombre is not None:
        body["firstName"] = nombre
    
    if apellido is not None:
        body["lastName"] = apellido
    
    if habilitado is not None:
        body["enabled"] = habilitado
    
    if body:
        async with httpx.AsyncClient() as client:
            response = await client.put(
                user_url,
                json=body,
                headers=headers
            )
            response.raise_for_status()
    
    # Actualizar required actions si es necesario
    if cambiar_contraseña is not None:
        required_actions_url = f"{get_admin_base_url()}/users/{user_id}"
        
        async with httpx.AsyncClient() as client:
            # Obtener usuario actual
            get_response = await client.get(
                required_actions_url,
                headers=headers
            )
            get_response.raise_for_status()
            user_data = get_response.json()
            
            required_actions = user_data.get("requiredActions", [])
            
            if cambiar_contraseña and "UPDATE_PASSWORD" not in required_actions:
                required_actions.append("UPDATE_PASSWORD")
            elif not cambiar_contraseña and "UPDATE_PASSWORD" in required_actions:
                required_actions.remove("UPDATE_PASSWORD")
            
            # Actualizar required actions
            update_body = {"requiredActions": required_actions}
            response = await client.put(
                required_actions_url,
                json=update_body,
                headers=headers
            )
            response.raise_for_status()
    
    # Actualizar grupos si se proporcionan
    if grupos is not None:
        # Validar que los grupos existen
        grupos_disponibles_list = await obtener_grupos_realm()
        grupos_disponibles_names = {
            g["nombre"]
            for g in grupos_disponibles_list
        }
        
        # Verificar que todos los grupos solicitados existen
        grupos_invalidos = [
            g for g in grupos
            if g not in grupos_disponibles_names
        ]
        
        if grupos_invalidos:
            raise Exception(f"Los siguientes grupos no existen: {', '.join(grupos_invalidos)}")
        
        # Obtener grupos actuales
        grupos_url = f"{get_admin_base_url()}/users/{user_id}/groups"
        
        async with httpx.AsyncClient() as client:
            grupos_response = await client.get(
                grupos_url,
                headers=headers
            )
            grupos_response.raise_for_status()
            
            grupos_actuales = [
                g["id"]
                for g in grupos_response.json()
            ]
            
            # Eliminar grupos actuales
            for grupo_id in grupos_actuales:
                delete_response = await client.delete(
                    f"{grupos_url}/{grupo_id}",
                    headers=headers
                )
                delete_response.raise_for_status()
            
            # Obtener lista de todos los grupos disponibles
            all_grupos_url = f"{get_admin_base_url()}/groups"
            all_grupos_response = await client.get(
                all_grupos_url,
                headers=headers
            )
            all_grupos_response.raise_for_status()
            
            grupos_disponibles = {
                g["name"]: g["id"]
                for g in all_grupos_response.json()
            }
            
            # Asignar nuevos grupos
            for grupo_name in grupos:
                if grupo_name in grupos_disponibles:
                    grupo_id = grupos_disponibles[grupo_name]
                    join_response = await client.put(
                        f"{grupos_url}/{grupo_id}",
                        headers=headers
                    )
                    join_response.raise_for_status()
    
    # Actualizar datos en base de datos
    if legajo is not None or dni is not None:
        try:
            db = SessionLocal()
            usuario_db = db.query(Usuarios).filter(Usuarios.id == user_id).first()
            
            if usuario_db:
                if legajo is not None:
                    usuario_db.legajo = legajo
                if dni is not None:
                    usuario_db.dni = dni
                
                db.commit()
            
            db.close()
        except Exception as e:
            raise Exception(f"Error al actualizar datos en base de datos: {str(e)}")
    
    return {
        "id": user_id,
        "mensaje": "Usuario actualizado exitosamente"
    }
