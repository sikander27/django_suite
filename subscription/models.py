from django.utils import timezone

from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model

from django.db import models
from common.models import BaseModel


from phonenumber_field.modelfields import PhoneNumberField

User = get_user_model()


def trial_period():
    return timezone.now() + timezone.timedelta(days=30)


class Organization(BaseModel):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="organizations"
    )
    name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    expired = models.DateTimeField(default=trial_period)

    def __str__(self):
        return f"{self.name}"


class Branch(BaseModel):
    organization = models.ForeignKey(
        Organization,
        related_name="branches",
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=255, null=True, blank=True)
    phone = PhoneNumberField(
        verbose_name="mobile number", null=True, blank=True, max_length=25
    )
    email = models.EmailField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    # tax_no = models.CharField(max_length=255, blank=True, null=True)
    # bank_ac_no = models.CharField(max_length=255, blank=True, null=True)
    is_headquarter = models.BooleanField(_("Is Headquarter"), default=False)

    def __str__(self):
        return f"{self.name}-{self.organization.name}"

    class Meta:
        verbose_name_plural = "Branches"


class Employee(BaseModel):
    """
    staff
    """

    user = models.ManyToManyField(User, related_name="mandatory_metrics")
    branch = models.ForeignKey(
        Branch,
        related_name="employees",
        on_delete=models.CASCADE,
    )


class Client(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    branch = models.ForeignKey(
        Branch,
        related_name="clients",
        on_delete=models.CASCADE,
    )


class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self) -> str:
        return self.user.get_full_name() if self.user.get_full_name() else self.user.email
