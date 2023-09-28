from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from .. import schemas
from ..database import get_db
from ..repository import users
from ..oauth2 import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse
)
async def create_user(request: schemas.User, db: Session = Depends(get_db)):
    return users.store_user(request, db)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[schemas.ShowUser],
    include_in_schema=False,
)
async def get_users(db: Session = Depends(get_db)):
    return users.show_users(db)


@router.get(
    "/{user_id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowUser
)
async def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    return users.show_user(user_id, db)
