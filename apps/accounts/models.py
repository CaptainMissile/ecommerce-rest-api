from django.db import models
from django.contrib.auth.models import AbstractUser

from django.db import models

# Create your models here.
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)

class UserManager(BaseUserManager):

    def create_user(self, username, email, role= None, password=None):
        if username is None or username == '':
            raise TypeError('Users should have a username')

        if email is None or email == '' :
            raise TypeError('Users should have a Email')

        user = self.model(username = username, email = self.normalize_email(email), role= role)
        user.set_password(password)
        user.save()

        return user


    def create_superuser(self, username, email, password=None):
        if password is None:
            raise TypeError('Password should not be none')

        user = self.create_user(username, email, password = password)
        user.is_superuser = True
        user.is_staff = True
        user.role = 2
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICES = (
        (1, 'Bank Manager'),
        (2, 'Ecommerce Admin'),
        (3, 'Seller'),
        (4, 'Customer')
    )

    username = models.CharField(max_length=255, unique=True, db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    role = models.PositiveSmallIntegerField(choices = USER_TYPE_CHOICES, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email


class Profile(models.Model):
    GENDER_CHOICES = (
        ('F', 'Female'),
        ('M', 'Male')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    address = models.CharField(max_length=50, null=True, blank =True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=1, null=True, blank=True)
    contact_no = models.CharField(max_length=15, blank=True, null=True)
    bank_account = models.PositiveBigIntegerField(blank=True, null=True)
    profile_pic = models.ImageField(upload_to='profile_pictures/', default = "images/default.png", null=True, blank=True)

    def __str__(self):
        return self.user.username