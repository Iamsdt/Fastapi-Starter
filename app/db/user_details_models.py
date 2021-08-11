from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator

from app.db.db_constants import DbConstants


# reset password
class ResetPasswordTable(models.Model):
    id = fields.IntField(pk=True)
    otp = fields.CharField(max_length=100, default="")
    user = fields.OneToOneField(DbConstants.USER_TABLE, related_name="reset_user")

    # status
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    status = fields.IntField(default=1)

    def __str__(self):
        return self.otp

    class Meta:
        table = "t_user_reset_password"

    class PydanticMeta:
        exclude = ["user", "created_at", "updated_at", "status"]


ResetPasswordTable_Pydantic = pydantic_model_creator(ResetPasswordTable, name="ResetPassword")


# Device tables
class DeviceTable(models.Model):
    id = fields.IntField(pk=True)
    device_type = fields.CharField(max_length=100, default="")
    device_token = fields.CharField(max_length=100, default="")

    user = fields.ForeignKeyField(DbConstants.USER_TABLE, related_name="device_user")

    # status
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    status = fields.IntField(default=1)

    def __str__(self):
        return self.device_type

    class Meta:
        table = "t_user_devices"

    class PydanticMeta:
        exclude = ["created_at", "updated_at", "status"]


DeviceTable_Pydantic = pydantic_model_creator(DeviceTable, name="DeviceTable")


# Login History
class LoginHistoryTable(models.Model):
    id = fields.IntField(pk=True)

    user = fields.ForeignKeyField(DbConstants.USER_TABLE, related_name="login_user")
    device = fields.ForeignKeyField(DbConstants.DEVICE_TABLE, related_name="login_device")

    # status
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    status = fields.IntField(default=1)

    def __str__(self):
        return str(self.id)

    class Meta:
        table = "t_user_login_history"

    class PydanticMeta:
        exclude = ["created_at", "updated_at", "status"]


LoginHistoryTable_Pydantic = pydantic_model_creator(LoginHistoryTable, name="LoginHistoryTable")
