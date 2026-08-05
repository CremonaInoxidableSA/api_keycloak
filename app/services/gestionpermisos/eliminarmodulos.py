import httpx

from app.services.funcioneskeycloak.get_admin_base_url import get_admin_base_url
from app.services.funcioneskeycloak.get_admin_token import get_admin_token

from app.config.db import SessionLocal
from app.models.submodulos import Submodulos
from app.models.modulos import Modulos


async def eliminar_modulo(nombre_modulo: str):
    """
    Elimina un módulo de Keycloak y BD.
    Previamente elimina todos los submódulos asociados.
    """
    
    try:
        token = await get_admin_token()
        
        headers = {
            "Authorization": f"Bearer {token}"
        }
        
        db = SessionLocal()
        
        modulo = db.query(Modulos).filter(
            Modulos.nombre == nombre_modulo
        ).first()
        
        if not modulo:
            db.close()
            raise Exception(f"El módulo '{nombre_modulo}' no existe en la base de datos")
        
        submodulos = db.query(Submodulos).filter(
            Submodulos.modulo_padre == nombre_modulo
        ).all()
        
        for submodulo in submodulos:
            roles_url = f"{get_admin_base_url()}/roles/{submodulo.nombre}"
            
            async with httpx.AsyncClient() as client:
                try:
                    response = await client.get(
                        roles_url,
                        headers=headers
                    )
                    response.raise_for_status()
                    
                    delete_response = await client.delete(
                        roles_url,
                        headers=headers
                    )
                    delete_response.raise_for_status()
                except Exception as role_error:
                    pass
        
        db.query(Submodulos).filter(
            Submodulos.modulo_padre == nombre_modulo
        ).delete()
        
        modulo_role_url = f"{get_admin_base_url()}/roles/{nombre_modulo}"
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    modulo_role_url,
                    headers=headers
                )
                response.raise_for_status()
                
                delete_response = await client.delete(
                    modulo_role_url,
                    headers=headers
                )
                delete_response.raise_for_status()
            except Exception as role_error:
                pass
        
        db.query(Modulos).filter(
            Modulos.nombre == nombre_modulo
        ).delete()
        
        db.commit()
        db.close()
        
        return {
            "detail": f"Módulo '{nombre_modulo}' y sus {len(submodulos)} submódulos eliminados exitosamente"
        }
    
    except Exception as e:
        db.rollback()
        db.close()
        raise Exception(f"Error al eliminar módulo: {str(e)}")
