import hashlib
import hmac
from decimal import Decimal, InvalidOperation

import requests
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from .models import Wallet, WalletTopup, WalletTransaction

DAILY_REWARD_AMOUNT = Decimal('10.00')
MIN_TOPUP_AMOUNT = Decimal('1.00')
MAX_TOPUP_AMOUNT = Decimal('100000.00')
RAZORPAY_ORDER_URL = 'https://api.razorpay.com/v1/orders'


class PaymentGatewayNotConfigured(Exception):
    """Raised when Razorpay keys are missing from the environment."""


def get_wallet(user):
    wallet, _ = Wallet.objects.get_or_create(user=user)
    return wallet


def _normalize_amount(amount):
    try:
        value = Decimal(str(amount))
    except (InvalidOperation, TypeError, ValueError) as exc:
        raise ValidationError('Enter a valid amount.') from exc

    if not value.is_finite():
        raise ValidationError('Enter a valid amount.')

    return value.quantize(Decimal('0.01'))


def _apply_transaction(wallet, amount, transaction_type):
    balance_before = wallet.balance
    balance_after = balance_before + amount

    wallet.balance = balance_after
    wallet.save(update_fields=['balance', 'updated_at'])

    return WalletTransaction.objects.create(
        wallet=wallet,
        transaction_type=transaction_type,
        amount=amount,
        balance_before=balance_before,
        balance_after=balance_after,
    )


def credit_wallet(wallet, amount, transaction_type=WalletTransaction.TransactionType.CREDIT):
    amount = _normalize_amount(amount)

    if amount <= 0:
        raise ValidationError('Amount must be greater than zero.')

    with transaction.atomic():
        wallet = Wallet.objects.select_for_update().get(pk=wallet.pk)
        return _apply_transaction(wallet, amount, transaction_type)


def claim_daily_reward(wallet):
    """Credit the daily reward once per calendar day. Returns None if already claimed."""
    with transaction.atomic():
        wallet = Wallet.objects.select_for_update().get(pk=wallet.pk)
        already_claimed = WalletTransaction.objects.filter(
            wallet=wallet,
            transaction_type=WalletTransaction.TransactionType.REWARD,
            created_at__date=timezone.localdate(),
        ).exists()

        if already_claimed:
            return None

        return _apply_transaction(
            wallet,
            DAILY_REWARD_AMOUNT,
            WalletTransaction.TransactionType.REWARD,
        )


def create_razorpay_topup(wallet, amount):
    amount = _normalize_amount(amount)

    if amount < MIN_TOPUP_AMOUNT or amount > MAX_TOPUP_AMOUNT:
        raise ValidationError(
            f'Top-up amount must be between ₹{MIN_TOPUP_AMOUNT} and ₹{MAX_TOPUP_AMOUNT}.'
        )

    key_id = settings.RAZORPAY_KEY_ID
    key_secret = settings.RAZORPAY_KEY_SECRET

    if not key_id or not key_secret:
        raise PaymentGatewayNotConfigured(
            'Razorpay is not configured. Add RAZORPAY_KEY_ID and '
            'RAZORPAY_KEY_SECRET to .env.'
        )

    topup = WalletTopup.objects.create(wallet=wallet, amount=amount)

    try:
        response = requests.post(
            RAZORPAY_ORDER_URL,
            auth=(key_id, key_secret),
            json={
                'amount': topup.amount_in_paise,
                'currency': 'INR',
                'receipt': f'wallet-topup-{topup.pk}',
                'notes': {
                    'wallet_id': wallet.pk,
                    'user_id': wallet.user_id,
                },
            },
            timeout=15,
        )
        response.raise_for_status()
        order_id = response.json().get('id')
    except requests.RequestException as exc:
        topup.status = WalletTopup.Status.FAILED
        topup.save(update_fields=['status', 'updated_at'])
        raise ValidationError('Could not start the payment. Please try again.') from exc

    if not order_id:
        topup.status = WalletTopup.Status.FAILED
        topup.save(update_fields=['status', 'updated_at'])
        raise ValidationError('The payment gateway returned an invalid response.')

    topup.provider_order_id = order_id
    topup.save(update_fields=['provider_order_id', 'updated_at'])
    return topup


def verify_razorpay_topup(topup, order_id, payment_id, signature):
    key_secret = settings.RAZORPAY_KEY_SECRET

    if not key_secret:
        raise PaymentGatewayNotConfigured(
            'Razorpay is not configured. Add RAZORPAY_KEY_ID and '
            'RAZORPAY_KEY_SECRET to .env.'
        )

    if not all([order_id, payment_id, signature]):
        return False

    if order_id != topup.provider_order_id:
        return False

    expected_signature = hmac.new(
        key_secret.encode(),
        f'{order_id}|{payment_id}'.encode(),
        hashlib.sha256,
    ).hexdigest()

    if not hmac.compare_digest(expected_signature, signature):
        return False

    with transaction.atomic():
        topup = WalletTopup.objects.select_for_update().get(pk=topup.pk)

        if topup.status == WalletTopup.Status.PAID:
            return True

        if topup.status != WalletTopup.Status.PENDING:
            return False

        wallet = Wallet.objects.select_for_update().get(pk=topup.wallet_id)
        _apply_transaction(
            wallet,
            topup.amount,
            WalletTransaction.TransactionType.CREDIT,
        )

        topup.status = WalletTopup.Status.PAID
        topup.provider_payment_id = payment_id
        topup.save(update_fields=['status', 'provider_payment_id', 'updated_at'])

    return True
