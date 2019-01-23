import uuid

from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin
)
from django.db import models
from django.utils import timezone

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    uuid = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        default=uuid.uuid4,
        verbose_name='PK'
    )

    username = models.CharField(
        unique=True,
        verbose_name='Nickname',
        max_length=30
    )

    is_active = models.BooleanField(
        verbose_name='Is active',
        default=True
    )
    date_joined = models.DateTimeField(
        verbose_name='Date joined',
        default=timezone.now
    )

    token = models.TextField(
        default=''
    )

    rate = models.IntegerField(
        verbose_name='rate',
        default=0
    )

    objects = UserManager()

    USERNAME_FIELD = 'username'

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        ordering = ('-date_joined',)

    def __str__(self):
        return self.username

    def get_username(self):
        return self.username

    @property
    def is_staff(self):
        return self.is_superuser


