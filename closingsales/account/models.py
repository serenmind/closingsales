from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.utils.translation import ugettext_lazy as _

class AccountUserManager(BaseUserManager):
    """
    A custom manager to deal with emails as unique identifier for auth
    instead of usernames. The default that's used is "UserManager"
    """

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and save a User with given email and password
        """
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser musht have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser musht have is_superuser=True')
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
    )
    is_active = models.BooleanField(
        _('active'),
        default=False
    )
    USERNAME_FIELD = 'email'
    objects = AccountUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.email

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Send an email to this user
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

