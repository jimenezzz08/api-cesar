from fastapi import HTTPException, status

from .. import schemas, models
from ..hashing import get_password_hash
from sqlalchemy.orm import Session


def store_user(request: schemas.User, db: Session):
    if len(str(request.password)) < 3 or len(str(request.password)) > 50:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid password"
        )

    request.password = get_password_hash(request.password)

    _user = models.User(**request.dict())

    if len(str(_user.name)) < 3 or len(str(_user.name)) > 50:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid name"
        )

    find_user = db.query(models.User).filter(models.User.email == _user.email).first()

    if find_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email already registered"
        )

    # if len(str(_user.password)) < 8 or len(str(_user.password)) > 61:
    #    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
    #                        detail="Invalid password")

    if not _user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid data"
        )

    db.add(_user)
    db.commit()
    db.refresh(_user)
    return _user


def show_users(db: Session):
    _users = db.query(models.User).all()

    if not _users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Users not found"
        )

    return _users


def show_user(user_id: int, db: Session):
    _user = db.query(models.User).filter(models.User.id_user == user_id).first()

    if _user == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found",
        )
    return _user
