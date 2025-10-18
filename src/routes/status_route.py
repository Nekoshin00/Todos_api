from fastapi import APIRouter
from connection.connection import get_session
from controllers.status_controller import get_all, get_one
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.statuses import Status
from typing import List

statusRouter = APIRouter()

@statusRouter.get('', response_model=List[Status])
async def get_statuses(session: AsyncSession = Depends(get_session)):
    return await get_all(session)

@statusRouter.get('/{id_status}', response_model=Status)
async def get_one_status(id_status: int, session: AsyncSession = Depends(get_session)):
    return await get_one(session, id_status)