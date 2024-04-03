from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import UserManager
from .manager import UserManager as customManager
from django.contrib.auth.models import PermissionsMixin




class User(AbstractBaseUser, PermissionsMixin):
    REQUIRED_FIELDS = ['password']
    USERNAME_FIELD = ('email')

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=32)
    # remove later
    username = models.CharField(max_length=32, default='d_username')
    email = models.EmailField(unique=True, null=False, blank=False)
    password = models.CharField(max_length=256, null=False, blank=False)
    profile_pic = models.ImageField(upload_to='_user/user_profile_pics', default='_user/defaults/default_profile.png', null=True, blank=True)
    is_superuser = models.BooleanField('superuser', default=False)
    is_staff = models.BooleanField('superuser', default=False)


    objects = customManager()

    def __str__(self) -> str:
        return f"{self.email}"


class Address(models.Model):
    id = models.IntegerField(primary_key=True)
    block = models.IntegerField()
    office = models.IntegerField()
    phone_num = models.CharField(max_length=13)

    def __str__(self) -> str:
        return f"{self.id}"

class Host(models.Model):
    id = models.IntegerField(primary_key=True)
    hostname = models.CharField(max_length=500)
    account_pic = models.ImageField(upload_to='_user/host_profile_pics', default='_user/defaults/default_account.png', null=True, blank=True)
    host_address = models.OneToOneField(Address, related_name='adress_of', blank=True, null=True, on_delete=models.CASCADE) 
    user = models.ForeignKey(User, related_name='hosts_owned', null=False, blank=False, on_delete=models.CASCADE)
    followers = models.ManyToManyField(User, related_name='following', blank=True)
    def __str__(self) -> str:
        return f"{self.hostname}"
