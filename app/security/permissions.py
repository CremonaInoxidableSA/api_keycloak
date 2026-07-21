from fastapi import Depends, HTTPException, status

from app.schemas.authenticated_user import AuthenticatedUser
from app.security.dependencies import get_current_user


def require_role(role: str):

    def dependency(
        usuario: AuthenticatedUser = Depends(get_current_user)
    ):

        if role not in usuario.roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Se requiere el rol '{role}'."
            )

        return usuario

    return dependency