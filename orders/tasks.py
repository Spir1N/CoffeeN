from celery import shared_task
from django.core.mail import send_mail
from shop.models import Order
from django.template.loader import render_to_string
from django.utils.html import strip_tags

@shared_task
def order_created(id):
    """
    Задача для отправки уведомления по электронной почте при успешном создании заказа
    """
    order = Order.objects.get(id=id)
    subject = f'Заказ № 1023{order.id} успешно оформлен'
    
    # Создаем HTML сообщение
    html_message = render_to_string('orders/order_email.html', {
        'order': order,
    })
    plain_message = strip_tags(html_message)
    mail_sent = send_mail(
        subject,
        plain_message,
        'svu6@tpu.ru',  # От кого
        [order.email],  # Кому
        html_message=html_message,  # HTML версия
        fail_silently=False,
    )
    return mail_sent
