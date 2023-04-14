from datetime import datetime
from tortoise.models import Model
from tortoise import fields
from tortoise.validators import RegexValidator

from .utils import uuid



class User(Model):
    id: str = fields.TextField(pk=True, default=uuid)
    username: str = fields.CharField(max_length=12, unique=True)
    #email: str = fields.TextField(validator=[RegexValidator(r'^[a-zA-Z0-9]+(?:\.[a-zA-Z0-9]+)*@[a-zA-Z0-9]+(?:\.[a-zA-Z0-9]+)*$')])
    password: str = fields.TextField()
    todos: fields.ReverseRelation['Todo']
    
    class Meta:
        table = 'users'


class Todo(Model):
    title: str = fields.CharField(max_length=20)
    content: str = fields.TextField()
    user = fields.ForeignKeyField('models.User', 'todos')
    created: datetime = fields.DatetimeField(auto_now_add=True)
    due: datetime = fields.DatetimeField(default=None, null=True)
    done: bool = fields.BooleanField(default=False)
    
    class Meta:
        table = 'todos'