from fastapi import FastAPI, Depends

from app.schemas.authenticated_user import AuthenticatedUser
from app.security.dependencies import get_current_user

from app.core.config import settings
from app.security.jwks import jwks_client

from app.routers.usuarios import usuarios
from app.routers.usuarios import estadousuarios
from app.routers.usuarios import reestablecercontraseña

#Cosas MYSQL
from sqlalchemy import create_engine, text 
from urllib.parse import quote_plus
from app.config import db
from app.config.sql_loader import cargar_datos_iniciales

import os
from dotenv import load_dotenv

from app.models.usuarios import Usuarios
from app.models.roles import Roles
from app.models.modulos import Modulos
from app.models.submodulos import Submodulos
from app.models.permisos import Permisos
from app.models.usuarios_roles import usuarios_roles
from app.models.rol_modulos import rol_modulos
from app.models.rol_submodulos import rol_submodulos

load_dotenv()

with create_engine(
    f"mysql+pymysql://{os.getenv('DB_USER')}:{quote_plus(os.getenv('DB_PASSWORD', ''))}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}"
).connect() as connection:
    connection.execute(text(f"CREATE DATABASE IF NOT EXISTS {os.getenv('DB_NAME')}"))
    print(f"✓ Base de datos '{os.getenv('DB_NAME')}' verificada o creada exitosamente")

db.Base.metadata.drop_all(bind=db.engine)
db.Base.metadata.create_all(bind=db.engine)
#cargar_datos_iniciales()

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

app.include_router(usuarios.router)
app.include_router(estadousuarios.router)
app.include_router(reestablecercontraseña.router)