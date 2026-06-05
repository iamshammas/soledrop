import requests
from django.conf import settings


def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{settings.BOT_TOKEN}/sendMessage"

    requests.post(
        url,
        data={
            "chat_id": settings.CHAT_ID,
            "text": message,
        },
        timeout=10,
    )

def send_order_notification(order):
    message = (
        f"🛒 New Order\n\n"
        f"Order ID: {order.order_number}\n"
        f"Customer: {order.user.email}\n"
        f"Amount: ₹{order.total_amount}\n"
        f"Payment: {order.payment_method}"
    )

    send_telegram_message(message)

    
    