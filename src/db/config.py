from tortoise.contrib.fastapi import register_tortoise
from src.constants import DATABASE_URL

TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        "models": {
            "models": ["src.db.models"],
            "default_connection": "default"
        }
    }
}
