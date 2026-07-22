import httpx

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