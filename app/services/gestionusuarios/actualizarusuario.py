import httpx

from app.services.keycloak_admin import (
    get_admin_base_url,
    get_admin_token
)


async def update_user_keycloak(
    user_id: str,
    data
):

    token = await get_admin_token()

    url = (
        f"{get_admin_base_url()}"
        f"/users/{user_id}"
    )

    body = {}

    email = getattr(data, "email", None)
    if email is not None:
        body["email"] = email

    nombre = getattr(data, "nombre", None)
    if nombre is not None:
        body["firstName"] = nombre

    apellido = getattr(data, "apellido", None)
    if apellido is not None:
        body["lastName"] = apellido

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