from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_registration_letter(email, username):
    send_mail(
        "Welcome to courses",
        f"Welcome to courses, dear {username}",
        None,
        [email],
        fail_silently=False,
    )


@shared_task
def send_course_buy_letter(email, username, course_id, course_name, option):
    send_mail(
        f"You have bought course {course_name}",
        f"""Congratulations, dear {username}! You have bought course {course_name}.
        Your option is {option}. If you want to upgrade 
        you can do it on a course page http://127.0.0.1:8000/course/{course_id}/
         """,
         None,
         [email],
         fail_silently=False
    )