import httpx

from app.services.funcioneskeycloak.get_admin_base_url import get_admin_base_url
from app.services.funcioneskeycloak.get_admin_token import get_admin_token
from app.config.db import SessionLocal
from app.models.usuarios import Usuarios


async def eliminar_usuario(user_id: str):
    """
    Elimina un usuario de Keycloak y BD.
    """
    
    try:
        db = SessionLocal()
        
        usuario = db.query(Usuarios).filter(
            Usuarios.id == user_id
        ).first()
        
        if not usuario:
            db.close()
            raise Exception(f"El usuario con ID '{user_id}' no existe en la base de datos")
        
        token = await get_admin_token()
        
        headers = {
            "Authorization": f"Bearer {token}"
        }
        
        user_url = f"{get_admin_base_url()}/users/{user_id}"
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.delete(
                    user_url,
                    headers=headers
                )
                response.raise_for_status()
            except Exception as keycloak_error:
                pass
        
        db.query(Usuarios).filter(
            Usuarios.id == user_id
        ).delete()
        
        db.commit()
        db.close()
        
        return {
            "detail": f"Usuario con ID '{user_id}' eliminado exitosamente"
        }
    
    except Exception as e:
        db.rollback()
        db.close()
        raise Exception(f"Error al eliminar usuario: {str(e)}")
