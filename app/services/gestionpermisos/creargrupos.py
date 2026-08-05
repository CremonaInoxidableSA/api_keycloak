from typing import Optional, List
from app.services.keycloak_admin import (
    get_realm_role,
    create_group,
    assign_realm_roles_to_group
)


async def crear_grupo(
    nombre: str,
    permisos: Optional[List[str]] = None,
    modulos: Optional[List[str]] = None,
    submodulos: Optional[List[str]] = None
):
    """
    Crea un grupo en Keycloak con los permisos, módulos y submódulos asignados.
    """
    
    roles_a_asignar = []
    
    if permisos:
        for permiso in permisos:
            try:
                rol = await get_realm_role(permiso)
                roles_a_asignar.append(permiso)
            except Exception:
                raise Exception(f"El permiso '{permiso}' no existe.")
    
    if modulos:
        for modulo in modulos:
            try:
                rol = await get_realm_role(modulo)
                roles_a_asignar.append(modulo)
            except Exception:
                raise Exception(f"El módulo '{modulo}' no existe.")
    
    if submodulos:
        for submodulo in submodulos:
            try:
                rol = await get_realm_role(submodulo)
                roles_a_asignar.append(submodulo)
            except Exception:
                raise Exception(f"El submódulo '{submodulo}' no existe.")
    
    try:
        grupo = await create_group(nombre)
    except Exception as e:
        error_str = str(e)
        if "409" in error_str or "Conflict" in error_str:
            raise Exception(f"El grupo '{nombre}' ya existe en Keycloak")
        else:
            raise Exception(f"Error al crear grupo en Keycloak: {error_str}")
    
    if roles_a_asignar:
        try:
            await assign_realm_roles_to_group(
                group_id=grupo["id"],
                role_names=roles_a_asignar
            )
        except Exception as e:
            raise Exception(f"Error al asignar roles al grupo: {str(e)}")
    
    return {
        "id": grupo["id"],
        "nombre": grupo["name"],
        "roles_asignados": roles_a_asignar,
        "detail": "Grupo creado exitosamente"
    }
