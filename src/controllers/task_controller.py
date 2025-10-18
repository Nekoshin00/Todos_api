from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from typing import List
from dominio.db_model import TaskModel
from schemas.tasks import TaskCreate, TaskUpdate, TaskStatusUpdate
from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError
import math
from utils.task_utils import ParamsGetAllTasks, validate_folder

async def get_all(session: AsyncSession, folder_id: int, user_id: int, params: ParamsGetAllTasks):
    try:
        await validate_folder(session, folder_id, user_id)

        total_count_result = await session.execute(
            select(func.count())
            .select_from(TaskModel)
            .filter(
                TaskModel.status_id == params.status,
                TaskModel.title.ilike(f'%{params.q}%' if params.q else '%%')
            )
            .where(TaskModel.folder_id == folder_id)
            
        )
        total_count = total_count_result.scalar_one()

        if total_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='No se encontraron tareas.'
            )
        
        tasks_result = await session.execute(
            select(TaskModel)
            .filter(
                TaskModel.status_id == params.status,
                TaskModel.title.ilike(f'%{params.q}%' if params.q else '%%')    
            )
            .where(TaskModel.folder_id == folder_id)
            .offset((params.page - 1) * params.limit)
            .limit(params.limit)
        )
        tasks: List[TaskModel] = tasks_result.scalars().all()

        if not tasks:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='No se encontraron tareas.'
            )

        total_pages = math.ceil(total_count / params.limit)
        return {
            "tasks": tasks,
            "total_pages": total_pages,
            "total_count": total_count
        }

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Error al obtener las tareas: {str(e)}'
        )
    
async def get_one(session: AsyncSession, task_id: int, folder_id: int, user_id: int):
    try:
        await validate_folder(session, folder_id, user_id)
        
        task_result = await session.execute(select(TaskModel).where(TaskModel.id == task_id))
        task = task_result.scalars().first()

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Tarea no encontrada.'
            )
        
        return task

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Error al obtener la tarea: {str(e)}'
        )
    
async def create(session: AsyncSession, data: TaskCreate, folder_id: int, user_id):
    try:
        await validate_folder(session, folder_id, user_id)

        task = TaskModel()
        task.folder_id = folder_id
        task.title = data.title
        task.description = data.description

        session.add(task)
        await session.commit()
        await session.refresh(task)

        return {"success": True}

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Error al crear la tarea: {str(e)}'
        )
    
async def updata(session: AsyncSession, data: TaskUpdate, task_id: int, folder_id: int, user_id: int):
    try:
        await validate_folder(session, folder_id, user_id)

        task_result = await session.execute(select(TaskModel).where(TaskModel.id == task_id))
        task = task_result.scalars().first()

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Tarea no encontrada.'
            )
        
        task.title = data.title if data.title else task.title
        task.description = data.description if data.description else task.description

        await session.commit()

        return {"success": True}

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Error al actualizar la tarea: {str(e)}'
        )
        
async def delete(session: AsyncSession, task_id: int, folder_id: int, user_id: int):
    try:
        await validate_folder(session, folder_id, user_id)

        task_result = await session.execute(select(TaskModel).where(TaskModel.id == task_id))
        task = task_result.scalars().first()

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Tarea no encontrada.'
            )
        
        await session.delete(task)
        await session.commit()

        return {"success": True}

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Error al eliminar la tarea: {str(e)}'
        )
    
async def change_status(session: AsyncSession, data: TaskStatusUpdate, task_id: int, folder_id: int, user_id: int):
    try:
        await validate_folder(session, folder_id, user_id)

        task_result = await session.execute(select(TaskModel).where(TaskModel.id == task_id))
        task = task_result.scalars().first()

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Tarea no encontrada.'
            )
        
        task.status_id = data.status_id if data.status_id else task.status_id

        await session.commit()

        return {"success": True}

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Error al cambiar el estado de la tarea: {str(e)}'
        )