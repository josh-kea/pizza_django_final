from django.contrib.auth.models import Group


def is_pizza_employee(user) -> bool:
    return True if user else False
