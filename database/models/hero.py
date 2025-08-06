from tortoise import fields

from database.models.base_model import BaseModel


class Hero(BaseModel):
    name = fields.CharField(max_length=150)
    intelligence = fields.IntField(null=True)
    strength = fields.IntField(null=True)
    speed = fields.IntField(null=True)
    power =fields.IntField(null=True)
