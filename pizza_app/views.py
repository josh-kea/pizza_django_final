from django.shortcuts import render, get_object_or_404, reverse
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model
from .models import UserProfile, Pizza, Order, Topping
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
import random
from django.urls import reverse
from django.shortcuts import redirect
from .forms import PizzaForm
from django.views.generic import CreateView

# EMAILS
import django_rq

def employee_required(login_url=None):
    return user_passes_test(isEmployee, login_url=login_url)

def isEmployee(user):
    user_profile = UserProfile.objects.get(user=user)
    return user_profile.isEmployee

@login_required
@employee_required(login_url="/customer_page")
def index(request):
        return HttpResponseRedirect(reverse('pizza_app:employee_page'))

@login_required
def customer_page(request):
    pizzas = Pizza.objects.all()
    user_profile = UserProfile.objects.get(user=request.user)
    toppings = Topping.objects.all()

    order = Order.objects.filter(customer=request.user).last()
    if(order):
        if(order.is_placed):
            order = Order.start_new_order(request.user)
            print("one order has already been placed, creating a new one")
    else:
        order = Order.start_new_order(request.user)
        print("No order found, starting new order")

    if request.method == 'POST' and 'addBtn' in request.POST:
        pizza_id = request.POST['pizza_id']
        pizza_quantity = request.POST['pizza_quantity']

        order.create_line_item(pizza_id, order)
        context = {
            'toppings' : toppings,
            'pizzas': pizzas,
            'user_profile': user_profile,
            'order': order
        }  
        render(request, 'pizza_app/customer_page.html', context)               
    
    if request.method == 'POST' and 'clearBtn' in request.POST:
        order_id = request.POST['order_id']

        order.clear_line_items()
        context = {
            'toppings' : toppings,
            'pizzas': pizzas,
            'user_profile': user_profile,
            'order': order
        }  
        render(request, 'pizza_app/customer_page.html', context)               

    if request.method == 'POST' and 'placeBtn' in request.POST:
        order_id = request.POST['order_id']
        order.place_order()

        return redirect('thank_you/'+ str(order.pk))              
        
    context = {
        'toppings' : toppings,
        'pizzas': pizzas,
        'user_profile': user_profile,
        'order': order,
    }
    return render(request, 'pizza_app/customer_page.html', context)


@login_required
def user_profile(request):
    if request.method == 'GET':
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
@employee_required(login_url="/customer_page")
def employee_page(request):
    user_profile = UserProfile.objects.get(user=request.user)
    pizzas = Pizza.objects.all()
    form= PizzaForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()

    context = {
        'pizzas': pizzas,
        'user_profile': user_profile,
        'form': form,
    }
    return render(request, 'pizza_app/employee_page.html', context)

@login_required
def base(request):
    user_profile = UserProfile.objects.filter(user=request.user)
    context = {
        'user_profile': user_profile,
    }
    return render(request, 'pizza_app/base.html', context)

@login_required
@employee_required(login_url="/customer_page")
def edit_pizza(request, pk):
    pizza = get_object_or_404(Pizza, pk=pk)
    context = {
        'pizza': pizza,
    }
    return render(request, 'pizza_app/edit_pizza.html', context)

def delete_pizza(request):
    pizza_id = request.POST['pizza_id']
    pizza = get_object_or_404(Pizza, pk=pizza_id)
    pizza.delete()

    return HttpResponseRedirect(reverse('pizza_app:employee_page'))

def update_pizza(request):
    pizza_id = request.POST['pizza_id']
    pizza = get_object_or_404(Pizza, pk=pizza_id)
    pizza.update_pizza(request.POST['pizza_name'], request.POST['pizza_text'], request.POST['pizza_price'])

    return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required
@employee_required(login_url="/customer_page")
def edit_customers(request):
    customers = get_user_model().objects.all()
    profiles = UserProfile.objects.all()
    context = {
        'customers': customers,
        'profiles': profiles,
    }
    return render(request, 'pizza_app/edit_customers.html', context)


# Admin/orders
@login_required
@employee_required(login_url="/customer_page")
def orders_page(request):
    user_profile = UserProfile.objects.get(user=request.user)
    orders = Order.objects.all()

    context = {
        'orders' : orders
    }

    return render(request, 'pizza_app/orders.html', context)

# Admin/Orders/<int:pk> Page (SINGLE order page)
@login_required
@employee_required(login_url="/customer_page")
def single_order(request, pk):
    order = get_object_or_404(Order, pk=pk)

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



def clear_order(request):
    order_id = request.POST['order_id']
    order = get_object_or_404(Order, pk=order_id)
    order.clear_line_items()

    return HttpResponseRedirect(reverse('pizza_app:customer_page'))

def place_order(request):
    order_id = request.POST['order_id']
    order = get_object_or_404(Order, pk=order_id)
    order.place_order()
    
    #return HttpResponseRedirect(reverse('pizza_app:thank_you/' +str(order.pk)))
    return redirect('http://127.0.0.1:8000/thank_you/'+ str(order.pk))
