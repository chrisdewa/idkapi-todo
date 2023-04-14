from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from passlib.hash import bcrypt

from src.db.models import User
from src.db.schemas import UserOut

security = HTTPBasic()
router = APIRouter(prefix='/router', tags=['users'])

CredentialDeps = Annotated[HTTPBasicCredentials, Depends(security)]


@Depends
async def get_current_user(credentials: CredentialDeps) -> User:
    """returns the user for the given credentials. 
    Raises 403 (forbidden) if username unexistant or wrong password
    """
    credentials.username, credentials.password
    user = await User.get_or_none(username=credentials.username)
    if not user or not bcrypt.verify(credentials.password, user.password):
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, 'Invalid Username/password combination',
            headers={"WWW-Authenticate": "Basic"},
        )
    
    return user

UserDeps = Annotated[User, get_current_user]
    

@Depends
async def register_new_user(username: str, password: str) -> User:
    """Registers a new user into the database and returns the newly created user
    Raises 409 (conflict)
    """
    try:
        user = await User.create(username=username, password=bcrypt.hash(password))
    except Exception as _: # todo: identify precise exception and use it instead
        raise HTTPException(status.HTTP_409_CONFLICT, 'Username already taken')
    
    return user
    
    


@router.get('/me')
async def read_current_user(user: UserDeps) -> UserOut:
    """Returns the current user"""
    return UserOut.from_orm(user)

@router.post('/register')
async def register_new_user(user: Annotated[User, register_new_user]) -> UserOut:
    """Registers a new user"""
    return UserOut.from_orm(user)


    