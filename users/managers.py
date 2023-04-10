from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, username, email_address, password=None, referred_by=None, is_admin=False, is_superuser=False):
        if not username:
            raise ValueError("Users must have a username")
        if not email_address:
            raise ValueError("Users must have an email address")
        user = self.model(
            username=username,
            email_address=self.normalize_email(email_address),
            referred_by=referred_by,
            is_admin=is_admin,
            is_superuser=is_superuser,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email_address, password, referred_by=None):
        user = self.create_user(
            username=username,
            email_address=self.normalize_email(email_address),
            password=password,
            referred_by=referred_by,
            is_admin=True,
            is_superuser=True,
        )
        return user