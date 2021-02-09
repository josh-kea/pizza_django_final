from django.shortcuts import render, reverse
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.contrib.auth import authenticate, login as dj_login, logout as dj_logout
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from . import models
from .models import PasswordResetRequest
from pizza_app.models import UserProfile


# EMAILS
import django_rq
from . messaging import email_message

def login(request):
    context={}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        userProfile = UserProfile.objects.get(user=user)

        if user: 
            if userProfile.isEmployee:
                dj_login(request, user)
                return HttpResponseRedirect(reverse('pizza_app:employee_page')) # new
            elif userProfile.isEmployee == False:
                dj_login(request, user)
                return HttpResponseRedirect(reverse('pizza_app:customer_page')) # new
        else:
            context = {'error': 'Bad username or password.'}
    return render(request, 'login_app/login.html', context)


def logout(request):
    dj_logout(request)
    return HttpResponseRedirect(reverse('login_app:login'))


def password_reset(request):
    context = {}

    if request.method == "POST":
        email = request.POST['email']
        user = User.objects.get(email__exact=email)

        if email:
            try:
               user = User.objects.get(email__exact=email)
               print(f"{email}")
            except:
               print(f"No user with {user} found??")
        if user:
            prr = PasswordResetRequest()
            prr.user = user
            prr.save()
            django_rq.enqueue(email_message, {
               'token' : prr.secret,
               'email' : prr.user.email,
            })
            return HttpResponseRedirect(reverse('login_app:password_reset'))
    
    return render(request, 'login_app/password_reset.html')


def password_reset_secret(request, secret):
    context = {'secret': secret}
    return render(request, 'login_app/password_reset_form.html', context)


def password_reset_form(request):
    email = request.POST['email']
    password = request.POST['password']
    confirm_password = request.POST['confirm_password']
    secret = request.POST['secret']
    user = User.objects.get(email=email)
    reset_request = models.PasswordResetRequest.objects.get(
        user=user, secret=secret)
    if password == confirm_password:
        user.set_password(password)
        user.save()
        reset_request.save()
        return HttpResponseRedirect(reverse('login_app:login'))
    context = {
        'error': 'Something went wrong, try again, don\'t screw up this time!'}
    return render(request, 'login_app/password_reset_form.html', context)


# signup naming changed
def signup(request):
    context = {}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        email = request.POST['email']

        if password == confirm_password:
            try:
                User.objects.create_user(username=username, password=password, email=email)
                return HttpResponseRedirect(reverse('login_app:login'), context)
                
            except IntegrityError:
                context['error'] = 'Could not create user account.'
        else:
            # If passwords do not match.
            context = {'error': 'Passwords do not match.'}
    return render(request, 'login_app/signup.html', context)
