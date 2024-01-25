from courses.models import Course, CoursePayment
from core.consts import COURSE_PAYMENT_PAID, AUTHOR_PAYMENT_RATE
from django.contrib.auth import get_user_model
from django.db.models import F
from django.db import DatabaseError, transaction
from mailings.tasks import send_course_buy_letter
from logging import getLogger

logger = getLogger(__name__)

User = get_user_model()

def fullfill_order(product_data, client_id, metadata):
    user = User.objects.get(id=client_id)
    amount = product_data['amount_total'] / 100

    logger.info('Fulfilling order of client id=%s amount=%s upgrade=%s course_id=%s' % 
                (client_id, amount, 'upgrade' in metadata, metadata['course']))
   
    if 'upgrade' in metadata:
        course = Course.objects.get(id=metadata['course'])
        try:
            with transaction.atomic():
                CoursePayment.objects.filter(course=course, student=user).update(option=metadata['option'], amount=F('amount') + amount)
                user.profile.balance += AUTHOR_PAYMENT_RATE * amount
        except DatabaseError as exc:
            logger.error('Exception %s happened when trying to save payment information' % exc)
    else:
        course = Course.objects.get(stripe__product=product_data['price']['product'])
        try:
            with transaction.atomic():
                course.students.add(user)
                CoursePayment.objects.create(course=course, student=user, status=COURSE_PAYMENT_PAID, amount=amount, option=metadata['option'])
                user.profile.balance += AUTHOR_PAYMENT_RATE * amount
        except DatabaseError as exc:
            logger.error('Exception %s happened when trying to save payment information' % exc)
        send_course_buy_letter.delay(user.email, user.username, course.id, course.name, metadata['option'])