from fastapi import Depends

from app.core.config import get_settings


async def get_context(
    settings=Depends(get_settings),
):
    return {
        "settings": settings,
    }

