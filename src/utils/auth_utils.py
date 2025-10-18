from typing_extensions import Annotated
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from dominio.db_model import UserModel
from exceptions.auth_exceptions import CREDENTIALS_EXCEPTION
from schemas.auth import TokenData
from utils.password_utils import verify_password
from utils.tokens_utils import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login", refreshUrl="/refresh-token")

async def get_user(session: AsyncSession, username: str):
    try:
        result = await session.execute(select(UserModel).where(UserModel.username == username))
        user = result.scalars().first()
        if not user:
            return None
        return user
    except SQLAlchemyError:
        return None
    
async def authenticate_user(session: AsyncSession, username: str, password: str):
    try:
        user = await get_user(session, username=username)
        if not user:
            return False
        if not verify_password(password, user.password):
            return False
        return user
    except SQLAlchemyError:
        return False

async def get_current_user(token: Annotated[TokenData, Depends(oauth2_scheme)]):
    try:
        payload = decode_token(token)
        username: str = payload.get("sub")
        id: int = payload.get("id")

        if username is None:
            raise CREDENTIALS_EXCEPTION
        
        token_data = TokenData(username=username, id=id)

        return token_data
    except HTTPException:
        raise CREDENTIALS_EXCEPTION

async def authenticated(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        decode_token(token)
        return True
    except HTTPException:
        raise CREDENTIALS_EXCEPTION
    

CURRENT_USER = Annotated[TokenData, Depends(get_current_user)]