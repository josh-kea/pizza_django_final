from django.urls import path

from . import views
from login_app import urls as login_apps

urlpatterns = [
    path('', views.notifications, name='notifications'),
]