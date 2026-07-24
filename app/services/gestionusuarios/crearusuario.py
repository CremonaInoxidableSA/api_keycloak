import httpx

from app.services.keycloak_admin import (
    get_admin_base_url,
    get_admin_token,
    assign_realm_roles
)


async def crear_usuario(
    username: str,
    email: str,
    first_name: str,
    last_name: str,
    password: str,
    realm_roles: list[str] | None = None
):

    token = await get_admin_token()

    url = (
        f"{get_admin_base_url()}"
        "/users"
    )

    body = {

        "username": username,

        "email": email,

        "firstName": first_name,

        "lastName": last_name,

        "enabled": True,

        "emailVerified": False,

        "requiredActions": [
            "UPDATE_PASSWORD"
        ],

        "credentials": [
            {
                "type": "password",
                "value": password,
                "temporary": True
            }
        ]
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

        location = response.headers["Location"]

    user_id = location.split("/")[-1]

    if realm_roles:
        await assign_realm_roles(
            user_id=user_id,
            role_names=realm_roles
        )

    return user_id