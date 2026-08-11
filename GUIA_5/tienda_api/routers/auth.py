from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

import seguridad
from pydantic import BaseModel

router = APIRouter(
    prefix="/auth",
    tags=["Autenticacion"]
)

class UsuarioRegistro(BaseModel):
    username: str
    password: str
    nombre: str

@router.post("/login")
def login(
    datos: OAuth2PasswordRequestForm = Depends()
):
    usuario = seguridad.buscar_usuario(
        datos.username
    )

    if (
        usuario is None
        or not seguridad.verificar_password(
            datos.password,
            usuario["password"]
        )
    ):
        raise HTTPException(
            status_code=401,
            detail="Usuario o contraseña incorrectos"
        )

    token = seguridad.crear_token(
        usuario["username"]
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@router.get("/yo")
def quien_soy(
    usuario: dict = Depends(
        seguridad.obtener_usuario_actual
    )
):
    return {
        "username": usuario["username"],
        "rol": usuario["rol"]
    }

@router.post("/registro", status_code=201)
def registrar_usuario(datos: UsuarioRegistro):

    if seguridad.buscar_usuario(datos.username):
        raise HTTPException(
            status_code=400,
            detail="El usuario ya existe"
        )

    nuevo_usuario = {
        "username": datos.username,
        "nombre": datos.nombre,
        "password": seguridad.hashear_password(
            datos.password
        ),
        "rol": "cliente"
    }

    seguridad.usuarios.append(nuevo_usuario)

    return {
        "mensaje": "Usuario registrado correctamente",
        "username": datos.username,
        "rol": "cliente"
    }