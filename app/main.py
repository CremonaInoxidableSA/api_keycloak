from fastapi import FastAPI

from fastapi import Depends
from app.schemas.authenticated_user import AuthenticatedUser
from app.security.dependencies import get_current_user

from app.core.config import settings
from app.security.jwks import jwks_client

from app.routers import users

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0"
)


@app.get("/")
async def root():
    return {
        "message": "API funcionando correctamente",
        "realm": settings.KEYCLOAK_REALM,
        "client": settings.KEYCLOAK_LOGIN_CLIENT_ID
    }

@app.get("/private")
async def private(
    user: AuthenticatedUser = Depends(get_current_user)
):

    return user

@app.get("/health")
async def health():
    return {
        "status": "ok"
    }

app.include_router(
    users.router
    
)