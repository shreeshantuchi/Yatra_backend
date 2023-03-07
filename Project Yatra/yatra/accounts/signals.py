from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver

from .models import Yatri, User,SahayatriExpert,SahayatriGuide,SOSRequest


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

@receiver(post_delete, sender=Yatri)
def delete_user_when_profile_deleted(sender, instance, **kwargs):
    try:
        user = instance.user
        user.delete()
    except User.DoesNotExist:
        pass

@receiver(post_save,sender=SOSRequest)
def check_sos_status(sender, instance, **kwargs):
    if instance.status=='SOL':
        SOSRequest.objects.filter(pk=instance.pk).update(is_active=False)
