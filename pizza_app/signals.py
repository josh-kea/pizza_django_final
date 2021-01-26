from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from . models import UserProfile, Order

@receiver(post_save, sender=User, dispatch_uid="create_user_profile")
def create_user_profile(sender, instance, **kwargs):
    print("**** signal received")
    print(sender)
    print(kwargs)
    if UserProfile.objects.filter(user=instance).exists():
        print("User Profile created.")


@receiver(post_save, sender=Order, dispatch_uid="create_order")
def create_order(sender, instance, **kwargs):
    print("**** order created")
    print(sender)
    print(kwargs)
    if Order.objects.exists():
        print(f"Order # {str(instance.pk)} created successfully by customer {str(instance.customer.username)} at {str(instance.order_date_time)}.")
    