import httpx

from app.services.keycloak_admin import (
    get_admin_base_url,
    get_admin_token
)


async def cambiar_contraseña_usuario(
    user_id: str,
    new_password: str
):
    """
    Cambia la contraseña del usuario en Keycloak.
    
    Se utiliza para que el usuario cambie su propia contraseña.
    La contraseña no se marca como temporal.
    
    Args:
        user_id: ID del usuario en Keycloak (del JWT)
        new_password: Nueva contraseña del usuario
    
    Returns:
        dict con estado del cambio de contraseña
    
    Raises:
        Exception: Con mensaje específico del error
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
            "message": "Contraseña cambiada correctamente"
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
