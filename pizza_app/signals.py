from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from . models import UserProfile

@receiver(post_save, sender=User, dispatch_uid="create_user_profile")
def create_user_profile_signal(sender, instance, **kwargs):
    user = instance

    if UserProfile.objects.filter(user=user).exists() == False:
        UserProfile.create_userprofile(user)
