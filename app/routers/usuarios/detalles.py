from fastapi import APIRouter, Depends

from app.services.gestionpersonal.detalles import procesar_detalles
from app.schemas.authenticated_user import AuthenticatedUser
from app.security.dependencies import get_current_user

router = APIRouter(
    prefix="/personal",
    tags=["Usuarios gestion personal"]
)

@router.get("/detalles")
async def detalles(
    user: AuthenticatedUser = Depends(get_current_user)
):
    """
    Retorna la información del usuario autenticado con sus 
    módulos, submódulos y permisos clasificados.
    """
    return await procesar_detalles(user)