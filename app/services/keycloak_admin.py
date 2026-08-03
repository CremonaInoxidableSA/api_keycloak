import httpx
import json

from app.core.config import settings

def get_admin_base_url():
    return (
        f"{settings.KEYCLOAK_URL}"
        f"/admin/realms/"
        f"{settings.KEYCLOAK_REALM}"
    )


async def get_admin_token():

    url = (
        f"{settings.KEYCLOAK_URL}"
        f"/realms/{settings.KEYCLOAK_REALM}"
        "/protocol/openid-connect/token"
    )

    data = {
        "grant_type": "client_credentials",
        "client_id": settings.KEYCLOAK_ADMIN_CLIENT_ID,
        "client_secret": settings.KEYCLOAK_ADMIN_SECRET,
    }

    async with httpx.AsyncClient() as client:

        response = await client.post(
            url,
            data=data
        )

        response.raise_for_status()

        return response.json()["access_token"]


async def get_user(user_id: str):

    token = await get_admin_token()

    headers = {
        "Authorization": f"Bearer {token}"
    }

    user_url = (
        f"{get_admin_base_url()}"
        f"/users/{user_id}"
    )

    roles_url = (
        f"{get_admin_base_url()}"
        f"/users/{user_id}/role-mappings/realm"
    )

    async with httpx.AsyncClient() as client:

        user_response = await client.get(
            user_url,
            headers=headers
        )

        user_response.raise_for_status()

        roles_response = await client.get(
            roles_url,
            headers=headers
        )

        roles_response.raise_for_status()

    user = user_response.json()

    user["realm_roles"] = [
        role["name"]
        for role in roles_response.json()
    ]

    return user


async def get_realm_role(role_name: str):

    token = await get_admin_token()


    url = (
        f"{get_admin_base_url()}"
        f"/roles/{role_name}"
    )


    async with httpx.AsyncClient() as client:

        response = await client.get(
            url,
            headers={
                "Authorization":
                f"Bearer {token}"
            }
        )


        response.raise_for_status()

        return response.json()



async def assign_realm_roles(
    user_id: str,
    role_names: list[str]
):

    token = await get_admin_token()

    roles = []

    for role_name in role_names:

        role = await get_realm_role(role_name)

        roles.append({
            "id": role["id"],
            "name": role["name"]
        })

    url = (
        f"{get_admin_base_url()}"
        f"/users/{user_id}"
        "/role-mappings/realm"
    )

    async with httpx.AsyncClient() as client:

        response = await client.post(
            url,
            json=roles,
            headers={
                "Authorization": f"Bearer {token}"
            }
        )

        response.raise_for_status()


async def delete_user(user_id: str):
    """
    Elimina un usuario de Keycloak.
    
    Args:
        user_id: ID del usuario en Keycloak
    """

    token = await get_admin_token()

    url = (
        f"{get_admin_base_url()}"
        f"/users/{user_id}"
    )

    async with httpx.AsyncClient() as client:

        response = await client.delete(
            url,
            headers={
                "Authorization": f"Bearer {token}"
            }
        )

        response.raise_for_status()


async def create_realm_role(role_name: str, description: str = ""):
    """
    Crea un rol en Keycloak.
    
    Args:
        role_name: Nombre del rol a crear
        description: Descripción del rol (opcional)
    
    Returns:
        dict con datos del rol creado
    
    Raises:
        Exception: Si ocurre un error en la creación
    """

    token = await get_admin_token()

    url = (
        f"{get_admin_base_url()}"
        "/roles"
    )

    body = {
        "name": role_name,
        "description": description
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            url,
            json=body,
            headers={
                "Authorization": f"Bearer {token}"
            }
        )

        response.raise_for_status()

    role = await get_realm_role(role_name)
    
    return role


