from typing import Any

from fastapi import APIRouter, BackgroundTasks, Depends, Response, status

from src.auth import jwt, service, utils
from src.auth import db
from src.auth.dependencies import (
    valid_refresh_token,
    valid_refresh_token_user,
    valid_user_create,
)
from src.auth.jwt import parse_jwt_user_data
from src.foodlist.schemas import Food
from src.foodlist.db import create_food

router = APIRouter()


@router.post("/food", status_code=status.HTTP_201_CREATED, response_model=Food)
async def register_user(
    food:Food,
    # auth_data = Depends(valid_user_create),
):
    create_food(food)
    return food
    # user = await db.create_user(auth_data)
    # return {
    #     "email": user["email"],
    # }
