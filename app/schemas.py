from pydantic import BaseModel, EmailStr

from datetime import datetime


class NoteBase(BaseModel):
    name: str
    location: str
    img_name: str
    description: str


class Note(NoteBase):
    class Config:
        from_attributes = True


class NoteEdit(BaseModel):
    name: str | None = None
    location: str | None = None
    img_name: str | None = None
    description: str | None = None
    updated_at: datetime = datetime.now()

    class Config:
        from_attributes = True


class User(BaseModel):
    name: str
    email: EmailStr
    password: str

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    name: str
    email: EmailStr

    class Config:
        from_attributes = True


class ShowUser(BaseModel):
    name: str
    email: EmailStr
    notes: list[Note] = []

    class Config:
        from_attributes = True


class UserInfo(BaseModel):
    name: str
    email: EmailStr

    class Config:
        from_attributes = True


class ShowNote(BaseModel):
    name: str | None = None
    location: str | None = None
    img_name: str | None = None
    description: str | None = None
    creator: UserInfo

    class Config:
        from_attributes = True


class ShowNoteFilter(BaseModel):
    id_tur: int
    name: str
    img_name: str
    description: str
    creator: UserInfo

    class Config:
        from_attributes = True


class Token(BaseModel):
    # email: str
    # token: str
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None


class TokenDataRole(BaseModel):
    role: str | None = None
