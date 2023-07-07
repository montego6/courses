from courses.models import Course
from django.contrib.auth import get_user_model


User = get_user_model()

def fullfill_order(product_data, client_id):
    course = Course.objects.get(stripe__product=product_data['product'], stripe__price=product_data['id'])
    user = User.objects.get(id=client_id)
    course.students.add(user)