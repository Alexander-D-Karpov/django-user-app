import secrets
import string

from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .manager import CustomUserManager

# Create your models here.

gender = [("M", "Male"), ("F", "Female"), ("O", "Other")]


class Person(AbstractUser):
    username = models.CharField(unique=True, blank=False, max_length=100)
    email = models.EmailField(_("email address"), unique=True)
    gender = models.CharField(max_length=1, choices=gender, blank=True)
    first_name = models.CharField(blank=True, max_length=100)
    second_name = models.CharField(blank=True, max_length=100)
    about = models.TextField(blank=True)
    image = models.ImageField(blank=True, upload_to="")
    solves = models.IntegerField(default=0)
    coins = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    left_file_upload = models.BigIntegerField(default=0)

    objects = CustomUserManager()

    def get_absolute_url(self):
        return reverse("profile", kwargs={"username": self.username})

    def tg_username(self):
        account = TgAccount.objects.filter(user=self)
        if account:
            return account[0].username
        else:
            return ""

    def __str__(self):
        return self.username


class TgAccount(models.Model):
    user = models.ForeignKey(Person, on_delete=models.CASCADE)
    username = models.CharField(max_length=50, blank=True, null=True)
    secret = models.CharField(max_length=10)
    varified = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.varified:
            alphabet = string.ascii_letters + string.digits
            self.secret = "".join(secrets.choice(alphabet) for _ in range(10))
        super(TgAccount, self).save(*args, **kwargs)
