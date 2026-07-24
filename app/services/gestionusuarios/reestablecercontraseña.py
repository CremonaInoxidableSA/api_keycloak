import httpx

from app.services.keycloak_admin import (
    get_admin_base_url,
    get_admin_token
)

async def reset_user_password(
    user_id: str,
    new_password: str
):

    token = await get_admin_token()

    url = (
        f"{get_admin_base_url()}"
        f"/users/{user_id}/reset-password"
    )

    body = {
        "type": "password",
        "value": new_password,
        "temporary": False
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

    url_user = (
        f"{get_admin_base_url()}"
        f"/users/{user_id}"
    )

    body_actions = {
        "requiredActions": ["UPDATE_PASSWORD"]
    }

    async with httpx.AsyncClient() as client:

        response = await client.put(
            url_user,
            json=body_actions,
            headers={
                "Authorization": f"Bearer {token}"
            }
        )

        response.raise_for_status()