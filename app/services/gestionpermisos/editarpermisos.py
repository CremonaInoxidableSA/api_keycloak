from typing import Optional

from app.services.funcioneskeycloak.get_realm_role import get_realm_role
from app.services.funcioneskeycloak.update_realm_role import update_realm_role

async def editar_permiso(
    permiso_nombre: str,
    nuevo_nombre: Optional[str] = None,
    descripcion: Optional[str] = None
):
    """
    Edita un permiso existente en Keycloak.
    """
    
    try:
        permiso = await get_realm_role(permiso_nombre)
        
        if not permiso:
            raise Exception(f"El permiso '{permiso_nombre}' no existe.")
        
        if nuevo_nombre is None and descripcion is None:
            raise Exception("Debe proporcionar al menos un valor a actualizar")
        
        if nuevo_nombre and not nuevo_nombre.startswith("PERMISO_"):
            raise Exception("El nuevo nombre del permiso debe contar con 'PERMISO_' de prefijo")
        
        nuevo_nombre_upper = nuevo_nombre.upper() if nuevo_nombre else permiso_nombre
        
        if nuevo_nombre and nuevo_nombre_upper != permiso_nombre:
            try:
                await get_realm_role(nuevo_nombre_upper)
                raise Exception(f"El nombre '{nuevo_nombre_upper}' ya existe en Keycloak")
            except Exception as e:
                if "ya existe en Keycloak" in str(e):
                    raise
        
        descripcion_actualizada = descripcion if descripcion is not None else permiso.get("description", "")
        
        permiso_actualizado = await update_realm_role(
            old_role_name=permiso_nombre,
            new_role_name=nuevo_nombre_upper,
            description=descripcion_actualizada
        )
        
        return {
            "detail": "Permiso actualizado exitosamente"
        }
    
    except Exception as e:
        error_str = str(e)
        raise Exception(error_str)
