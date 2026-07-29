from fastapi import APIRouter, HTTPException, Depends

from app.schemas.change_password import ChangePasswordRequest
from app.schemas.authenticated_user import AuthenticatedUser
from app.security.dependencies import get_current_user

from app.services.gestionpersonal.cambiarcontraseña import cambiar_contraseña_usuario


router = APIRouter(
    prefix="/personal",
    tags=["Usuarios gestion personal"]
)


@router.put(
    "/change-password"
)
async def change_password(
    data: ChangePasswordRequest,
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    """
    Permite al usuario cambiar su propia contraseña.
    """

    try:
        if data.password != data.password_confirmation:
            raise HTTPException(
                status_code=400,
                detail="Las contraseñas no coinciden"
            )

        if not data.password or len(data.password) < 8:
            raise HTTPException(
                status_code=400,
                detail="La contraseña debe tener al menos 8 caracteres"
            )

        resultado = await cambiar_contraseña_usuario(
            user_id=current_user.id,
            new_password=data.password
        )

        return resultado

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
