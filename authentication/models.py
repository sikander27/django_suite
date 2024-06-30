from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.utils.translation import gettext as _
from django.db import models
from common.models import BaseModel

from phonenumber_field.modelfields import PhoneNumberField

"""
Usefule Links:
    https://docs.allauth.org/en/latest/
"""

USER_TYPE_OPTION = (
    ("employee", "Employee"),
    ("client", "Client"),
    ("system_admin", "System Admin"),
)


class CustomUser(AbstractUser, BaseModel):
    username = None
    email = models.EmailField(_('email address'), unique=True)
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

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email}"

    class Meta:
        verbose_name_plural = "Users"


def post_user_created_signal(sender, instance, created, **kwargs):
    from subscription.models import Organization, Branch, Profile

    if created and instance.is_organisor:
        org = Organization.objects.create(user=instance)
        if org:
            Branch.objects.create(Organization=org)
    else:
        Profile.objects.get_or_create(user=instance)


post_save.connect(post_user_created_signal, sender=CustomUser)