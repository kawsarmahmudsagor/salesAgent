# app/auth.py
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from . import models, schemas
from .database import get_db

# ---------------- CONFIG -----------------
SECRET_KEY = "c9d27bcaa6b4902c63f25a39cc21b3610d1736586b1f2a82653b5445c365b74c"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# ---------------- PASSWORD -----------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme_user = OAuth2PasswordBearer(tokenUrl="/auth/user/token")
oauth2_scheme_admin = OAuth2PasswordBearer(tokenUrl="/auth/admin/token")


def get_password_hash(password: str):
    # truncate to 72 characters to avoid bcrypt limitation
    truncated_password = password[:72]
    return pwd_context.hash(truncated_password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password[:72], hashed_password)


# ---------------- USER -----------------
def get_user(db: Session, email: str):
    query = db.query(models.User).filter(models.User.email == email)
    return query.first()

def get_admin(db: Session, email: str):
    query = db.query(models.Admin).filter(models.Admin.email == email)
    return query.first()

def authenticate_user(db: Session, email: str, password: str):
    user = get_user(db, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def authenticate_admin(db: Session, email: str, password: str):
    admin = get_admin(db, email)
    if not admin:
        return False
    if not verify_password(password, admin.hashed_password):
        return False
    return admin

# ---------------- JWT TOKEN -----------------
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme_user), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(db, email=email)
    if user is None:
        raise credentials_exception
    return user


def get_current_admin(token: str = Depends(oauth2_scheme_admin), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    admin = get_admin(db, email=email)
    if admin is None:
        raise credentials_exception
    return admin

