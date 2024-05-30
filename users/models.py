from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from materials.models import Course, Lesson, NULLABLE


class User(AbstractUser):
    username = None

    email = models.EmailField(verbose_name='почта', unique=True)
    phone = PhoneNumberField(region='RU', verbose_name='номер телефона', **NULLABLE)
    town = models.CharField(max_length=50, verbose_name='город', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'


class Payment(models.Model):

    CASH_METHOD = 'Наличные'
    TRANSLATION_METHOD = 'Перевод на счет'

    PAYMENT_METHODS = [
        (CASH_METHOD, 'Наличные'),
        (TRANSLATION_METHOD, 'Перевод на счет'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name='пользователь')
    payment_date = models.DateField(auto_now=True, verbose_name='дата оплаты')
    payed_course = models.ForeignKey(Course, on_delete=models.SET_NULL, verbose_name='оплаченный курс', **NULLABLE)
    payed_lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, verbose_name='оплаченный урок', **NULLABLE)
    payment_amount = models.PositiveIntegerField(verbose_name='сумма оплаты')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, verbose_name='способ оплаты')
    session_id = models.CharField(max_length=200, **NULLABLE, verbose_name='id платежа')
    link = models.URLField(max_length=400, **NULLABLE, verbose_name='ссылка на оплату')

    def __str__(self):
        return f'{self.payment_amount} / {self.payment_method}'

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'
        ordering = ('payment_date',)
