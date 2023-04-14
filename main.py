import uvicorn

from src.db.config import register_tortoise, TORTOISE_ORM
from src.app import app


register_tortoise(
    app, 
    config=TORTOISE_ORM, 
    generate_schemas=True,
    add_exception_handlers=True,
)

if __name__ == '__main__':
    uvicorn.run('main:app', host='localhost', port=8080, reload=True)
