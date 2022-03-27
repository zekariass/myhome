from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone


class MyHomeUserGroup(models.Model):
    name = models.CharField(verbose_name='user group', max_length=50, blank=False, unique=True)
    description = models.TextField()


"""User manager for the custom user model"""
class MyHomeUserManager(BaseUserManager):
    def create_superuser(self, email, first_name, last_name, password, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_blocked', False)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_admin', True)

        if extra_fields.get('is_admin') is not True:
            raise ValueError('is_admin must be True for superuser')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('is_staff must be True for superuser')

        return self.create_user(email, first_name, last_name, password, **extra_fields)

    def create_user(self, email, first_name, last_name, password, **extra_fields):
        if not email:
            raise ValueError('You must provide email address')

        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save()
        return user
        

"""Custom user model which replaces built is User model"""
class MyHomeUser(AbstractBaseUser):
    first_name = models.CharField(max_length=30, blank=False, null=False)
    last_name = models.CharField(max_length=30, blank=False, null=False)
    email = models.EmailField(verbose_name='email address', unique=True, blank=False, null=False)
    user_group = models.ForeignKey(MyHomeUserGroup, related_name='users', related_query_name='user',
                                     null=True, blank=False, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    is_blocked = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    last_login = models.DateTimeField(editable=False, null=True)
    date_joined = models.DateTimeField(default=timezone.now, editable=False)

    objects = MyHomeUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return '%s %s %s' % (self.first_name, self.last_name, self.email)

    def get_full_name(self):
        return '%s %s' % (self.first_name, self.last_name)

    def get_short_name(self):
        return self.first_name

    def has_perm(self, perm, obj=None):
        '''Check if the user has specific permission'''
        return True
    
    def has_module_perms(self, app_label):
        '''Check if the user has module level permission'''
        return True