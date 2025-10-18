from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from controllers.task_controller import get_all, get_one, create, change_status, delete, updata
from connection.connection import get_session
from schemas.tasks import Task, TaskCreate, TaskUpdate, TaskStatusUpdate, TasksResponse
from utils.auth_utils import CURRENT_USER
from utils.task_utils import get_all_params

taskRouter = APIRouter()


@taskRouter.get('/{id_folder}/tasks', name='Obtener todas las tareas de la carpeta', response_model=TasksResponse)
async def get_all_tasks(
    id_folder: int, 
    current_user: CURRENT_USER,
    params: get_all_params,
    session: AsyncSession = Depends(get_session),
    ):
    return await get_all(session, id_folder, current_user.id, params)

@taskRouter.post('/{id_folder}/tasks', name='Crear una tarea')
async def create_task(id_folder: int, data: TaskCreate, current_user: CURRENT_USER, session: AsyncSession = Depends(get_session)):
    return await create(session, data, id_folder, current_user.id)

@taskRouter.get('/{id_folder}/tasks/{id_task}', name='Obtener una tarea', response_model=Task)
async def get_one_task(id_folder: int, id_task: int, current_user: CURRENT_USER, session: AsyncSession = Depends(get_session)):
    return await get_one(session, id_task, id_folder, current_user.id)

@taskRouter.patch('/{id_folder}/tasks/{id_task}', name='Actualizar una tarea')
async def change_status_task(id_folder: int, id_task: int, data: TaskStatusUpdate, current_user: CURRENT_USER, session: AsyncSession = Depends(get_session)):
    return await change_status(session, data, id_task, id_folder, current_user.id)

@taskRouter.put('/{id_folder}/tasks/{id_task}', name='Actualizar una tarea')
async def update_task(id_folder: int, id_task: int, data: TaskUpdate, current_user: CURRENT_USER, session: AsyncSession = Depends(get_session)):
    return await updata(session, data, id_task, id_folder, current_user.id)

@taskRouter.delete('/{id_folder}/tasks/{id_task}', name='Eliminar una tarea')
async def delete_task(id_folder: int, id_task: int, current_user: CURRENT_USER, session: AsyncSession = Depends(get_session)):
    return await delete(session, id_task, id_folder, current_user.id)



