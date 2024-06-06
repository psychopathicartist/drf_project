from celery import shared_task
from django.utils import timezone

from users.models import User


@shared_task
def check_users_last_login():
    """
    Проверяет дату последнего логина всех активных пользователей,
    если пользователь не заходил больше месяца, то его профиль деактивируется
    """
    one_month_ago = timezone.now() - timezone.timedelta(days=30)
    users = User.objects.filter(is_active=True)
    for user in users:
        if user.last_login < one_month_ago:
            user.is_active = False
            user.save()
