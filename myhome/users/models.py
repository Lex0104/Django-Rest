from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='Email')
    phone_number = PhoneNumberField(verbose_name='Номер телефона', blank=True, null=True)
    city = models.CharField(max_length=170, verbose_name='Город', blank=True, null=True)
    avatar = models.ImageField(upload_to="users/images", verbose_name="Аватар", blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return {self.email}

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"