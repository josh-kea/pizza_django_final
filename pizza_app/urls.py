from django.contrib import admin
from django.urls import path, include
from . import views
from .api import PizzaList, PizzaDetail
from login_app import urls as login_app

app_name = "pizza_app"

urlpatterns = [
    path('', login_app.views.login, name='login'),
    path('customer_page', views.customer_page, name='customer_page'),
    path('employee_page/', views.employee_page, name='employee_page'),
    path('user_profile/', views.user_profile, name='user_profile'),  # new
    path('base/', views.base, name='base'),
    path('edit_pizza/<int:pk>/', views.edit_pizza, name='edit_pizza'),
    path('delete_pizza/', views.delete_pizza, name='delete_pizza'),
    path('update_pizza/', views.update_pizza, name='update_pizza'),

    path('place_order/', views.place_order, name='place_order'),
    path('clear_order/', views.clear_order, name='clear_order'),
    path('thank_you/<int:pk>/', views.thank_you, name='thank_you'),
    path('api/v1/', PizzaList.as_view()),

    path('api/v1/<int:pk>/', PizzaDetail.as_view()),
    path('edit_customers/', views.edit_customers, name='edit_customers'),

    path('admin/orders', views.orders_page, name='orders_page'),
    path('admin/orders/<int:pk>', views.single_order, name='single_order'),

    path('accept_order', views.accept_order, name='accept_order'),
    path('fulfill_order', views.fulfill_order, name='fulfill_order'),

]
