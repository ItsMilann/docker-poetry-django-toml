from ast import mod
from django.contrib.auth.models import AbstractUser
from django.db import models
from users.constants import Roles
from users.managers import UserManager
from project.utils import models as base_models


class User(AbstractUser):
    _R = Roles
    username = None
    email = models.EmailField(unique=True)
    active_role = models.CharField(max_length=25, choices=_R.choices, default=_R.RESEARCHER)
    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["role"]

    class Meta:
        ordering = ("-id",)

    def __str__(self):
        return self.email


class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=30, choices=Roles.choices)


class Profile(base_models.SoftDeleteModel):
    _R = Roles
    image = models.ImageField(blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50)
    city = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    streetName = models.CharField(max_length=50, blank=True, null=True)
    zipCode = models.CharField(max_length=50, blank=True, null=True)
    phoneNumber = models.CharField(max_length=25)
    alternatePhoneNumber = models.CharField(max_length=25, blank=True, null=True)

    @property
    def _image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        return ""


class ProfileAddress(base_models.Address):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    class Meta:
        unique_together = (("profile", "address_type"),)


class InstitutionAddress(models.Model):
    country = models.CharField(max_length=55)
    
class InstitutionalAffiliation(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    