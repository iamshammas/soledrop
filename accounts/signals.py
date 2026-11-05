from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import CustomUser, Wallet


@receiver(post_save, sender=CustomUser)
def create_wallet_for_new_user(sender, instance, created, **kwargs):
    """Create a wallet once, when a new user account is registered."""
    if created:
        Wallet.objects.get_or_create(user=instance)
