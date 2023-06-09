
from datetime import datetime
from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator

from src.db.models import User, Todo

class UserIn(BaseModel):
    username: str
    password: str

UserOut = pydantic_model_creator(
    User, name='UserOut', exclude=('hashed_password', 'todos')
)

TodoOut = pydantic_model_creator(
    Todo, name='TodoOut'
)

TodoOutSet = pydantic_queryset_creator(
    Todo, name='TodoOutSet'
)

class TodoIn(BaseModel):
    title: str
    content: str | None = None
    due: datetime | None = None
    done: bool | None = False