async def update_realm_role(old_role_name: str, new_role_name: str, description: str = ""):
    """
    Actualiza un rol en Keycloak (principalmente el nombre).
    
    Args:
        old_role_name: Nombre actual del rol en Keycloak
        new_role_name: Nuevo nombre del rol
        description: Nueva descripción del rol (opcional)
    
    Returns:
        dict con datos del rol actualizado
    
    Raises:
        Exception: Si ocurre un error en la actualización
    """
    
    token = await get_admin_token()
    
    url = (
        f"{get_admin_base_url()}"
        f"/roles/{old_role_name}"
    )
    
    body = {
        "name": new_role_name,
        "description": description
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.put(
            url,
            json=body,
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        
        response.raise_for_status()
    
    role = await get_realm_role(new_role_name)
    
    return role


async def create_group(group_name: str):
    """
    Crea un grupo en Keycloak.
    
    Args:
        group_name: Nombre del grupo a crear
    
    Returns:
        dict con datos del grupo creado
    
    Raises:
        Exception: Si ocurre un error en la creación
    """
    
    token = await get_admin_token()
    
    url = (
        f"{get_admin_base_url()}"
        "/groups"
    )
    
    body = {
        "name": group_name
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url,
            json=body,
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        
        response.raise_for_status()
    
    group = await get_group(group_name)
    
    return group


async def get_group(group_name: str):
    """
    Obtiene un grupo de Keycloak por nombre.
    
    Args:
        group_name: Nombre del grupo a obtener
    
    Returns:
        dict con datos del grupo
    
    Raises:
        Exception: Si el grupo no existe
    """
    
    token = await get_admin_token()
    
    url = (
        f"{get_admin_base_url()}"
        "/groups"
    )
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            url,
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        
        response.raise_for_status()
    
    groups = response.json()
    
    for group in groups:
        if group["name"] == group_name:
            return group
    
    raise Exception(f"El grupo '{group_name}' no existe en Keycloak")


async def assign_realm_roles_to_group(
    group_id: str,
    role_names: list[str]
):
    """
    Asigna realm_roles a un grupo.
    
    Args:
        group_id: ID del grupo en Keycloak
        role_names: Lista de nombres de roles a asignar
    
    Raises:
        Exception: Si ocurre un error en la asignación
    """
    
    token = await get_admin_token()
    
    roles = []
    
    for role_name in role_names:
        role = await get_realm_role(role_name)
        
        roles.append({
            "id": role["id"],
            "name": role["name"]
        })
    
    url = (
        f"{get_admin_base_url()}"
        f"/groups/{group_id}/role-mappings/realm"
    )
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url,
            json=roles,
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        
        response.raise_for_status()


async def get_group_roles(group_id: str):
    """
    Obtiene los realm_roles asignados a un grupo.
    
    Args:
        group_id: ID del grupo en Keycloak
    
    Returns:
        Lista de roles asignados al grupo
    
    Raises:
        Exception: Si ocurre un error
    """
    
    token = await get_admin_token()
    
    url = (
        f"{get_admin_base_url()}"
        f"/groups/{group_id}/role-mappings/realm"
    )
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            url,
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        
        response.raise_for_status()
    
    roles = response.json()
    
    return [role["name"] for role in roles]


async def remove_realm_roles_from_group(
    group_id: str,
    role_names: list[str]
):
    """
    Remueve realm_roles de un grupo.
    
    Args:
        group_id: ID del grupo en Keycloak
        role_names: Lista de nombres de roles a remover
    
    Raises:
        Exception: Si ocurre un error
    """
    
    token = await get_admin_token()
    
    roles = []
    
    for role_name in role_names:
        role = await get_realm_role(role_name)
        
        roles.append({
            "id": role["id"],
            "name": role["name"]
        })
    
    url = (
        f"{get_admin_base_url()}"
        f"/groups/{group_id}/role-mappings/realm"
    )
    
    async with httpx.AsyncClient() as client:
        response = await client.request(
            "DELETE",
            url,
            json=roles,
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        
        response.raise_for_status()


async def update_group_name(group_id: str, new_name: str):
    """
    Actualiza el nombre de un grupo.
    
    Args:
        group_id: ID del grupo en Keycloak
        new_name: Nuevo nombre del grupo
    
    Returns:
        dict con datos del grupo actualizado
    
    Raises:
        Exception: Si ocurre un error
    """
    
    token = await get_admin_token()
    
    url = (
        f"{get_admin_base_url()}"
        f"/groups/{group_id}"
    )
    
    body = {
        "name": new_name
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.put(
            url,
            json=body,
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        
        response.raise_for_status()
    
    # Obtener el grupo actualizado
    group_url = (
        f"{get_admin_base_url()}"
        f"/groups/{group_id}"
    )
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            group_url,
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        
        response.raise_for_status()
    
    return response.json()