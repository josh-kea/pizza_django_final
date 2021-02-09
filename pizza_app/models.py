from uuid import uuid4
from django.contrib.auth.models import User
from django.db import models
import random, _datetime
import uuid

# CHANNELS FOR NOTIFICATION WHEN ORDER IS PLACED
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# DJANGO RQ FOR EMAIL WHEN ORDER IS PLACED
import django_rq
from . messaging import admin_order_email, user_order_email

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    telephone = models.CharField(max_length=35, default=None, blank=True, null=True)
    isEmployee = models.BooleanField(default=False)

    @classmethod
    def create_userprofile(cls, user): # For signals
        userProfile = cls()
        userProfile.user = user
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

        pizza.save()

        return pizza

    def update_pizza(self, name, text, price):
        self.name = name
        self.text = text
        self.price = price

        self.save()

        return self

    def __str__(self):
        return f"{self.name}"

class Topping(models.Model):
     item = models.CharField(max_length=64, unique=True, blank=False)
     price = models.IntegerField(default=0)

     def __str__(self):
        return f'{self.item}'

class LineItem(models.Model):
    item = models.ForeignKey(Pizza, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=1)
    line_item_order = models.ForeignKey('Order', on_delete=models.CASCADE, null=True, related_name='+')
    
    def __str__(self):
        return f"{self.quantity}x {self.item.name}"

class Order(models.Model):
    status = (
        ('pending', 'pending'),
        ('delivering', 'delivering'),
        ('delivered', 'delivered'),
    )

    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date_time = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(
        choices=status, default='pending', max_length=250)
    final_line_items = models.ManyToManyField(LineItem, blank=True)
    total_price = models.IntegerField(default=0)
    line_items_total_quantity = models.IntegerField(default=0)
    is_placed = models.BooleanField(default=False)

    @classmethod
    def start_new_order(cls, customer):
        order = cls()
        order.customer = customer
        order.is_placed = False
        order.save()

        return order

    def place_order(self):
        self.is_placed = True
        self.save()

        self.create_order_notification()
        self.send_order_confirmation_emails()

        return self

    def create_line_item(self, pizza_id, order):
        pizza = Pizza.objects.get(pk=pizza_id)
        
        line_item, created = LineItem.objects.get_or_create(item=pizza, line_item_order=order)
        
        if created:
            self.final_line_items.add(line_item)
        else:
            line_item.quantity+=1
            line_item.save()
        
        self.line_items_total_quantity = 0
        self.total_price = 0

        for final_line_item in self.final_line_items.all():
            self.total_price+= final_line_item.item.price * final_line_item.quantity
            self.line_items_total_quantity+= final_line_item.quantity
            self.save()

    def clear_line_items(self):
        self.final_line_items.all().delete()
        self.line_items_total_quantity = 0
        self.total_price = 0
        self.save()


    def create_order_notification(self):
        channel_layer = get_channel_layer()
        data = "Order #"+ str(self.pk) + " placed."

        async_to_sync(channel_layer.group_send)(
            str("Notification_Group"),
            {
                "type": "notify",
                "text": data,
            },
        )

    def order_status_change(self):
        channel_layer = get_channel_layer()
        data = self.order_status

        async_to_sync(channel_layer.group_send)(
            str("Order_Status_Group"), 
            {
                "type": "update_status",
                "text": data,
            },
        ) 

    def send_order_confirmation_emails(self):
        django_rq.enqueue(admin_order_email, {
               'order_id' : str(self.pk),
               'email' : 'joshkap2015@gmail.com',
               'order': self
            })
        django_rq.enqueue(user_order_email, {
               'order_id' : str(self.pk),
               'email' : 'joshkap2015@gmail.com',
            })

    def __str__(self):
        return f"Order #{self.pk} {'Placed' if self.is_placed else 'Draft'}"





