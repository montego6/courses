from celery import shared_task
from django.core.mail import send_mail
from . import consts


@shared_task
def send_registration_letter(email, username):
    send_mail(
        consts.REGISTRATION_LETTER_HEADER,
        consts.REGISTRATION_LETTER_BODY.format(username),
        None,
        [email],
        fail_silently=False,
    )


@shared_task
def send_course_buy_letter(email, username, course_id, course_name, option):
    send_mail(
        consts.COURSE_BUY_LETTER_HEADER.format(course_name),
        consts.COURSE_BUY_LETTER_BODY.format(username, course_name, option, course_id),
         None,
         [email],
         fail_silently=False
    )