"""
Database models.
"""

from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('Users must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Component(models.Model):
    """Component object."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    name = models.TextField(max_length=63)                          # Component name                        # noqa: E501
    parent = models.IntegerField(blank=True, null=True)             # ID of the Parent                      # noqa: E501
    description = models.TextField(max_length=255, blank=True)      # Description of the component          # noqa: E501
    version = models.TextField(max_length=7)                        # Version of the component              # noqa: E501
    type = models.TextField(max_length=63)                          # Type of the component                 # noqa: E501
    level = models.IntegerField()                                   # Level/Depth of the component          # noqa: E501
    index = models.IntegerField()                                   # Feature No. of the component          # noqa: E501
    skeleton = models.TextField(max_length=25, default=name)        # Name of the main/top skeleton model   # noqa: E501
    mass_properties = models.ManyToManyField(                       # A list of Mass Properties             # noqa: E501
        'MassProperties',
        # related_name='+',
        # blank=True
    )

    def __str__(self):
        return self.name


class MassProperties(models.Model):
    """MassProperties object."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    csys_name = models.TextField(max_length=255)        # Respective csys name local / parent's                   # noqa: E501
    is_csys_local = models.BooleanField(default=True)   # Respective csys is either local or parent's             # noqa: E501
    # component = models.ForeignKey(                      # ID of the relative component                            # noqa: E501
    #     'Component',
    #     on_delete=models.CASCADE
    # )
    xform_matrix = models.TextField(blank=True)         # Formatted String for the Array of [00, 01, 02, 03, 10, 11, 12, 13, 20, 21, 22, 23, 30, 31, 32, 33]     # noqa: E501
    position = models.TextField(blank=True)             # Formatted String for the Array of [x, y, z]             # noqa: E501
    mass = models.TextField(blank=True)                 # Formatted String for the Array of [LSL, LIKELY, USL]    # noqa: E501
    cog_lsl = models.TextField(blank=True)              # Formatted String for the Array of [x, y, z]             # noqa: E501
    cog_usl = models.TextField(blank=True)              # Formatted String for the Array of [x, y, z]             # noqa: E501

    def __str__(self):
        return self.csys_name
