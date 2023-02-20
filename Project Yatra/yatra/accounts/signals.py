from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Yatri, User


@receiver(post_save, sender=User)
def create_profile_resume(sender, instance, created, **kwargs):
    """
    Signal to create profile when user is created
    """
    if created:
        Yatri.objects.create(user=instance)