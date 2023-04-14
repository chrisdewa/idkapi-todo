from fastapi import APIRouter, Depends

from .users import UserDeps

from src.db.models import Todo
from src.db.schemas import TodoOut

router = APIRouter(prefix='/todos', tags=['todos'])



@router.get('/all')
async def get_user_todos(user: UserDeps) -> list[TodoOut]:
    """Returns the user's todos"""
    todos = await user.todos
    return [TodoOut.from_orm(todo) for todo in todos]
    
