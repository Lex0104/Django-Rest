from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from materials.models import Course, Lesson


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='Email')
    phone_number = PhoneNumberField(verbose_name='Номер телефона', blank=True, null=True)
    city = models.CharField(max_length=170, verbose_name='Город', blank=True, null=True)
    avatar = models.ImageField(upload_to="users/images", verbose_name="Аватар", blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f'{self.email}'


class Payment(models.Model):
    CASH = 'Наличные'
    TRANSFER = 'Перевод'
    method = [
        (CASH, 'Наличные'),
        (TRANSFER, 'Перевод'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='payment')
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата оплаты')
    payment_course = models.ManyToManyField(
        Course, verbose_name='Оплаченный курс', related_name='payment', blank=True, null=True
    )
    payment_lesson = models.ManyToManyField(
        Lesson, verbose_name='Оплаченный урок', related_name='payment', blank=True, null=True
    )
    payment_amount = models.PositiveIntegerField(verbose_name='Сумма оплаты')
    payment_method = models.CharField(max_length=10, choices=method, verbose_name='Способ оплаты')

    class Meta:
        verbose_name = 'Платёж'
        verbose_name_plural = 'Платежи'
        ordering = ['payment_date']

    def __str__(self):
        return f'{self.user} - {self.payment_date}'


class SubscriptionForUpdate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Подписка', related_name='subscription_for_update')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс', related_name='subscription_for_update')