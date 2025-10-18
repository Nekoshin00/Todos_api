from fastapi import APIRouter, Depends, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from controllers.auth_controller import register, login, refresh_token_access
from connection.connection import get_session
from schemas.auth import Register,RefreshTokenRequest
from typing import Annotated
from utils.auth_utils import authenticated, CURRENT_USER

authRouter = APIRouter()

@authRouter.post("/refresh-token", name="Refrescar token de acceso")
async def refresh_token_route(refresh_token: RefreshTokenRequest):
    return await refresh_token_access(refresh_token.refresh_token)

@authRouter.post("/register", name="Registrar usuario")
async def register_route(user: Register, session: AsyncSession = Depends(get_session)):
    return await register(session, user)

@authRouter.post("/login", name="Iniciar sesión")
async def login_route(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: AsyncSession = Depends(get_session)):
    return await login(session, form_data)

@authRouter.get("/auth", name="Verificar token")
async def auth_route(current_user: CURRENT_USER):
    return {
        "message": "Token válido", 
        "user": current_user
    }