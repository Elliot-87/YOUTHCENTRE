from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import EmployerProfile, JobseekerProfile

@receiver(post_save, sender=User)
def create_profiles(sender, instance, created, **kwargs):
    if created:
        # create both types if you want; or only create one when user selects role in registration
        EmployerProfile.objects.create(user=instance)
        JobseekerProfile.objects.create(user=instance)
