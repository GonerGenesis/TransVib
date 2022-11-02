from tortoise import Tortoise

from .models import User, Ship, Note, Frame, FramePoint, FrameSegment, FrameCSValues

Tortoise.init_models(["app.db.models"], "models")