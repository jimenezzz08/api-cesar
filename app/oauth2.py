from datetime import datetime, timedelta

from fastapi import HTTPException, status, Depends, Security

from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from . import schemas, models
from .config import settings
from .database import get_db
from .hashing import verify_password

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

oauth2_scheme = HTTPBearer()


def authenticate_user(db: Session, email: str, password: str):
    _user = db.query(models.User).filter(models.User.email == email).first()

    if not _user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials"
        )

    if not verify_password(password, _user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials"
        )
    return _user


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = verify_token(token, credentials_exception)

    _user = db.query(models.User).filter(models.User.email == token.email).first()

    return _user


def get_current_token(
    credentials: HTTPAuthorizationCredentials = Security(oauth2_scheme),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authorization token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    _token = credentials.credentials

    verify_token(_token, credentials_exception)

    # return {"token_type": credentials.scheme, "access_token": credentials.credentials}
    return {"access_token": credentials.credentials, "token_type": credentials.scheme}


def decode_token_email(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authorization token",
    )

    try:
        decode_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = decode_token.get("sub")
        role = decode_token.get("role")
        if email is None:
            raise credentials_exception

        token_email = schemas.TokenData(email=email)
        token_role = schemas.TokenDataRole(role=role)
    except JWTError:
        raise credentials_exception

    return token_email.email, token_role.role
