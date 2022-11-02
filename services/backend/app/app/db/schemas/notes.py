from typing import Optional

from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from ..models import Note


NoteSchemaCreate = pydantic_model_creator(
    Note, name=f"{Note.__name__}SchemaCreate", exclude_readonly=True)
NoteSchema = pydantic_model_creator(
    Note, name=f"{Note.__name__}Schema", exclude=("author",))


class UpdateNote(BaseModel):
    title: Optional[str]
    content: Optional[str]
