from fastapi import APIRouter, HTTPException

from app.schemas.user import CreateUserRequest

from app.services.keycloak_admin import create_user


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/crear-usuario")
async def create_new_user(
    data: CreateUserRequest
):

    try:

        user_id = await create_user(
            username=data.email,
            email=data.email,
            first_name=data.nombre,
            last_name=data.apellido,
            password=data.password
        )


        return {

            "message": "Usuario creado correctamente",

            "id": user_id,

            "email": data.email
        }


    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )