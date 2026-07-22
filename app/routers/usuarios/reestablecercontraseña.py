from fastapi import APIRouter, HTTPException, Depends

from app.schemas.reset_password import ResetPasswordRequest

from app.services.gestionusuarios.reestablecercontraseña import reset_user_password

from app.security.permissions import require_role
from app.schemas.authenticated_user import AuthenticatedUser
from app.security.dependencies import get_current_user

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)


@router.put(
    "/{user_id}/reset-password",
    dependencies=[Depends(require_role("CONTRASEÑA_USUARIOS"))]
)
async def reset_password(
    user_id: str,
    data: ResetPasswordRequest,
    current_user: AuthenticatedUser = Depends(get_current_user)
):

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

        await reset_user_password(
            user_id=user_id,
            new_password=data.password
        )

        return {
            "message": "Contraseña reestablecida correctamente",
            "user_id": user_id
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
