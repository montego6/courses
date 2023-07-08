from courses.models import Course, CoursePayment
from courses.consts import COURSE_PAYMENT_PAID
from django.contrib.auth import get_user_model


User = get_user_model()

def fullfill_order(product_data, client_id):
    course = Course.objects.get(stripe__product=product_data['price']['product'], stripe__price=product_data['price']['id'])
    user = User.objects.get(id=client_id)
    course.students.add(user)
    CoursePayment.objects.create(course=course, student=user, status=COURSE_PAYMENT_PAID, amount=product_data['amount_total'])