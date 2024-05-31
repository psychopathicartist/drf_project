import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_API_KEY


def create_stripe_product(payment):
    if payment.payed_course:
        stripe_product = stripe.Product.create(name=payment.payed_course)
    else:
        stripe_product = stripe.Product.create(name=payment.payed_lesson)
    return stripe_product


def create_stripe_price(payment, product):
    stripe_price = stripe.Price.create(
        currency='rub',
        unit_amount=payment.payment_amount * 100,
        product=product.get('id'),
    )
    return stripe_price


def create_stripe_session(price):
    stripe_session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": price.get('id'), "quantity": 1}],
        mode="payment",
    )
    return stripe_session.get('id'), stripe_session.get('url')
