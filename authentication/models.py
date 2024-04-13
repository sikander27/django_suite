from django.db import models

# Create your models here.
from django.utils import timezone

from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.utils.translation import gettext as _

from django.db import models
from common.models import BaseModel

from phonenumber_field.modelfields import PhoneNumberField


USER_TYPE_OPTION = (
    ("employee", "Employee"),
    ("client", "Client"),
    ("system_admin", "System Admin"),
)


class User(AbstractUser, BaseModel):
    phone = PhoneNumberField(
        verbose_name="mobile number",
        null=True,
        blank=True,
        unique=True,
        max_length=25,
    )
    user_type = models.CharField(
        choices=USER_TYPE_OPTION,
        max_length=50,
        default="client",
        null=True,
        blank=True,
    )
    is_organisor = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.username}({self.email})"

    class Meta:
        verbose_name_plural = "Users"