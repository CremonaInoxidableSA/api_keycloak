import httpx

from app.services.funcioneskeycloak.get_admin_base_url import get_admin_base_url
from app.services.funcioneskeycloak.get_admin_token import get_admin_token

from app.config.db import SessionLocal
from app.models.submodulos import Submodulos


async def eliminar_submodulo(nombre_submodulo: str):
    """
    Elimina un submódulo de Keycloak y BD.
    """
    
    try:
        token = await get_admin_token()
        
        headers = {
            "Authorization": f"Bearer {token}"
        }
        
        db = SessionLocal()
        
        submodulo = db.query(Submodulos).filter(
            Submodulos.nombre == nombre_submodulo
        ).first()
        
        if not submodulo:
            db.close()
            raise Exception(f"El submódulo '{nombre_submodulo}' no existe en la base de datos")
        
        submodulo_role_url = f"{get_admin_base_url()}/roles/{nombre_submodulo}"
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    submodulo_role_url,
                    headers=headers
                )
                response.raise_for_status()
                
                delete_response = await client.delete(
                    submodulo_role_url,
                    headers=headers
                )
                delete_response.raise_for_status()
            except Exception as role_error:
                pass
        
        db.query(Submodulos).filter(
            Submodulos.nombre == nombre_submodulo
        ).delete()
        
        db.commit()
        db.close()
        
        return {"detail": f"Submódulo '{nombre_submodulo}' eliminado exitosamente"}
    
    except Exception as e:
        db.rollback()
        db.close()
        raise Exception(f"Error al eliminar submódulo: {str(e)}")
