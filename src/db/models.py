from datetime import datetime
from tortoise.models import Model
from tortoise import fields
from tortoise.validators import RegexValidator

from .utils import uuid



class User(Model):
    id: str = fields.TextField(pk=True, default=uuid)
    username: str = fields.CharField(max_length=12, unique=True)
    #email: str = fields.TextField(validator=[RegexValidator(r'^[a-zA-Z0-9]+(?:\.[a-zA-Z0-9]+)*@[a-zA-Z0-9]+(?:\.[a-zA-Z0-9]+)*$')])
    hashed_password: str = fields.TextField()
    todos: fields.ReverseRelation['Todo']
    
    class Meta:
        table = 'users'


class Todo(Model):
    title: str = fields.CharField(max_length=20)
    content: str | None = fields.TextField(default=None, null=True)
    user: User = fields.ForeignKeyField('models.User', 'todos')
    due: datetime | None = fields.DatetimeField(default=None, null=True)
    created: datetime = fields.DatetimeField(auto_now_add=True)
    done: bool = fields.BooleanField(default=False)
    
    class Meta:
        table = 'todos'