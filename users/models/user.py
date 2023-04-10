from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from base.models import BaseModel
from users.managers import UserManager




class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True)
    email_address = models.EmailField(max_length=255, unique=True)
    referred_by = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email_address'
    REQUIRED_FIELDS = ['email_address']

    objects = UserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    @property
    def is_staff(self):
        return self.is_admin