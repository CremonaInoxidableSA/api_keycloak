import httpx

from app.services.keycloak_admin import (
    get_admin_base_url,
    get_admin_token
)


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