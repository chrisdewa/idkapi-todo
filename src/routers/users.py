from datetime import datetime, timedelta
from typing import Annotated, Literal

from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import jwt, JWTError

from src.db.models import User
from src.db.schemas import UserOut, UserIn

SECRET_KEY = '985ab97f4c60fd05c88b0ede23646b05d4474d511903101dd17646c8572def53'
ALGORITHM = 'HS256'
TOKEN_EXP_MIN = 720 # half a day
pwd_ctx = CryptContext(schemes=['bcrypt'], deprecated='auto')
credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'

class TokenData(BaseModel):
    username: str | None = None

router = APIRouter(prefix='/users', tags=['users'])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")

async def authenticate_user(username: str, password: str) -> User | Literal[False]:
    user = await User.get_or_none(username=username)
    if not user or not pwd_ctx.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@Depends	
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    """returns the user for the given credentials. 
    Raises 403 (forbidden) if username unexistant or wrong password
    """    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get('sub')
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = await User.get_or_none(username=username)
    if user is None:
        raise credentials_exception
    
    return user

UserDeps = Annotated[User, get_current_user]

@router.post('/token')
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise credentials_exception
    access_token = create_access_token(
        data={'sub': user.username}, 
        expires_delta=timedelta(minutes=TOKEN_EXP_MIN)
    )
    return Token(access_token=access_token)


@router.get('/me')
async def read_current_user(user: UserDeps) -> UserOut:
    """Returns the current user"""
    return UserOut.from_orm(user)

@router.post('/register')
async def register_new_user(userin: UserIn) -> UserOut:
    """Registers a new user"""
    username = userin.username
    hashed = pwd_ctx.hash(userin.password)
    try:
        user = await User.create(username=username, hashed_password=hashed)
    except Exception as e:
        raise e
    return UserOut.from_orm(user)

    


    