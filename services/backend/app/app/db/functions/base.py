from typing import TypeVar, Generic, Type, Optional, Any

from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException
from tortoise import models

from pydantic import BaseModel
from tortoise.contrib.pydantic import PydanticModel
from tortoise.exceptions import IntegrityError


class Msg(BaseModel):
    msg: str
    id: Optional[int]
    type: Optional[str]


ModelType = TypeVar("ModelType", bound=models.Model)
SchemaType = TypeVar("SchemaType", bound=PydanticModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, SchemaType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType], schema: Type[SchemaType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model
        self.schema = schema

    async def create(self, obj_in: CreateSchemaType):
        obj = await self._create_obj(obj_in)
        return await self.schema.from_tortoise_orm(await obj)

    async def _create_obj(self, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        try:
            obj = await self.model.create(**obj_in_data)
        except IntegrityError:
            raise HTTPException(status_code=401, detail=f"Sorry, that frame exists.")
        return obj

    async def get(self, id: Any) -> Optional[SchemaType]:
        obj = await self.model.get(id=id)
        # print(obj)
        # print(await obj.fetch_related())
        # print(await self.schema.from_tortoise_orm(obj))
        return await self.schema.from_tortoise_orm(obj)

    async def update(self, id: Any, obj_in: UpdateSchemaType) -> Optional[SchemaType]:
        await self.model.filter(id=id).update(**obj_in.dict(exclude_unset=True))
        return await self.schema.from_queryset_single(self.model.get(id=id))

    async def delete(self, id: Any) -> Optional[Msg]:
        deleted_count = await self.model.filter(id=id).delete()
        # print(deleted_count)
        if not deleted_count:
            raise HTTPException(status_code=404, detail=f"{self.model.__name__} {id} not found")
        return Msg(msg=f"Deleted {self.model.__name__} {id}", id=id, type=self.model.__name__)
