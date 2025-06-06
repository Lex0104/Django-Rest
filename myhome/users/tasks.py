from datetime import timedelta

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from materials.models import Course
from users.models import User, SubscriptionForUpdate


@shared_task
def send_mail_about_update_course(course_pk):
    course = Course.objects.filter(pk=course_pk).first()
    users = User.objects.all()
    for user in users:
        sub = SubscriptionForUpdate.objects.filter(course=course_pk, user=user.pk).first()
        if sub:
            send_mail(
                subject=f'Курс {course.title_course} был обновлен!',
                message=f'Курс {course.title_course} был обновлен! Скорее посмотрите, какие изменения произошли!',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
            )


@shared_task
def check_last_login():
    today = timezone.now()
    users = User.objects.filter(last_login__isnull=False, is_active=True)
    for user in users:
        if today - user.last_login > timedelta(days=30):
            user.is_active = False
            user.save()