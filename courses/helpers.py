from django.utils.text import slugify

from courses.models import Course
from users.helpers import get_user_full_name


def generate_course_slug(course):
    slug = slugify(course.name)
    if Course.objects.filter(slug=slug).exists():
        slug += slugify('by ' + get_user_full_name(course.author))
    return slug


def make_course_options(prices):
    options = []
    for price in prices:
        option = {
            'id': price.id,
            'option': price.option,
            'amount': price.amount
        }
        options.append(option)
    return options