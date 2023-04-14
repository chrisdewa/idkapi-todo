from fastapi import APIRouter, Depends

from .users import UserDeps

from src.db.models import Todo
from src.db.schemas import TodoOutSet

router = APIRouter(prefix='/todos')



@router.get('/all')
async def get_user_todos(user: UserDeps) -> TodoOutSet:
    """Returns the user's todos"""
    todos = await user.todos
