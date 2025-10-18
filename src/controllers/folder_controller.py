from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from dominio.db_model import FolderModel
from schemas.folders import Folder, CreateFolder, UpdateFolder

async def get_all(session: AsyncSession, user_id: int):
    try:
        result = await session.execute(select(FolderModel).where(FolderModel.user_id == user_id))
        folder: list[FolderModel] = result.scalars().all()

        if not folder:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='No se encontraron carpetas'
            )
        
        return folder
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Error al obtener las carpetas'
        )
    
async def get_one(session: AsyncSession, folder_id: int, user_id: int):
    try:
        result = await session.execute(
            select(FolderModel).where(FolderModel.id == folder_id, FolderModel.user_id == user_id)
        )
        folder = result.scalars().first()

        if not folder:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Carpeta no encontrada'
            )
        
        return folder
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Error al obtener la carpeta'
        )
    
async def create(session: AsyncSession, data: CreateFolder, user_id: int):
    try:
        folder = FolderModel()
        folder.user_id = user_id
        folder.name = data.name
        folder.description = data.description
        
        session.add(folder)
        await session.commit()
        await session.refresh(folder)

        return {"success": True}

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Error al crear la carpeta'
        )
    
async def update(session: AsyncSession, folder_id: int, data: UpdateFolder, user_id: int):
    try:
        if not data.name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='El nombre de la carpeta es obligatorio'
            )

        result = await session.execute(
            select(FolderModel).where(FolderModel.id == folder_id, FolderModel.user_id == user_id)
        )
        folder_data = result.scalars().first()

        if not folder_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Carpeta no encontrada'
            )
        
        if folder_data.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='No tienes permiso para actualizar esta carpeta'
            )
        
        folder_data.name = data.name if data.name else folder_data.name
        folder_data.description = data.description if data.description else folder_data.description

        await session.commit()
        
        return {"success": True}

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Error al actualizar la carpeta: {str(e)}'
        )
    
async def delete(session: AsyncSession, folder_id: int, user_id: int):
    try:
        result = await session.execute(
            select(FolderModel).where(FolderModel.id == folder_id, FolderModel.user_id == user_id)
        )
        folder_data = result.scalars().first()

        if not folder_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Carpeta no encontrada'
            )
        
        if folder_data.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='No tienes permiso para eliminar esta carpeta'
            )
        
        await session.delete(folder_data)
        await session.commit()

        return {"success": True}
    
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Error al eliminar la carpeta'
        )