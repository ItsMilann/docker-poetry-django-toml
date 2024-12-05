from django.db import models
from django.utils import timezone


class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at=None)


class SoftDeleteModel(models.Model):
    deleted_at = models.DateTimeField(blank=True, null=True)
    objects = SoftDeleteManager()
    manager = models.Manager()

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def undo_delete(self):
        self.deleted_at = None
        self.save()

    class Meta:
        abstract = True


class AddressTypes(models.TextChoices):
    """Choices for Address"""
    PERMANENT = "PERMANENT", "PERMANENT"
    TEMPORARY = "TEMPORARY", "TEMPORARY"


class Address(models.Model):
    """Abstract Model for address"""
    _AT = AddressTypes
    address_type = models.CharField(max_length=10, choices=_AT.choices, default=_AT.PERMANENT)
    country = models.CharField(max_length=55)
    street_address = models.CharField(max_length=155, blank=True, null=True)
    house_number = models.CharField(max_length=155, blank=True, null=True)

    class Meta:
        unique_together = (("profile", "address_type"),)
        abstract = True
