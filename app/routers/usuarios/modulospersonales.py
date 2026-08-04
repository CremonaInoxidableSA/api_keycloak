from fastapi import APIRouter, Depends

from app.schemas.authenticated_user import AuthenticatedUser
from app.security.dependencies import get_current_user
from app.services.gestionpersonal.modulospersonales import obtener_modulos_usuario

router = APIRouter(
    prefix="/modulos-personales",
    tags=["Permisos"]
)

@router.get("/lista")
async def get_modulos_personales(
    usuario: AuthenticatedUser = Depends(get_current_user)
):
    """
    Obtiene los módulos asignados al usuario.
    """
    modulos = await obtener_modulos_usuario(usuario.roles)
    return modulos