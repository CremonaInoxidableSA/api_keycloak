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