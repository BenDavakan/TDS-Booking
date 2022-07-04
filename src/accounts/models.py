from TdsBooking import settings
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import PermissionsMixin

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
# Create your models here.


class MyUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, tel, password=None,):
        if not email:
            raise ValueError("Vous devez entrer un email.")
        user = self.model(email=self.normalize_email(email),
                          first_name=first_name, last_name=last_name, tel=tel)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email, password=password)
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True

        user.save()
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    tel = models.IntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now=True, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELD = ['first_name', 'last_name']

    objects = MyUserManager()

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


def post_save_receiver(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


post_save.connect(post_save_receiver, sender=settings.AUTH_USER_MODEL)
