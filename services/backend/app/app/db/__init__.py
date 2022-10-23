from sqlmodel import SQLModel

from app.core.config import get_settings

settings = get_settings()

SQLModel.metadata.create_all(settings.database_url)
