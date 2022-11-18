from typing import Tuple, Any, Optional, Union, Type, List

from tortoise import fields, models, Model
from tortoise.exceptions import ValidationError
from tortoise.fields import Field
from tortoise.validators import MaxLengthValidator, Validator
from pydantic import BaseModel


class PointDictValidator(Validator):
    """
    A validator to validate whether the given value is an even number or not.
    """

    # def __init__(self, something: Any):
    #     pass

    def __call__(self, value: dict):
        if "y" not in value:
            raise ValidationError("no y value in dict")
        if "z" not in value:
            raise ValidationError("no z value in dict")


class Point(Field, dict):
    SQL_TYPE = "point"

    # field_type = Tuple[float]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.validators = [PointDictValidator()]

    def to_db_value(self, value: dict, instance: "Union[Type[Model], Model]") -> Optional[tuple]:
        self.validate(value)
        print(value)
        value = tuple((float(value["y"]), float(value["z"])))
        y, z = value
        # return f"({y}, {z})::point"
        return value

    def to_python_value(self, value: Any) -> dict:
        out = {}
        if isinstance(value, str):
            y, z = value.strip('()').split(',')
            return {"y": float(y), "z": float(z)}
        if isinstance(value, tuple):
            y, z = value
            out["y"] = float(y)
            out["z"] = float(z)
            value = out
        self.validate(value)
        return value

    # class _db_postgres:
    #     SQL_TYPE = "point"

    # def describe(self, serializable: bool) -> dict:
    #     desc = super().describe(serializable)
    #     desc["db_filed_types"] = "point"
    #     return desc


class User(models.Model):
    id = fields.IntField(pk=True, unique=True)
    username = fields.CharField(max_length=20, unique=True)
    full_name = fields.CharField(max_length=50, null=True)
    hashed_password = fields.CharField(max_length=128, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)
    is_active = fields.BooleanField(default=True)
    is_superuser = fields.BooleanField(default=True)
    notes: fields.ReverseRelation["Note"]
    ships: fields.ReverseRelation["Ship"]

    def __str__(self):
        return f"{self.username}"

    # class PydanticMeta:
    #     arbitrary_types_allowed = True


class Note(models.Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=225)
    content = fields.TextField()
    author: fields.ForeignKeyRelation[User] = fields.ForeignKeyField("models.User", related_name="notes")
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}, {self.author_id} on {self.created_at}"

    # @staticmethod
    # def parent_id_string():
    #     return "author_id"
    #
    # def owner_id(self):
    #     return self.author_id

    # class PydanticMeta:
    #     exclude = ("author_id",)


class Ship(models.Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=225)
    description = fields.CharField(max_length=225)
    author: fields.ForeignKeyRelation[User] = fields.ForeignKeyField("models.User", related_name="ships")
    frames: fields.ReverseRelation["Frame"]

    def __str__(self):
        return f"{self.title}"


class Frame(models.Model):
    id = fields.IntField(pk=True)
    frame_pos = fields.DecimalField(index=True, max_digits=9, decimal_places=3)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)
    ship: fields.ForeignKeyRelation[Ship] = fields.ForeignKeyField("models.Ship", related_name="frames")
    cs_values: fields.OneToOneNullableRelation["FrameCSValues"]
    frame_segments: fields.ReverseRelation["FrameSegment"]
    frame_points: fields.ReverseRelation["FramePoint"]

    class Meta:
        unique_together = ("frame_pos", "ship")

    # def __str__(self):
    #     return f"{self.frame_pos}"


class FrameSegment(models.Model):
    id = fields.IntField(pk=True)
    frame = fields.ForeignKeyField("models.Frame", related_name="frame_segments")
    start_point = fields.ForeignKeyField('models.FramePoint', related_name="starts_segments")
    end_point = fields.ForeignKeyField('models.FramePoint', related_name="ends_segments")
    thick = fields.DecimalField(max_digits=9, decimal_places=3)


class FramePoint(models.Model):
    id = fields.IntField(pk=True)
    frame: fields.ForeignKeyRelation[Frame] = fields.ForeignKeyField("models.Frame", related_name="frame_points")
    y = fields.DecimalField(max_digits=9, decimal_places=3)
    z = fields.DecimalField(max_digits=9, decimal_places=3)
    starts_segments: fields.ManyToManyRelation["FrameSegment"]
    end_segments: fields.ManyToManyRelation["FrameSegment"]

    def __hash__(self):
        return hash((self.id, self.frame_id))

    def __eq__(self, other):
        return other and self.id == other.id and self.frame_id == other.frame_id

    def __ne__(self, other):
        return not self.__eq__(other)


class FrameCSValues(models.Model):
    # id = fields.IntField(pk=True)
    frame: fields.OneToOneRelation[Frame] = fields.OneToOneField("models.Frame", related_name="cs_values",
                                                                 on_delete=fields.CASCADE, to_field="id", pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)
    # y = fields.DecimalField(max_digits=9, decimal_places=3)
    # z = fields.DecimalField(max_digits=9, decimal_places=3)
    center = Point()
    area = fields.DecimalField(max_digits=40, decimal_places=15)
    aqy = fields.DecimalField(max_digits=40, decimal_places=15)
    aqz = fields.DecimalField(max_digits=40, decimal_places=15)
    ay = fields.DecimalField(max_digits=40, decimal_places=15)
    az = fields.DecimalField(max_digits=40, decimal_places=15)
    ayy = fields.DecimalField(max_digits=40, decimal_places=15)
    azz = fields.DecimalField(max_digits=40, decimal_places=15)
    ayz = fields.DecimalField(max_digits=40, decimal_places=15)
    ayys = fields.DecimalField(max_digits=40, decimal_places=15)
    azzs = fields.DecimalField(max_digits=40, decimal_places=15)
    ayzs = fields.DecimalField(max_digits=40, decimal_places=15)
    phi = fields.DecimalField(max_digits=40, decimal_places=15)
    i1 = fields.DecimalField(max_digits=40, decimal_places=15)
    i2 = fields.DecimalField(max_digits=40, decimal_places=15)
    ir1 = fields.DecimalField(max_digits=40, decimal_places=15)
    ir2 = fields.DecimalField(max_digits=40, decimal_places=15)
    # shear_y = fields.DecimalField(max_digits=9, decimal_places=3)
    # shear_z = fields.DecimalField(max_digits=9, decimal_places=3)
    shear_center = Point()
    it = fields.DecimalField(max_digits=40, decimal_places=15)
    awwm = fields.DecimalField(max_digits=40, decimal_places=15)
