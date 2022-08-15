from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.bank.models import BankAccount
from .models import Profile, User

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_bank_account(sender, instance, **kwargs):
    instance.profile.save()

@receiver(post_save, sender=User)
def create_bank_account(sender, instance, created, **kwargs):
    if created:
        BankAccount.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_bank_account(sender, instance, **kwargs):
    instance.profile.save()