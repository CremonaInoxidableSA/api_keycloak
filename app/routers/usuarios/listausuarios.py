from fastapi import APIRouter, HTTPException, Depends, Query

from app.services.gestionusuarios.listausuarios import obtener_lista_usuarios
from app.security.permissions import require_role
from app.schemas.authenticated_user import AuthenticatedUser
from app.security.dependencies import get_current_user

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)


@router.get(
    "/lista",
    dependencies=[Depends(require_role("PERMISO_CONSULTAR_USUARIOS"))]
)
async def listar_usuarios(
    numero_pagina: int = Query(1, ge=1, description="Número de página (empezando desde 1)"),
    filtro: str = Query("0", description="Filtro para buscar por email, nombre o apellido"),
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    """
    Obtiene la lista de usuarios del sistema con paginación y filtro.
    """
    
    try:
        if filtro == "0" or filtro == None:
            filtro = None
        
        usuarios, total = await obtener_lista_usuarios(
            numero_pagina=numero_pagina,
            filtro=filtro
        )
        
        usuarios_por_pagina = 10
        total_paginas = (total + usuarios_por_pagina - 1) // usuarios_por_pagina
        
        if total > 0 and numero_pagina > total_paginas:
            raise HTTPException(
                status_code=404,
                detail=f"Página {numero_pagina} no existe."
            )
        
        return {
            "data": usuarios,
            "paginacion": {
                "total_paginas": total_paginas,
                "total_registros": total
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
