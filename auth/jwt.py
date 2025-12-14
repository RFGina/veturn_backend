from datetime import datetime, timedelta
from typing import Optional, Annotated
from jwt import PyJWTError
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from database.db import get_db
from models.models import Veterinarias
from helpers.constance import SECRET_KEY, ALGORITHM, TIMEZONE_LOCAL
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def authenticate_veterinaria(
    db: Session,
    email: str,
    password: str
) -> Optional[Veterinarias]:

    veterinaria = db.query(Veterinarias).filter(
        Veterinarias.email == email
    ).first()

    if not veterinaria:
        return None

    if not verify_password(password, veterinaria.hashed_password):
        return None

    if not veterinaria.is_active:
        return None

    return veterinaria


def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None
) -> str:

    to_encode = data.copy()

    expire = datetime.now(TIMEZONE_LOCAL) + (
        expires_delta or timedelta(hours=8)
    )

    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_veterinaria(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Session = Depends(get_db),
) -> Veterinarias:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        veterinaria_id: str | None = payload.get("sub")
        if veterinaria_id is None:
            raise credentials_exception
    except PyJWTError:
        raise credentials_exception

    veterinaria = db.query(Veterinarias).get(int(veterinaria_id))

    if not veterinaria or not veterinaria.is_active:
        raise credentials_exception

    return veterinaria
