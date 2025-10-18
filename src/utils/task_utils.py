from pydantic import BaseModel
from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status
from dominio.db_model import FolderModel

class ParamsGetAllTasks(BaseModel):
    q: str | None
    page: int
    limit: int
    status: int

async def get_all_tasks_params(q: str | None = None, page: int = 1, limit: int = 24, status: int = 1):
    return ParamsGetAllTasks(
        q=q, 
        page=page, 
        limit=limit, 
        status=status
    )

get_all_params = Annotated[ParamsGetAllTasks, Depends(get_all_tasks_params)]

async def validate_folder(session: AsyncSession, folder_id: int, user_id: int):
    folder_result = await session.execute(select(FolderModel).where(FolderModel.id == folder_id))
    folder = folder_result.scalars().first()

    if not folder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Carpeta no encontrada.'
        )
    
    if folder.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='No tienes permiso para ver las tareas de esta carpeta.'
        )