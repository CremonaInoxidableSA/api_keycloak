import httpx

from app.services.funcioneskeycloak.get_admin_base_url import get_admin_base_url
from app.services.funcioneskeycloak.get_admin_token import get_admin_token

async def cambiar_password_usuario(
    user_id: str,
    new_password: str
):
    """
    Cambia la contraseña del usuario en Keycloak.
    
    Se utiliza para que el usuario cambie su propia contraseña.
    La contraseña no se marca como temporal.
    """

    try:
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

        return {
            "status": "success",
            "detail": "Contraseña cambiada correctamente"
        }

    except httpx.HTTPStatusError as e:
        error_detail = f"Error al cambiar contraseña: {e.response.status_code}"
        
        if e.response.status_code == 404:
            error_detail = "Usuario no encontrado en Keycloak"
        elif e.response.status_code == 401:
            error_detail = "No autorizado para cambiar contraseña"
        
        raise Exception(error_detail)
    
    except Exception as e:
        raise Exception(f"Falla al cambiar contraseña: {str(e)}")
