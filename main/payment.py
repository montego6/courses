from courses.models import Course, CoursePayment
from core.consts import COURSE_PAYMENT_PAID
from django.contrib.auth import get_user_model
from django.db.models import F
from mailings.tasks import send_course_buy_letter


User = get_user_model()

def fullfill_order(product_data, client_id, metadata):
    user = User.objects.get(id=client_id)
    amount = product_data['amount_total'] / 100
   
    if 'upgrade' in metadata:
        course = Course.objects.get(id=metadata['course'])
        CoursePayment.objects.filter(course=course, student=user).update(option=metadata['option'], amount=F('amount') + amount)
    else:
        course = Course.objects.get(stripe__product=product_data['price']['product'])
        course.students.add(user)
        CoursePayment.objects.create(course=course, student=user, status=COURSE_PAYMENT_PAID, amount=amount, option=metadata['option'])
        send_course_buy_letter.delay(user.email, user.username, course.id, course.name, metadata['option'])