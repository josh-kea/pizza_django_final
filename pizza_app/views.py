from django.shortcuts import render, get_object_or_404, reverse
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model
from .models import UserProfile, Pizza, Order, Topping
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
import random
from .utils import is_pizza_employee
from django.urls import reverse
from django.shortcuts import redirect
from .forms import PizzaForm
from django.views.generic import CreateView

# EMAILS
import django_rq
from . messaging import email_message


def index(request):
    if is_pizza_employee(request.user):
        return HttpResponseRedirect(reverse('pizza_app:employee_page'))
    else:
        return HttpResponseRedirect(reverse('pizza_app:user_profile'))


@login_required
def customer_page(request):
    # assert not is_pizza_employee(
    #     request.user), 'Employee routed to customer view.'
    pizzas = Pizza.objects.all()
    userProfiles = UserProfile.objects.filter(user=request.user)
    toppings = Topping.objects.all()

    order = Order.objects.filter(customer=request.user).last()
    if(order):
        print("order exists")
        
        if(order.is_placed):
            order = Order.start_new_order(request.user)
            print("one order has already been placed, creating a new one")
        else:
            order = order
    else:
        order = Order.start_new_order(request.user)
        print("No order found, starting new order")


    context = {
        'toppings' : toppings,
        'pizzas': pizzas,
        'userProfiles': userProfiles,
        'order': order,
    }

    if request.method == 'POST':
        pizza_id = request.POST['pizza_id']

        order.add_pizza_to_order(pizza_id)
        context = {
            'toppings' : toppings,
            'pizzas': pizzas,
            'userProfiles': userProfiles,
            'order': order
        }  
        render(request, 'pizza_app/customer_page.html', context)               
        #return redirect('thank_you/'+ str(order.pk))

    return render(request, 'pizza_app/customer_page.html', context)


@login_required
def user_profile(request):
    if request.method == 'GET':
        # Getting only a single user profile object to pass through in the context, instead of an array which has to be looped through
        userProfile = UserProfile.objects.get(user=request.user)
        context = {
            'userProfile': userProfile,
        }
    return render(request, 'pizza_app/user_profile.html', context)


@login_required
def thank_you(request, pk):
    order = get_object_or_404(Order, pk=pk)
    context = {
        'order': order,
    }
    return render(request, 'pizza_app/thank_you.html', context)


@login_required
def employee_page(request):
    # assert is_pizza_employee(request.user), 'Customer routed to employee view.'
    # if request.method == 'POST':
    #     name = request.POST['pizza_name']
    #     text = request.POST['pizza_text']
    #     price = request.POST['pizza_price']
    #     cover = request.POST['pizza_cover']
    #     pizza = Pizza.create(name, text, price, cover)
    userProfiles = UserProfile.objects.filter(user=request.user)
    pizzas = Pizza.objects.all()
    form= PizzaForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
    context = {
        'pizzas': pizzas,
        'userProfiles': userProfiles,
        'form': form,
    }
    return render(request, 'pizza_app/employee_page.html', context)


@login_required
def base(request):
    userProfiles = UserProfile.objects.filter(user=request.user)
    context = {
        'userProfiles': userProfiles,
    }
    return render(request, 'pizza_app/base.html', context)


# edit PIZZA page
@login_required
def edit_pizza(request, pk):
    pizza = get_object_or_404(Pizza, pk=pk)
    context = {
        'pizza': pizza,
    }
    return render(request, 'pizza_app/edit_pizza.html', context)

# Delete PIZZA


def delete_pizza(request):
    pizza_id = request.POST['pizza_id']
    pizza = get_object_or_404(Pizza, pizza_id=pizza_id)
    pizza.delete()

    return HttpResponseRedirect(reverse('pizza_app:employee_page'))

# Update Pizza


def update_pizza(request):
    pizza_id = request.POST['pizza_id']
    pizza = get_object_or_404(Pizza, pizza_id=pizza_id)
    price = request.POST['pizza_price']
    text = request.POST['pizza_text']
    name = request.POST['pizza_name']
    pizza.price = price
    pizza.text = text
    pizza.name = name
    pizza.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


# CREATE ORDER

@login_required
def edit_customers(request):
    customers = get_user_model().objects.all()
    profiles = UserProfile.objects.all()
    context = {
        'customers': customers,
        'profiles': profiles,
    }
    return render(request, 'pizza_app/edit_customers.html', context)


@login_required
def create_order(request):
    pizzas = Pizza.objects.all()
    userProfiles = UserProfile.objects.filter(user=request.user)
    context = {
        'pizzas': pizzas,
        'userProfiles': userProfiles,
    }
    return render(request, 'pizza_app/edit_pizza.html', context)


# Admin/Orders Page
@login_required
def orders_page(request):

    orders = Order.objects.all()

    context = {
        'orders' : orders
    }

    return render(request, 'pizza_app/orders.html', context)

# Admin/Orders/<int:pk> Page (SINGLE order page)
@login_required
def single_order(request, pk):

    order = get_object_or_404(Order, pk=pk)

    # context = {
    #     'order': order,
    # }

    return render(request, 'pizza_app/single_order.html', {"order":order})

def accept_order(request):
    if request.method == 'POST':
        order_pk = request.POST['order_pk']
        order = get_object_or_404(Order, pk=order_pk)
        order.order_status = "Accepted"
        order.save()

        order.order_status_change()

    

    return HttpResponseRedirect(request.META['HTTP_REFERER'])
        

def fulfill_order(request):
    order_pk = request.POST['order_pk']
    order = get_object_or_404(Order, pk=order_pk)
    order.order_status = "Fulfilled"
    order.save()

    order.order_status_change()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])

# Update Pizza