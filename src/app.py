from fastapi import FastAPI

from src.routes.users import router as user_router

app = FastAPI(docs='/')

app.include_router(user_router)

@app.get('/health')
async def health_check() -> str:
    """Ping status check"""
    return "I'm alive"

