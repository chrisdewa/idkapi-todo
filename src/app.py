from fastapi import FastAPI

from src.routers.users import router as user_router
from src.routers.todos import router as todo_router

app = FastAPI(docs_url='/')

app.include_router(user_router)
app.include_router(todo_router)

@app.get('/health')
async def health_check() -> str:
    """Ping status check"""
    return "I'm alive"

