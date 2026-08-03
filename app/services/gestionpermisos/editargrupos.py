from typing import Optional, List
from app.services.keycloak_admin import (
    get_realm_role,
    get_group,
    get_group_roles,
    assign_realm_roles_to_group,
    remove_realm_roles_from_group,
    update_group_name
)


async def editar_grupo(
    nombre: str,
    permisos: Optional[List[str]] = None,
    modulos: Optional[List[str]] = None,
    submodulos: Optional[List[str]] = None
):
    """
    Edita un grupo en Keycloak.
    """
    
    try:
        grupo = await get_group(nombre)
    except Exception:
        raise Exception(f"El grupo '{nombre}' no existe en Keycloak")
    
    grupo_id = grupo["id"]
    roles_actuales = await get_group_roles(grupo_id)
    
    roles_a_asignar = []
    
    if permisos or modulos or submodulos:
        if permisos:
            for permiso in permisos:
                try:
                    await get_realm_role(permiso)
                    roles_a_asignar.append(permiso)
                except Exception:
                    raise Exception(f"El permiso '{permiso}' no existe en Keycloak")
        
        if modulos:
            for modulo in modulos:
                try:
                    await get_realm_role(modulo)
                    roles_a_asignar.append(modulo)
                except Exception:
                    raise Exception(f"El módulo '{modulo}' no existe en Keycloak")
        
        if submodulos:
            for submodulo in submodulos:
                try:
                    await get_realm_role(submodulo)
                    roles_a_asignar.append(submodulo)
                except Exception:
                    raise Exception(f"El submódulo '{submodulo}' no existe en Keycloak")
        
        if roles_actuales:
            try:
                await remove_realm_roles_from_group(grupo_id, roles_actuales)
            except Exception as e:
                raise Exception(f"Error al remover roles del grupo: {str(e)}")
        
        if roles_a_asignar:
            try:
                await assign_realm_roles_to_group(grupo_id, roles_a_asignar)
            except Exception as e:
                raise Exception(f"Error al asignar roles al grupo: {str(e)}")
    
    if nombre is not None:
        try:
            grupo_actualizado = await update_group_name(grupo_id, nombre)
            nombre_grupo = grupo_actualizado.get("name", nombre)
        except Exception as e:
            raise Exception(f"Error al actualizar nombre del grupo: {str(e)}")
    else:
        nombre_grupo = nombre
    
    return {
        "id": grupo_id,
        "nombre": nombre_grupo,
        "roles_asignados": roles_a_asignar if (permisos or modulos or submodulos) else roles_actuales,
        "detail": "Grupo actualizado exitosamente"
    }
