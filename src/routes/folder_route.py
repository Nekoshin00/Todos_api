from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from controllers.folder_controller import get_all, get_one, create, update, delete
from utils.auth_utils import CURRENT_USER
from connection.connection import get_session
from schemas.folders import Folder, CreateFolder, UpdateFolder

folderRouter = APIRouter()

@folderRouter.get('', name='Obtener todas las carpetas', response_model=List[Folder])
async def get_all_folders(current_user: CURRENT_USER, session: AsyncSession = Depends(get_session)):
    return await get_all(session, current_user.id)

@folderRouter.post('', name='Crear una carpeta')
async def create_folder(data: CreateFolder, current_user: CURRENT_USER, session: AsyncSession = Depends(get_session)):
    return await create(session, data, current_user.id)

@folderRouter.get('/{id_folder}', response_model=Folder, name='Obtener una carpeta por ID')
async def get_one_folder(id_folder: int, current_user: CURRENT_USER, session: AsyncSession = Depends(get_session)):
    return await get_one(session, id_folder, current_user.id)

@folderRouter.put('/{id_folder}', name='Actualizar una carpeta')
async def update_folder(id_folder: int, data: UpdateFolder, current_user: CURRENT_USER, session: AsyncSession = Depends(get_session)):
    return await update(session, id_folder, data, current_user.id)

@folderRouter.delete('/{id_folder}', name='Eliminar una carpeta')
async def delete_folder(id_folder: int, current_user: CURRENT_USER, session: AsyncSession = Depends(get_session)):
    return await delete(session, id_folder, current_user.id)