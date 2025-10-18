from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from fastapi import HTTPException, status
from typing import List
from dominio.db_model import StatusModel
from schemas.statuses import CreateStatus

async def get_all(session: AsyncSession):
    try:
        result = await session.execute(select(StatusModel))
        statuses: List[StatusModel] = result.scalars().all()

        if not statuses:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No se encontraron estados"
            )
        
        return statuses

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener los estados"
        )
    
async def get_one(session: AsyncSession, status_id: int):
    try:
        result_status = await session.execute(select(StatusModel).where(StatusModel.id == status_id))
        status_data: StatusModel = result_status.scalars().first()

        if not status_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Estado no encontrado"
            )
        
        return status_data
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener el estado"
        )

async def create(session: AsyncSession, data: CreateStatus):
    try:
        if not data.name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El nombre del estado es obligatorio"
            )

        status_model = StatusModel()
        status_model.name = data.name

        session.add(status_model)

        await session.commit()
        await session.refresh(status_model)
        return status_model
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al crear el estado"
        )


