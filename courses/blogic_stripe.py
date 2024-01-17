from decouple import config
import stripe
from django.urls import reverse
from core import consts
from courses.models import CoursePrice, CourseUpgradePrice, StripeCourse


stripe.api_key = config('STRIPE_KEY')


class StripeSession:
    def __init__(self, course, option, upgrade_from=False) -> None:
        self.course = course
        self.option = option
        self.upgrade_from = upgrade_from
    
    def buy(self, request):
        price = self.course.stripe.option_prices[self.option]['price']
        line_items = self.get_line_items(price)
        metadata = {'option': self.option} if self.option else {'option': consts.COURSE_OPTION_BASIC}
        return self.create_session(request, line_items, metadata)
    
    def upgrade(self, request):
        price = self.course.stripe.option_prices[self.option]['upgrade'][self.upgrade_from]
        line_items = self.get_line_items(price)
        metadata = {'option': self.option, 'upgrade': True, 'course': self.course.id} 
        return self.create_session(request, line_items, metadata)

    def create_session(self, request, line_items, metadata):
        session = stripe.checkout.Session.create(
            success_url=request.build_absolute_uri(reverse('course-single', kwargs={'id': self.course.id})),
            client_reference_id=request.user.id,
            line_items=[line_items],
            currency=consts.STRIPE_DEFAULT_CURRENCY,
            mode="payment",
            metadata=metadata
        )
        return session

    @staticmethod
    def get_line_items(price):
        return {'price': price, 'quantity': 1}
    

class StripePrice:
    def __init__(self, amount, product) -> None:
        self.amount = amount
        self.product = product

    def create(self):
        return stripe.Price.create(
            unit_amount=int(self.amount * 100),
            currency=consts.STRIPE_DEFAULT_CURRENCY,
            product=self.product['id']
        )
    


# Вызывать этот метод после публикации курса
def create_stripe_upgrade_prices(course, product):
    prices = course.prices.order_by('-amount')
    for idx, price in enumerate(prices):
        stripe_price = StripePrice(price.amount, product).create()['id']
        price.stripe = stripe_price
        if idx > 0:
            upgrade = stripe.Product.create(name=course.name + ' upgrade to option ' + price.option)
            for i in range(idx):
                upgrade_amount = price.amount - prices[i].amount
                upgrade_stripe = StripePrice(upgrade_amount, upgrade).create()['id']
                CourseUpgradePrice.objects.create(
                    course=course,
                    amount=upgrade_amount,
                    stripe=upgrade_stripe,
                    stripe_product=upgrade['id'],
                    from_option=prices[i].option,
                    to_option=price.option
                )
    CoursePrice.objects.bulk_update(prices, ['stripe'])
    # option_prices = {}
    # for idx, option in enumerate(instance.options):
    #     option_dict = {}
    #     option_dict['price'] = StripePrice(option['price'], product).create()['id']
    #     if idx > 0:
    #         upgrade = stripe.Product.create(name=instance.name + ' upgrade to option ' + option['option'])
    #         option_dict['upgrade'] = {}
    #         for upgradable_option in instance.options[:idx]:
    #             upgrade_price = option['price'] - upgradable_option['price']
    #             price = StripePrice(upgrade_price, upgrade).create()
    #             option_dict['upgrade'][upgradable_option['option']] = price['id']
    #     option_prices[option['option']] = option_dict   
    # return option_prices 


def create_stripe_course_item(course):
    product = stripe.Product.create(name=course.name)
    # create_stripe_upgrade_prices(instance, product)
    StripeCourse.objects.create(course=course, product=product['id'])

def delete_stripe_course_item(instance):
    StripeCourse.objects.filter(course=instance).delete()