import hashlib
import hmac
from decimal import Decimal, InvalidOperation

import requests
from django.conf import settings

from accounts.services import PaymentGatewayNotConfigured

RAZORPAY_ORDER_URL = 'https://api.razorpay.com/v1/orders'


def _razorpay_credentials():
    key_id = settings.RAZORPAY_KEY_ID
    key_secret = settings.RAZORPAY_KEY_SECRET

    if not key_id or not key_secret:
        raise PaymentGatewayNotConfigured(
            'Razorpay is not configured. Add RAZORPAY_KEY_ID and '
            'RAZORPAY_KEY_SECRET to .env.'
        )

    return key_id, key_secret


def _amount_in_paise(amount):
    return int((Decimal(str(amount)) * 100).to_integral_value())


def create_razorpay_order(amount, receipt):
    key_id, key_secret = _razorpay_credentials()

    try:
        amount_in_paise = _amount_in_paise(amount)
    except (InvalidOperation, TypeError, ValueError) as exc:
        raise ValueError('Invalid order amount.') from exc

    try:
        response = requests.post(
            RAZORPAY_ORDER_URL,
            auth=(key_id, key_secret),
            json={
                'amount': amount_in_paise,
                'currency': 'INR',
                'receipt': receipt,
                'payment_capture': 1,
            },
            timeout=15,
        )
        response.raise_for_status()
        provider_order_id = response.json().get('id')
    except requests.RequestException as exc:
        raise ValueError(
            'Could not start the payment. Please try again.'
        ) from exc

    if not provider_order_id:
        raise ValueError('The payment gateway returned an invalid response.')

    return provider_order_id


def verify_razorpay_payment(expected_order_id, order_id, payment_id, signature):
    _, key_secret = _razorpay_credentials()

    if not all([expected_order_id, order_id, payment_id, signature]):
        return False

    if order_id != expected_order_id:
        return False

    expected_signature = hmac.new(
        key_secret.encode(),
        f'{order_id}|{payment_id}'.encode(),
        hashlib.sha256,
    ).hexdigest()

    return hmac.compare_digest(expected_signature, signature)
