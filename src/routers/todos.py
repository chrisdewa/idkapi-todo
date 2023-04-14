from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from .users import UserDeps

from src.db.models import Todo, User
from src.db.schemas import TodoOut, TodoIn

router = APIRouter(prefix='/todos', tags=['todos'])

def get_todo_params(todoin: TodoIn, user: User) -> dict:
    params = dict(title=todoin.title, done=todoin.done, user=user)
    if todoin.content:
        params['content'] = todoin.content
    if todoin.due:
        params['due'] = todoin.due
    
    return params

@Depends
async def get_todo_by_id(todo_id: int, user: UserDeps) -> Todo:
    todo = await Todo.get_or_none(id=todo_id, user=user)
    if not todo:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            'Not such item for the given user'
        )
    return todo


@router.get('/all')
async def get_user_todos(user: UserDeps) -> list[TodoOut]:
    """Returns the user's todos"""
    todos = await user.todos
    return [TodoOut.from_orm(todo) for todo in todos]
    
@router.post('/new')
async def post_new_todo(user: UserDeps, todoin: TodoIn) -> TodoOut:
    params = get_todo_params(todoin, user)
        
    todo = await Todo.create(**params)
    
    return TodoOut.from_orm(todo)

@router.delete('/{todo_id}')
async def delete_todo(todo: Annotated[Todo, get_todo_by_id]) -> int:
    """
    Deletes the given todo by id and user_id taken from credentials
    Raises 404 if not such todo for the auth user
    Returns the id of the deleted todo
    """
    await todo.delete()
    return todo.id

@router.patch('/{todo_id}')
async def patch_todo(user: UserDeps, todoin: TodoIn, todo: Annotated[Todo, get_todo_by_id]) -> TodoOut:
    params = get_todo_params(todoin, user)
    todo.update_from_dict(params)
    await todo.save()
    return TodoOut.from_orm(todo)
    