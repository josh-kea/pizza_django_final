from django.contrib import admin
from .models import UserProfile, Pizza, Order, Topping

admin.site.register(UserProfile)
admin.site.register(Pizza)
admin.site.register(Order)
admin.site.register(Topping)
