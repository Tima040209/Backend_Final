
from time import sleep
import stripe
from celery import shared_task
from django.core.mail import send_mail
from .models import Order
@shared_task
def send_email_task(recipient_email):
    sleep(5)
    print(f"Email sent to {recipient_email}")
    return f"Email sent to {recipient_email}"


stripe.api_key = 'your_stripe_secret_key'

@shared_task
def process_payment(order_id, payment_method):
    try:
        order = Order.objects.get(id=order_id)
        # Создание платежа через Stripe
        charge = stripe.Charge.create(
            amount=int(order.total_amount * 100),  # Сумма в центах
            currency="usd",
            source=payment_method,  # Токен карты
            description=f"Payment for Order {order.id}",
        )
        # Обновление статуса заказа
        order.status = Order.PAID
        order.save()

        # Уведомление пользователя
        send_mail(
            'Payment Successful',
            f'Your payment for Order {order.id} was successful!',
            'noreply@yourdomain.com',
            [order.user.email],
        )
        return True
    except Exception as e:
        order = Order.objects.get(id=order_id)
        order.status = Order.FAILED
        order.save()
        return False
