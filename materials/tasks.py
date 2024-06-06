from celery import shared_task
from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER
from materials.models import Subscription, Course


@shared_task
def send_mail_to_user(course_id):
    """
    Рассылает сообщение об обновлении курса на почту пользователей, подписанных на курс
    """
    course = Course.objects.get(pk=course_id)
    subscribers = Subscription.objects.filter(course=course_id)
    email_list = []
    for subscriber in subscribers:
        email_list.append(subscriber.user.email)

    if email_list:
        send_mail(
            'Обновление материалов курса',
            f'Курс "{course}" был обновлен',
            EMAIL_HOST_USER,
            email_list
            )
