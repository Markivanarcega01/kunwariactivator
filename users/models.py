from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
# Create your models here.

class CustomAccountManager(BaseUserManager):

    def create_user(self,username, password, email, **other_fields):
        if not email:
            raise ValueError('Users must have an email')
        other_fields.setdefault('is_active', True)# Make a email verification for this one in the future
        email = self.normalize_email(email)
        user = self.model(
            username = username,
            email = email,
            **other_fields,
        )
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, username, password, email, **other_fields):
        """
        Creates and saves a superuser with the given email,username and password.
        """
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser',True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(username,password, email, **other_fields)

    

class NewUser(AbstractBaseUser, PermissionsMixin):
    SUBSCRIPTION = {
        "1": "Tier 1",
        "2": "Tier 2",
        "3": "Tier 3"
    }
    username = models.CharField(max_length=100, unique=True)
    #password = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(_("email address"),unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    subscription = models.CharField(max_length=100, choices=SUBSCRIPTION, default="1")

    objects = CustomAccountManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username