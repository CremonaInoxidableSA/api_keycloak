from fastapi import APIRouter, Depends

from app.services.gestionpermisos.listagrupos import obtener_grupos_realm
from app.security.dependencies import get_current_user
from app.schemas.authenticated_user import AuthenticatedUser

router = APIRouter(
    prefix="/permisos",
    tags=["Permisos"]
)

@router.get("/grupos")
async def listar_grupos(
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    """
    Retorna la lista de todos los grupos disponibles en el realm.
    Solo retorna los grupos que comienzan con "GRUPO_".
    """
    grupos = await obtener_grupos_realm()
    
    return {
        "grupos": grupos,
        "total": len(grupos)
    }
