from django.utils.text import slugify

from courses.models import Course
from sectionitems.models import SectionItem
from users.helpers import get_user_full_name
from core import consts


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


def get_course_section_items_types(course):
    options_set = set()
    for item in SectionItem.objects.filter(section__course=course):
        if item.lesson:
            options_set.add(consts.SECTION_ITEM_LESSON)
        if item.additional_file:
            options_set.add(consts.SECTION_ITEM_ADDITIONAL_FILE)
        if item.test:
            options_set.add(consts.SECTION_ITEM_TEST)
        if item.homework:
            options_set.add(consts.SECTION_ITEM_HOMEWORK)
    return options_set