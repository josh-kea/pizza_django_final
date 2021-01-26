from django.contrib import admin
from .models import UserProfile, Pizza, Order, Topping  # new

admin.site.register(UserProfile)  # Registers user profile here instead
admin.site.register(Pizza)
admin.site.register(Order)
admin.site.register(Topping)
