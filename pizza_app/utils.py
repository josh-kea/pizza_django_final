from django.contrib.auth.models import Group


def is_pizza_employee(user_profile) -> bool:
    return True if user_profile.isEmployee else False
