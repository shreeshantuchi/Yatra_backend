from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Yatri, User,SahayatriExpert,SahayatriGuide


@receiver(post_save, sender=User)
def create_profile_resume(sender, instance, created, **kwargs):
    """
    Signal to create profile when user is created
    """
    if created:
        if instance.type =='Y':
            Yatri.objects.create(user=instance)
        elif instance.type == 'G':
            SahayatriGuide.objects.create(user=instance)
        elif instance.type == 'E':
            SahayatriExpert.objects.create(user=instance)