from jwt import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from schemas.auth import Register
from fastapi import HTTPException, status, Depends
from dominio.db_model import UserModel
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from schemas.auth import Token
from datetime import timedelta
from utils.password_utils import get_password_hash
from utils.auth_utils import authenticate_user, decode_token
from utils.tokens_utils import create_access_token, create_refresh_token
from exceptions.auth_exceptions import CREDENTIALS_INCORRECT
from config import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS

async def refresh_token_access(refresh_token: str) -> Token:
    try:
        payload = decode_token(refresh_token)
        username: str = payload.get("sub")
        id: int = payload.get("id")
        token_type: str = payload.get("type")

        if username is None or token_type != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Token inválido"
            )
        
        new_access_token = create_access_token(
            data={"sub": username, "id": id},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )

        return Token(
            access_token=new_access_token,
            token_type="bearer",
            refresh_token=refresh_token
        )
    
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de refresco inválido"
        )
    
async def login(session: AsyncSession, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    try:
        user = await authenticate_user(session, form_data.username, form_data.password)
        if not user:
            raise CREDENTIALS_INCORRECT
        
        access_token = create_access_token(
            data={"sub": user.username, "id": user.id},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )

        refresh_token = create_refresh_token(
            data={"sub": user.username, "id": user.id},
            expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        )

        return Token(
            access_token=access_token,
            token_type="bearer",
            refresh_token=refresh_token
        )

    except SQLAlchemyError:
        raise HTTPException (
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al autenticar el usuario"
        )

async def register(session: AsyncSession, data: Register):
    try:
        if not data.username or not data.email or not data.password or not data.full_name:
            raise HTTPException(status_code=400, detail="Todos los campos son obligatorios")
        
        user = UserModel()

        user.username = data.username
        user.email = data.email
        user.full_name = data.full_name
        user.password = get_password_hash(data.password)
        session.add(user)

        await session.commit()
        await session.refresh(user)

        return { "message": "Usuario creado correctamente" }
    except SQLAlchemyError:
        raise HTTPException (
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al crear el usuario"
        )