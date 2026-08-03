import httpx
from sqlalchemy import text
from app.services.keycloak_admin import (
    get_admin_base_url,
    get_admin_token,
    assign_realm_roles
)
from app.config.db import SessionLocal
from app.models.usuarios import Usuarios
from app.core.config import settings

async def verificar_conexiones():
    # Verificar Keycloak
    try:
        url = (
            f"{settings.KEYCLOAK_URL}"
            f"/realms/{settings.KEYCLOAK_REALM}"
            "/.well-known/openid-configuration"
        )
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=5.0)
            response.raise_for_status()
    except Exception as e:
        raise Exception(f"Error de conexión con Keycloak: {str(e)}")
    
    # Verificar MySQL
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
    except Exception as e:
        raise Exception(f"Error de conexión con Base de Datos: {str(e)}")


async def crear_usuario(
    username: str,
    email: str,
    first_name: str,
    last_name: str,
    password: str,
    habilitado: bool = True,
    dni: int | None = None,
    legajo: int | None = None,
    realm_roles: list[str] | None = None
):
    """
    Crea un usuario en Keycloak y luego en MySQL.
    Verifica conexiones antes de crear.
    """
    
    await verificar_conexiones()
    
    try:
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
            "enabled": habilitado,
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
    
    except Exception as e:
        raise Exception(f"Falla en creación general: {str(e)}")
    
    if dni is not None and legajo is not None:
        db = SessionLocal()
        try:
            nuevo_usuario = Usuarios(
                id=user_id,
                dni=dni,
                legajo=legajo
            )
            
            db.add(nuevo_usuario)
            db.commit()
            db.close()
            
        except Exception as db_error:
            db.close()
            raise Exception(f"Falla en creación en base de datos: {str(db_error)}")
    
    return {
        "detail": "Creación correcta",
        "id": user_id,
        "email": email,
        "dni": dni,
        "legajo": legajo,
        "habilitado": habilitado
    }