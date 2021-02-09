from django.apps import AppConfig

class PizzaAppConfig(AppConfig):
    name = 'pizza_app'

    def ready(self):
        from . signals import create_user_profile_signal
