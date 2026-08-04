from fastapi import APIRouter, Depends, Query

from app.schemas.authenticated_user import AuthenticatedUser
from app.security.dependencies import get_current_user
from app.services.gestionpersonal.submodulospersonales import obtener_submodulos_usuario


router = APIRouter(
    prefix="/submodulos-personales",
    tags=["Permisos"]
)

@router.get("/lista")
async def get_submodulos_personales(
    modulo_padre: str = Query(..., description="Nombre del módulo padre"),
    usuario: AuthenticatedUser = Depends(get_current_user)
):
    """
    Obtiene los submodulos asignados al usuario según sus roles en el JWT
    y el módulo padre especificado.
    """
    submodulos = await obtener_submodulos_usuario(usuario.roles, modulo_padre)
    return submodulos