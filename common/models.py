from django.db import models

from django.utils import timezone

from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE_CASCADE


"""
    Useful links:
        - https://dev.to/bikramjeetsingh/soft-deletes-in-django-a9j
        -https://django-safedelete.readthedocs.io/en/latest/index.html
"""


class SoftDeletionQuerySet(models.QuerySet):
    def delete(self):
        return super(SoftDeletionQuerySet, self).update(
            deleted_at=timezone.now()
        )

    def hard_delete(self):
        return super(SoftDeletionQuerySet, self).delete()

    def alive(self):
        return self.filter(deleted_at__isnull=True)

    def dead(self):
        return self.exclude(deleted_at__isnull=True)


class SoftDeletionManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop("alive_only", True)
        super(SoftDeletionManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        if self.alive_only:
            return SoftDeletionQuerySet(self.model).filter(
                deleted_at__isnull=True
            )
        return SoftDeletionQuerySet(self.model)

    def hard_delete(self):
        return self.get_queryset().hard_delete()


class SoftDeletionModel(models.Model):
    """
    Model supporting soft deletion,
    used as parent class for further base models
    """

    deleted_at = models.DateTimeField(blank=True, null=True, editable=False)

    objects = SoftDeletionManager()
    all_objects = SoftDeletionManager(alive_only=False)

    class Meta:
        abstract = True
        # indexes = [
        #     models.Index(fields=["-is_deleted"], name="is_deleted_id"),
        # ]

    def delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        self.deleted_at = None
        self.save()

    def hard_delete(self):
        super(SoftDeletionModel, self).delete()


# with Cascading
# class BaseModel(SafeDeleteModel):
class BaseModel(SoftDeletionModel):
    """
    Base model with common fields
    """

    # _safedelete_policy = SOFT_DELETE_CASCADE

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        "authentication.CustomUser",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="%(class)s_created",
        editable=False,
    )
    last_modified_by = models.ForeignKey(
        "authentication.CustomUser",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="%(class)s_modifications",
        editable=False,
    )

    class Meta:
        abstract = True
