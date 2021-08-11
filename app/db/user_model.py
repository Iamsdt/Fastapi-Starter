from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator

from app.db.db_constants import DbConstants


class UserTable(models.Model):
    id = fields.UUIDField(pk=True, generated=False)
    email = fields.CharField(index=True, unique=True, null=False, max_length=255)
    hashed_password = fields.CharField(null=False, max_length=255)
    fullname = fields.CharField(max_length=1000, default="")
    phone = fields.CharField(max_length=100, default="")
    token = fields.CharField(max_length=1000, default="")
    type = fields.IntField(max_length=1000, default=DbConstants.USER_USER)

    image = fields.CharField(max_length=1000, default="")

    is_active = fields.BooleanField(default=True, null=False)
    is_superuser = fields.BooleanField(default=False, null=False)
    is_verified = fields.BooleanField(default=False, null=False)
    is_premium = fields.BooleanField(default=False, null=False)

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    status = fields.IntField(default=1)

    def __str__(self):
        return self.fullname

    class Meta:
        table = "t_user"

    class PydanticMeta:
        exclude = ["hashed_password", "is_active", "is_superuser",
                   "is_verified", "created_at", "updated_at", "status"]


UserTable_Pydantic = pydantic_model_creator(UserTable, name="User")