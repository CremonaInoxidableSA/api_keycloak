from fastapi import APIRouter, HTTPException, Depends, Query

from app.services.gestionpermisos.listamodulos import obtener_modulos_realm
from app.security.permissions import require_role
from app.security.dependencies import get_current_user
from app.schemas.authenticated_user import AuthenticatedUser

router = APIRouter(
    prefix="/modulos",
    tags=["Permisos"]
)

@router.get(
    "/lista",
    dependencies=[Depends(require_role("PERMISO_CONSULTAR_MODULOS"))]
)
async def listar_modulos(
    numero_pagina: int = Query(1, ge=1, description="Número de página (empezando desde 1)"),
    filtro: str = Query("0", description="Filtro para buscar por nombre de módulo"),
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    """
    Retorna la lista de todos los módulos disponibles en el realm con paginación.
    Solo retorna los módulos que comienzan con "MODULO_".
    
    Retorna máximo 10 módulos por página.
    
    Query Parameters:
        - numero_pagina: Número de página (default: 1)
        - filtro: String para filtrar módulos por nombre (opcional)
    """
    
    try:
        if filtro == "0" or filtro == None:
            filtro = None
        
        modulos, total = await obtener_modulos_realm(
            numero_pagina=numero_pagina,
            filtro=filtro
        )
        
        modulos_por_pagina = 10
        total_paginas = (total + modulos_por_pagina - 1) // modulos_por_pagina
        
        if total > 0 and numero_pagina > total_paginas:
            raise HTTPException(
                status_code=404,
                detail=f"Página {numero_pagina} no existe."
            )
        
        return {
            "data": modulos,
            "paginacion": {
                "total_paginas": total_paginas,
                "total_modulos": total
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
