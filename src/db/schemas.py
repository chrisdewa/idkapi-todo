from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator

from src.db.models import User, Todo

UserOut = pydantic_model_creator(
    User, name='UserOut', exclude=('password', 'todos')
)

TodoOut = pydantic_model_creator(
    Todo, name='TodoOut'
)

TodoOutSet = pydantic_queryset_creator(
    Todo, name='TodoOutSet'
)

