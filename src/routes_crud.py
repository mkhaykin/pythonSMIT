from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Body, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

import models
from src.database.async_db import get_async_db
from src.kafka.producer import send_log
from src.service_crud import add_rate, delete_rate, edit_rate, get_rate

router = APIRouter()


@router.get(
    path="/{rate_id}",
    summary="Получить ставку по id.",
    status_code=status.HTTP_200_OK,
    response_model=models.GetRateModel,
    response_description="Тарифная ставка.",
)
async def get(
    rate_id: int,
    session: AsyncSession = Depends(get_async_db),
) -> dict:
    return await get_rate(rate_id, session=session)


@router.post(
    path="",
    summary="Добавить ставку.",
    status_code=status.HTTP_201_CREATED,
    response_model=models.GetRateModel,
    response_description="Добавленное значение.",
)
async def add(
    rate: Annotated[models.CreateRateModel, Body()],
    background_tasks: BackgroundTasks,
    user_id: str | None = None,
    session: AsyncSession = Depends(get_async_db),
) -> models.GetRateModel:
    result = await add_rate(rate, session=session)
    background_tasks.add_task(send_log, user=user_id, action="Add rate.")
    return result


@router.patch(
    path="/{rate_id}",
    summary="Изменение ставки.",
    status_code=status.HTTP_200_OK,
    response_model=models.GetRateModel,
    response_description="Новое значение ставки.",
)
async def edit(
    rate_id: int,
    rate: Annotated[models.UpdateRateModel, Body()],
    background_tasks: BackgroundTasks,
    user_id: str | None = None,
    session: AsyncSession = Depends(get_async_db),
) -> models.GetRateModel:
    result = await edit_rate(rate_id, rate, session=session)
    background_tasks.add_task(send_log, user=user_id, action="Edit rate.")
    return result


@router.delete(
    path="/{rate_id}",
    summary="Удалить ставку.",
    status_code=status.HTTP_200_OK,
    response_model=models.Message,
    response_description="Сообщение с подтверждением.",
)
async def delete(
    rate_id: int,
    background_tasks: BackgroundTasks,
    user_id: str | None = None,
    session: AsyncSession = Depends(get_async_db),
) -> dict:
    result = await delete_rate(rate_id, session=session)
    background_tasks.add_task(send_log, user=user_id, action="Delete rate.")
    return result
