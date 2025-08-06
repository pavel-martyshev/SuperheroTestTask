from tortoise import Model, fields


class BaseModel(Model):
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    is_deleted = fields.BooleanField(default=False)

    class Meta:
        abstract = True
