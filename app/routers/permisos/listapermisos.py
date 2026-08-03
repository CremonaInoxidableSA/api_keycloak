from fastapi import APIRouter, HTTPException, Depends, Query

from app.services.gestionpermisos.listapermisos import obtener_permisos_realm
from app.security.permissions import require_role
from app.security.dependencies import get_current_user
from app.schemas.authenticated_user import AuthenticatedUser

router = APIRouter(
    prefix="/permisos",
    tags=["Permisos"]
)

@router.get(
    "/lista",
    dependencies=[Depends(require_role("PERMISO_CONSULTAR_PERMISOS"))]
)
async def listar_permisos(
    numero_pagina: int = Query(1, ge=1, description="Número de página (empezando desde 1)"),
    filtro: str = Query("0", description="Filtro para buscar por nombre de permiso"),
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    """
    Retorna la lista de todos los permisos disponibles en el realm con paginación.
    Solo retorna los permisos que comienzan con "PERMISO_".
    
    Retorna máximo 10 permisos por página.
    
    Query Parameters:
        - numero_pagina: Número de página (default: 1)
        - filtro: String para filtrar permisos por nombre (opcional)
    """
    
    try:
        if filtro == "0" or filtro == None:
            filtro = None
        
        permisos, total = await obtener_permisos_realm(
            numero_pagina=numero_pagina,
            filtro=filtro
        )
        
        permisos_por_pagina = 10
        total_paginas = (total + permisos_por_pagina - 1) // permisos_por_pagina
        
        if total > 0 and numero_pagina > total_paginas:
            raise HTTPException(
                status_code=404,
                detail=f"Página {numero_pagina} no existe."
            )
        
        return {
            "data": permisos,
            "paginacion": {
                "total_paginas": total_paginas,
                "total_permisos": total
            }
        }
    
    except HTTPException:
        raise
    except Exception as e:
        error_str = str(e)
        
        if "Error al conectar con Keycloak" in error_str:
            raise HTTPException(
                status_code=503,
                detail="Error al conectar con el servidor de autenticación"
            )
        else:
            raise HTTPException(
                status_code=400,
                detail=error_str
            )
