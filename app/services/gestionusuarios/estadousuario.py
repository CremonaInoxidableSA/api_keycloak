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


async def estado_user_keycloak(
    user_id: str,
    data
):

    token = await get_admin_token()

    url = (
        f"{get_admin_base_url()}"
        f"/users/{user_id}"
    )

    body = {}

    habilitado = getattr(data, "habilitado", None)
    if habilitado is not None:
        body["enabled"] = habilitado

    async with httpx.AsyncClient() as client:

        response = await client.put(
            url,
            json=body,
            headers={
                "Authorization": f"Bearer {token}"
            }
        )

        response.raise_for_status()