from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Activity

@receiver(pre_save, sender=Activity)
def update_activity_location(sender, instance, **kwargs):
    if instance.destination:
        instance.latitude = instance.destination.latitude
        instance.longitude = instance.destination.longitude