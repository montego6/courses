from django.urls import reverse
from decouple import config
import stripe
from moviepy.editor import VideoFileClip
from courses import consts
from courses.models import CoursePayment, Lesson, SectionItem, StripeCourse, TestCompletion


stripe.api_key = config('STRIPE_KEY')

def get_user_from_context(context):
    user = None
    request = context.get('request')
    if request and hasattr(request, 'user'):
        if request.user.is_authenticated:
            user = request.user
    return user
    

def make_payment_context(course, student):
    context = {}
    try:
        payment = CoursePayment.objects.get(course=course, student=student)
    except CoursePayment.DoesNotExist:
        context['payment'] = consts.COURSE_OPTION_FREE
    else:
        context['payment'] = payment.option
    return context

    

class ExtraContext:
    def __init__(self, context, user, course) -> None:
        self.context = context
        self.user = user
        self.course = course

    def is_author(self):
        return self.user == self.course.author
    
    def update_context(self):
        self.context['is_author'] = self.is_author()
        self.context['user'] = self.user
        return self.context
    

def get_test_completion_result(context, obj):
    user = context.get('user')
    try:
        test_completion = TestCompletion.objects.get(test=obj, student=user)
    except TestCompletion.DoesNotExist:
        return False
    else:
        return test_completion.result
    

def has_user_full_access(context, instance):
    payment_option = context.get('payment')
    is_author = context.get('is_author')
    return is_author or (payment_option and consts.COURSE_OPTIONS.index(payment_option) >= consts.COURSE_OPTIONS.index(instance.option))


# class StripeSession:
#     def __init__(self, course, option, upgrade_from=False) -> None:
#         self.course = course
#         self.option = option
#         self.upgrade_from = upgrade_from
    
#     def buy(self, request):
#         price = self.course.stripe.price if not self.option else self.course.stripe.option_prices[self.option]
#         line_items = self.get_line_items(price)
#         metadata = {'option': self.option} if self.option else {'option': consts.COURSE_OPTION_BASIC}
#         return self.create_session(request, line_items, metadata)
    
#     def upgrade(self, request):
#         price = self.course.stripe.option_prices[self.option]['upgrade'][self.upgrade_from]
#         line_items = self.get_line_items(price)
#         metadata = {'option': self.option, 'upgrade': True, 'course': self.course.id} 
#         return self.create_session(request, line_items, metadata)

#     def create_session(self, request, line_items, metadata):
#         session = stripe.checkout.Session.create(
#             success_url=request.build_absolute_uri(reverse('course-single', kwargs={'id': self.course.id})),
#             client_reference_id=request.user.id,
#             line_items=[line_items],
#             currency='rub',
#             mode="payment",
#             metadata=metadata
#         )
#         return session

#     @staticmethod
#     def get_line_items(price):
#         return {'price': price, 'quantity': 1}
    

# class StripePrice:
#     def __init__(self, amount, product) -> None:
#         self.amount = amount
#         self.product = product

#     def create(self):
#         return stripe.Price.create(
#             unit_amount=int(self.amount * 100),
#             currency=consts.STRIPE_DEFAULT_CURRENCY,
#             product=self.product['id']
#         )
    
# def create_section_item(instance):
#     SectionItem.objects.create(content_object=instance, section=instance.section)


# def create_stripe_upgrade_prices(instance, product):
#     option_prices = {}
#     for idx, option in enumerate(instance.options):
#         option_dict = {}
#         option_dict['price'] = StripePrice(option['price'], product).create()['id']
#         if idx > 0:
#             upgrade = stripe.Product.create(name=instance.name + ' upgrade to option ' + option['option'])
#             option_dict['upgrade'] = {}
#             for upgradable_option in instance.options[:idx]:
#                 upgrade_price = option['price'] - upgradable_option['price']
#                 price = StripePrice(upgrade_price, upgrade).create()
#                 option_dict['upgrade'][upgradable_option['option']] = price['id']
#         option_prices[option['option']] = option_dict   
#     return option_prices 


# def create_stripe_course_item(instance):
#     product = stripe.Product.create(name=instance.name)
#     option_prices = create_stripe_upgrade_prices(instance, product)
#     StripeCourse.objects.create(course=instance, product=product['id'], option_prices=option_prices)

# def delete_stripe_course_item(instance):
#     StripeCourse.objects.filter(course=instance).delete()

def calculate_video_length(instance):
    video = VideoFileClip(instance.file.path)
    Lesson.objects.filter(id=instance.id).update(duration=video.duration)