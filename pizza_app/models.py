from uuid import uuid4
from django.contrib.auth.models import User
from django.db import models
import random, _datetime

# CHANNELS FOR NOTIFICATION WHEN ORDER IS PLACED
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# DJANGO RQ FOR EMAIL WHEN ORDER IS PLACED
import django_rq
from . messaging import email_message, admin_order_email, user_order_email

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    telephone = models.CharField(max_length=35, default=None, blank=True, null=True)
    status = (
        ('employee', 'employee'),
        ('customer', 'customer')
    )
    user_status = models.CharField(
        choices=status, default='customer', max_length=250)

    # @classmethod
    # def create_user(cls, username, password, email, telephone) -> User:
    #     user = None
    #     # Creating a new Django user and also referencing this new user in a variable to be used later down when creating a user profile
    #     user = User.objects.create_user(
    #         username=username, password=password, email=email)

    #     userProfile = cls()
    #     userProfile.user = user
    #     userProfile.telephone = telephone
    #     # Hardcoded testing creating user with customer status so we can test further and improve
    #     userProfile.user_status = "customer"
    #     userProfile.save()

    #     return user

    @classmethod
    def create_userprofile(cls, user):
        # Creating a Django user profile whenever a user is created elsewhere
        userProfile = cls()
        userProfile.user = user
        userProfile.user_status = "customer"
        userProfile.save()

        return userProfile

    def __str__(self):
        return f'{self.user}'

class Pizza(models.Model):
    name = models.CharField(max_length=250)
    text = models.CharField(max_length=250)
    price = models.IntegerField(default=0)
    cover = models.ImageField(upload_to='images', default='default.jpg')


    @classmethod
    def create(cls, name, text, price, cover):
        pizza = cls()
        pizza.name = name
        pizza.text = text
        pizza.price = price
        pizza.cover = cover

        pizza.create_pizza_notification()
        pizza.save()

        return pizza

    def create_pizza_notification(self):
        channel_layer = get_channel_layer()
        data = "Pizza "+ str(self.name) + " is created." # Pass any data based on your requirement
        # Trigger message sent to group
        async_to_sync(channel_layer.group_send)(
            str("Notification_Group"),  # Group Name, Should always be string
            {
                "type": "notify",   # Custom Function written in the consumers.py
                "text": data,
            },
        )

    def __str__(self):
        return f"{self.name}"


class Topping(models.Model):
     item = models.CharField(max_length=64, unique=True, blank=False)
     price = models.IntegerField(default=0)

     def __str__(self):
        return f'{self.item}'

class Order(models.Model):
    status = (
        ('pending', 'pending'),
        ('delivering', 'delivering'),
        ('delivered', 'delivered'),
    )
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date_time = models.DateTimeField(auto_now_add=True)
    delivery_date_time = models.DateTimeField(default='20:00')
    total_price = models.IntegerField(default=0)
    order_status = models.CharField(
        choices=status, default='pending', max_length=250)
    toppings = models.ManyToManyField(Topping, blank=True)
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)

    @classmethod
    def create(cls, delivery_date_time, pizza_id, pizza_name, pizza_price, customer, topping):
        order = cls()
        order.delivery_date_time = delivery_date_time
        order.total_price = pizza_price
        order.customer = customer
        order.pizza = Pizza(pk=pizza_id)
        order.save()
        order.toppings.add(topping)

        # Using non class methods - rather methods on the instance that was created:
        order.create_order_notification()
        order.send_order_confirmation_emails()
        order.test_print()

        return order

    def create_order_notification(self):
        channel_layer = get_channel_layer()
        data = "Order #"+ str(self.pk) + " placed." # Pass any data based on your requirement
        # Trigger message sent to group
        async_to_sync(channel_layer.group_send)(
            str("Notification_Group"),  # Group Name, Should always be string
            {
                "type": "notify",   # Custom Function written in the consumers.py
                "text": data,
            },
        )

        # Tell websocket to update status live 

    def order_status_change(self):
        channel_layer = get_channel_layer()
        data = self.order_status
        # Trigger message sent to group
        async_to_sync(channel_layer.group_send)(
            str("Order_Status_Group"),  # Group Name, Should always be string
            {
                "type": "update_status",   # Custom Function written in the consumers.py
                "text": data,
            },
        )
        

    def send_order_confirmation_emails(self):
        django_rq.enqueue(admin_order_email, {
               'order_id' : str(self.pk),
               'email' : 'joshkap2015@gmail.com',
            })
        django_rq.enqueue(user_order_email, {
               'order_id' : str(self.pk),
               'email' : 'joshkap2015@gmail.com',
            })

    def test_print(self):
        print("Testing the print method. Order id: #" + str(self.pk))

    def __str__(self):
        return f"Order #{self.pk} "





