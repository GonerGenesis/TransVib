from tortoise import Tortoise

from .models import User, Ship
# Frame, FramePoint, FrameSegment, FrameCSValues

Tortoise.init_models(["app.db.models.models"], "models")