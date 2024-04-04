# signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import StudentProfile, FacilitatorProfile, SponsorProfile, CustomUser


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Check the user type and create the corresponding profile
        if hasattr(instance, 'studentuser'):
            StudentProfile.objects.create(user=instance)
        elif hasattr(instance, 'facilitatoruser'):
            FacilitatorProfile.objects.create(user=instance)
        elif hasattr(instance, 'sponsoruser'):
           SponsorProfile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    # Save the corresponding profile after the user is saved
    if hasattr(instance, 'studentuser'):
        instance.studentuser.save()
    elif hasattr(instance, 'facilitatoruser'):
        instance.facilitatoruser.save()
    elif hasattr(instance, 'sponsoruser'):
        instance.sponsoruser.save()
