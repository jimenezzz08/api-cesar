from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from pydantic import EmailStr

from .. import schemas
from ..database import get_db
from ..repository import notes

# from ..oauth2 import get_current_user, get_current_token
from ..oauth2 import get_current_token

router = APIRouter(
    prefix="/turismos",
    tags=["turismos"],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_turismo(
    request: schemas.Note,
    db: Session = Depends(get_db),
    current_token: schemas.Token = Depends(get_current_token),
):
    print(current_token)
    print(type(current_token))
    return notes.store_note(request, db, current_token)


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[schemas.ShowNote])
async def get_turismos_all(
    db: Session = Depends(get_db),
    current_token: schemas.Token = Depends(get_current_token),
):
    return notes.show_notes_all(db, current_token)


@router.get(
    "/{turismo_id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowNote
)
async def get_turismo(
    turismo_id: int,
    db: Session = Depends(get_db),
    current_token: schemas.Token = Depends(get_current_token),
):
    return notes.show_note(turismo_id, db, current_token)


@router.put("/{turismo_id}", status_code=status.HTTP_200_OK)
async def update_turismo_put(
    turismo_id: int,
    request: schemas.NoteEdit,
    db: Session = Depends(get_db),
    current_token: schemas.Token = Depends(get_current_token),
):
    return notes.edit_note_put(turismo_id, request, db, current_token)


@router.patch("/{turismo_id}", status_code=status.HTTP_200_OK)
async def update_turismo_patch(
    turismo_id: int,
    request: schemas.NoteEdit,
    db: Session = Depends(get_db),
    current_token: schemas.Token = Depends(get_current_token),
):
    return notes.edit_note_patch(turismo_id, request, db, current_token)


@router.delete("/{turismo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_turismo(
    turismo_id: int,
    db: Session = Depends(get_db),
    current_token: schemas.Token = Depends(get_current_token),
):
    return notes.destroy_note(turismo_id, db, current_token)
