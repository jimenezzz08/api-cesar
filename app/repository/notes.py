from fastapi import HTTPException, status, Response
from pydantic import EmailStr

from .. import schemas, models
from ..oauth2 import decode_token_email
from sqlalchemy.orm import Session


def store_note(request: schemas.Note, db: Session, current_token: schemas.Token):
    # _email = "test@gmail.com"
    _token_encode = current_token.get("access_token")
    _email, _role = decode_token_email(_token_encode)

    if _role not in [
        "admin",
    ]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"User with email {_email} not authorized",
        )

    _user = db.query(models.User).filter(models.User.email == _email).first()

    if _user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User not found"
        )

    _note = models.Note(
        name=request.name,
        location=request.location,
        img_name=request.img_name,
        description=request.description,
        user_id=_user.id_user,
    )

    # _note = models.Note(**request.dict())

  #  if len(str(_note.title)) < 4 or len(str(_note.title)) > 50:
  #      raise HTTPException(
  #          status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid title"
  #      )
 #
  #  if len(str(_note.description)) < 4 or len(str(_note.description)) > 50:
  #     raise HTTPException(
  #          status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid description"
  #      )

    if not _note:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid data"
        )

    db.add(_note)
    db.commit()
    db.refresh(_note)
    return _note


def show_notes_all(db: Session, current_token: schemas.Token):
    _token_encode = current_token.get("access_token")
    _email, _role = decode_token_email(_token_encode)

    if _role not in ["admin", "client"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"User with email {_email} not authorized",
        )

    _notes = db.query(models.Note).all()

    #    if not _notes:
    #        raise HTTPException(
    #            status_code=status.HTTP_404_NOT_FOUND, detail="Notes not found"
    #        )

    if not _notes:
        _notes = []

    return _notes


def show_note(note_id: int, db: Session, current_token: schemas.Token):
    _token_encode = current_token.get("access_token")
    _email, _role = decode_token_email(_token_encode)

    if _role not in ["admin", "client"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"User with email {_email} not authorized",
        )

    _note = db.query(models.Note).filter(models.Note.id_note == note_id).first()

    if _note == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note with id {note_id} not found",
        )

    return _note


def edit_note_put(
    note_id: int, request: schemas.NoteEdit, db: Session, current_token: schemas.Token
):
    _token_encode = current_token.get("access_token")
    _email, _role = decode_token_email(_token_encode)

    if _role not in [
        "admin",
    ]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"User with email {_email} not authorized",
        )

    _note = db.query(models.Note).filter(models.Note.id_note == note_id)

    valide_note = _note.first()

    if valide_note == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note with id {note_id} not found",
        )

    if len(str(request.title)) < 4 or len(str(request.title)) > 50:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid title"
        )

    if len(str(request.description)) < 4 or len(str(request.description)) > 50:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid description"
        )

    _note.update(request.dict(), synchronize_session=False)
    db.commit()

    return _note.first()


def edit_note_patch(
    note_id: int, request: schemas.NoteEdit, db: Session, current_token: schemas.Token
):
    _token_encode = current_token.get("access_token")
    _email, _role = decode_token_email(_token_encode)

    if _role not in [
        "admin",
    ]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"User with email {_email} not authorized",
        )

    _note = db.query(models.Note).filter(models.Note.id_note == note_id)

    valide_note = _note.first()

    if valide_note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note with id {note_id} not found",
        )

    if len(str(request.title)) < 4 or len(str(request.title)) > 50:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid title"
        )

    if len(str(request.description)) < 4 or len(str(request.description)) > 50:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid description"
        )

    _note.update(request.dict(exclude_unset=True))
    db.commit()

    return _note.first()


def destroy_note(note_id: int, db: Session, current_token: schemas.Token):
    _token_encode = current_token.get("access_token")
    _email, _role = decode_token_email(_token_encode)

    if _role not in [
        "admin",
    ]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"User with email {_email} not authorized",
        )

    _note = db.query(models.Note).filter(models.Note.id_note == note_id)

    valide_note = _note.first()

    if valide_note == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note with id {note_id} not found",
        )

    _note.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
